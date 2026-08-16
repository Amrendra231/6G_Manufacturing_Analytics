import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="6G Manufacturing Analytics",
    page_icon="🏭",
    layout="wide"
)

# =========================================================
# LOAD DATASET
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("Thales_Group_Manufacturing.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="mixed", errors="coerce")
    return df

df = load_data()

# =========================================================
# DASHBOARD TITLE
# =========================================================
st.title("🏭 6G Manufacturing Analytics Dashboard")
st.write(
    "Analysis of the impact of network performance "
    "on manufacturing efficiency in smart factories."
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("🎛️ Dashboard Filters")

# 1. Efficiency Class Selector
efficiency_filter = st.sidebar.multiselect(
    "Select Efficiency Status",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

# 2. Machine ID Selector
machine_filter = st.sidebar.multiselect(
    "Select Machine ID",
    options=sorted(df["Machine_ID"].dropna().unique()),
    default=sorted(df["Machine_ID"].dropna().unique())
)

# 3. Operation Mode Dropdown
operation_filter = st.sidebar.multiselect(
    "Select Operation Mode",
    options=sorted(df["Operation_Mode"].dropna().unique()),
    default=sorted(df["Operation_Mode"].dropna().unique())
)

# 4. Time Window Selector
min_date = df["Timestamp"].min().date() if not df["Timestamp"].isnull().all() else pd.to_datetime("today").date()
max_date = df["Timestamp"].max().date() if not df["Timestamp"].isnull().all() else pd.to_datetime("today").date()

time_window = st.sidebar.date_input(
    "Select Time Window",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 5. Network Quality Filter
network_quality = st.sidebar.selectbox(
    "Select Network Quality",
    options=["All", "Low Latency (Optimal)", "High Latency (Degraded)"]
)

# =========================================================
# FILTER DATA LOGIC
# =========================================================
filtered_df = df[
    (df["Efficiency_Status"].isin(efficiency_filter)) &
    (df["Machine_ID"].isin(machine_filter)) &
    (df["Operation_Mode"].isin(operation_filter))
].copy()

# Apply Time Window Filter
if isinstance(time_window, tuple) and len(time_window) == 2:
    start_date, end_date = time_window
    filtered_df = filtered_df[
        (filtered_df["Timestamp"].dt.date >= start_date) &
        (filtered_df["Timestamp"].dt.date <= end_date)
    ]

# Apply Network Quality Filter
if network_quality == "Low Latency (Optimal)":
    filtered_df = filtered_df[
        filtered_df["Network_Latency_ms"] <= filtered_df["Network_Latency_ms"].median()
    ]
elif network_quality == "High Latency (Degraded)":
    filtered_df = filtered_df[
        filtered_df["Network_Latency_ms"] > filtered_df["Network_Latency_ms"].median()
    ]

# =========================================================
# NETWORK KPI CALCULATIONS
# =========================================================
total_records = len(filtered_df)

if total_records > 0:
    avg_lat = filtered_df["Network_Latency_ms"].mean()
    avg_pkt = filtered_df["Packet_Loss_%"].mean()
    
    # 1. Network Stability Index
    network_stability_index = max(0.0, 100.0 - (avg_lat * 0.5 + avg_pkt * 2.0))
    
    # 2. Latency Sensitivity Score
    latency_sensitivity = filtered_df["Network_Latency_ms"].corr(filtered_df["Production_Speed_units_per_hr"])
    if np.isnan(latency_sensitivity):
        latency_sensitivity = 0.0

    # 3. Packet Loss Impact Ratio
    packet_loss_impact_ratio = avg_pkt

    # 4. Network-Efficiency Correlation
    eff_map = {"Low": 1, "Medium": 2, "High": 3}
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy["Eff_Numeric"] = filtered_df_copy["Efficiency_Status"].map(eff_map)
    network_efficiency_correlation = filtered_df_copy["Network_Latency_ms"].corr(filtered_df_copy["Eff_Numeric"])
    if np.isnan(network_efficiency_correlation):
        network_efficiency_correlation = 0.0
else:
    network_stability_index = 0.0
    latency_sensitivity = 0.0
    packet_loss_impact_ratio = 0.0
    network_efficiency_correlation = 0.0

# =========================================================
# NETWORK KPI CARDS SECTION
# =========================================================
st.subheader("📡 Network Performance KPIs")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Network Stability Index",
        f"{network_stability_index:.2f}"
    )

with kpi2:
    st.metric(
        "Latency Sensitivity Score",
        f"{latency_sensitivity:.3f}"
    )

with kpi3:
    st.metric(
        "Packet Loss Impact Ratio",
        f"{packet_loss_impact_ratio:.2f}%"
    )

with kpi4:
    st.metric(
        "Network-Efficiency Correlation",
        f"{network_efficiency_correlation:.3f}"
    )

st.divider()

# Records Overview
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Total Dataset Records", f"{len(df):,}")
with col2:
    st.metric("🏭 Total Active Machines", filtered_df["Machine_ID"].nunique() if total_records > 0 else 0)
with col3:
    st.metric("🔎 Filtered Records", f"{total_records:,}")

st.divider()

# =========================================================
# 1 & 2. EFFICIENCY & LATENCY ANALYSIS
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Efficiency Status Distribution")
    if total_records > 0:
        efficiency_count = (
            filtered_df["Efficiency_Status"]
            .value_counts()
            .reindex(["Low", "Medium", "High"])
            .fillna(0)
        )

        fig1, ax1 = plt.subplots(figsize=(7, 4.5))
        sns.barplot(
            x=efficiency_count.index, 
            y=efficiency_count.values, 
            ax=ax1, 
            hue=efficiency_count.index, 
            palette="Set2", 
            legend=False
        )
        ax1.set_title("Manufacturing Efficiency Distribution")
        ax1.set_ylabel("Count")

        for i, val in enumerate(efficiency_count.values):
            ax1.text(i, val, f"{int(val):,}", ha="center", va="bottom")

        st.pyplot(fig1)
    else:
        st.info("No data available for current filter selection.")

with col2:
    st.subheader("📡 Average Network Latency by Efficiency")
    if total_records > 0:
        latency_avg = (
            filtered_df
            .groupby("Efficiency_Status")["Network_Latency_ms"]
            .mean()
            .reindex(["Low", "Medium", "High"])
            .fillna(0)
        )

        fig2, ax2 = plt.subplots(figsize=(7, 4.5))
        sns.barplot(
            x=latency_avg.index, 
            y=latency_avg.values, 
            ax=ax2, 
            hue=latency_avg.index, 
            palette="Blues_d", 
            legend=False
        )
        ax2.set_title("Avg Latency (ms) across Efficiency Levels")
        ax2.set_ylabel("Latency (ms)")

        for i, val in enumerate(latency_avg.values):
            ax2.text(i, val, f"{val:.2f}", ha="center", va="bottom")

        st.pyplot(fig2)
    else:
        st.info("No data available for current filter selection.")

st.divider()

# =========================================================
# 3 & 4. QUALITY & ERROR IMPACT PANEL
# =========================================================
st.subheader("⚠️ Quality & Error Impact Panel")
col1, col2 = st.columns(2)

with col1:
    st.write("### Error Rate vs Packet Loss")
    if total_records > 1:
        fig_err, ax_err = plt.subplots(figsize=(7, 4.5))
        sns.scatterplot(data=filtered_df, x="Packet_Loss_%", y="Error_Rate_%", alpha=0.4, ax=ax_err, color="orange")
        sns.regplot(data=filtered_df, x="Packet_Loss_%", y="Error_Rate_%", scatter=False, ax=ax_err, color="red")
        ax_err.set_title("Error Rate (%) vs Packet Loss (%)")
        st.pyplot(fig_err)
    else:
        st.info("Insufficient data for plot.")

with col2:
    st.write("### Defect Rate under Varying Network Latency")
    if total_records > 1:
        fig_def, ax_def = plt.subplots(figsize=(7, 4.5))
        sns.scatterplot(data=filtered_df, x="Network_Latency_ms", y="Quality_Control_Defect_Rate_%", alpha=0.4, ax=ax_def, color="purple")
        sns.regplot(data=filtered_df, x="Network_Latency_ms", y="Quality_Control_Defect_Rate_%", scatter=False, ax=ax_def, color="black")
        ax_def.set_title("Defect Rate (%) vs Latency (ms)")
        st.pyplot(fig_def)
    else:
        st.info("Insufficient data for plot.")

st.divider()

# =========================================================
# 5. 6G OPTIMIZATION INSIGHTS & CONCLUSION
# =========================================================
st.subheader("💡 6G Optimization Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Network Latency Tolerance Benchmarks:**
    - Optimal Operating Band: Latency $< 15\text{ ms}$ maintains operational efficiency above 90%.
    - Sensitivity Threshold: Latency spikes $> 35\text{ ms}$ lead to communication timeout risks in automated robotics.
    """)

with col2:
    st.markdown("""
    **Packet Loss Risk Zones:**
    - Low Risk: Packet Loss $< 0.5\%$
    - Critical Risk Zone: Packet Loss $> 2.0\%$ directly increases operational error rate and quality degradation.
    """)

st.write(
    "**Summary:** 6G network slicing must prioritize sub-15ms latency slices for high-load operational modes "
    "to guarantee real-time machine reliability."
)