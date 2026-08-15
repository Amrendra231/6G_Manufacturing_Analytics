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

df = pd.read_csv("Thales_Group_Manufacturing.csv")

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

efficiency_filter = st.sidebar.multiselect(
    "Select Efficiency Status",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

machine_filter = st.sidebar.multiselect(
    "Select Machine ID",
    options=sorted(df["Machine_ID"].unique()),
    default=sorted(df["Machine_ID"].unique())
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["Efficiency_Status"].isin(efficiency_filter)) &
    (df["Machine_ID"].isin(machine_filter))
].copy()

# =========================================================
# BASIC INFORMATION
# =========================================================

total_records = len(filtered_df)
total_machines = filtered_df["Machine_ID"].nunique()

# KPI Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📊 Total Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "🏭 Total Machines",
        total_machines
    )

with col3:
    st.metric(
        "🔎 Filtered Records",
        f"{total_records:,}"
    )

st.divider()

# =========================================================
# 1 & 2. Efficiency and Network Performance
col1, col2 = st.columns(2)

# 1. Efficiency Status Distribution
with col1:
    st.subheader("📊 Efficiency Status Distribution")

    efficiency_count = (
        filtered_df["Efficiency_Status"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
        .dropna()
    )

    fig1, ax1 = plt.subplots(figsize=(7, 5))

    sns.barplot(
        x=efficiency_count.index,
        y=efficiency_count.values,
        ax=ax1
    )

    ax1.set_title("Manufacturing Efficiency Status")
    ax1.set_xlabel("Efficiency Status")
    ax1.set_ylabel("Number of Records")

    for i, value in enumerate(efficiency_count.values):
        ax1.text(
            i,
            value,
            f"{int(value):,}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    st.pyplot(fig1)


# 2. Average Network Latency by Efficiency
with col2:
    st.subheader("📡 Average Network Latency by Efficiency")

    latency_avg = (
        filtered_df
        .groupby("Efficiency_Status")["Network_Latency_ms"]
        .mean()
        .reindex(["Low", "Medium", "High"])
        .dropna()
    )

    fig2, ax2 = plt.subplots(figsize=(7, 5))

    sns.barplot(
        x=latency_avg.index,
        y=latency_avg.values,
        ax=ax2
    )

    ax2.set_title("Average Network Latency by Efficiency")
    ax2.set_xlabel("Efficiency Status")
    ax2.set_ylabel("Average Latency (ms)")

    for i, value in enumerate(latency_avg.values):
        ax2.text(
            i,
            value,
            f"{value:.2f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    st.pyplot(fig2)

st.divider()

# 3 & 4. Network and Production Performance
col1, col2 = st.columns(2)

# 3. Average Packet Loss by Efficiency
with col1:
    st.subheader("📦 Average Packet Loss by Efficiency")

    packet_loss_avg = (
        filtered_df
        .groupby("Efficiency_Status")["Packet_Loss_%"]
        .mean()
        .reindex(["Low", "Medium", "High"])
        .dropna()
    )

    fig3, ax3 = plt.subplots(figsize=(7, 5))

    sns.barplot(
        x=packet_loss_avg.index,
        y=packet_loss_avg.values,
        ax=ax3
    )

    ax3.set_title("Average Packet Loss by Efficiency")
    ax3.set_xlabel("Efficiency Status")
    ax3.set_ylabel("Average Packet Loss (%)")

    for i, value in enumerate(packet_loss_avg.values):
        ax3.text(
            i,
            value,
            f"{value:.3f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    st.pyplot(fig3)


# 4. Average Production Speed by Efficiency
with col2:
    st.subheader("⚙️ Average Production Speed by Efficiency")

    production_avg = (
        filtered_df
        .groupby("Efficiency_Status")["Production_Speed_units_per_hr"]
        .mean()
        .reindex(["Low", "Medium", "High"])
        .dropna()
    )

    fig4, ax4 = plt.subplots(figsize=(7, 5))

    sns.barplot(
        x=production_avg.index,
        y=production_avg.values,
        ax=ax4
    )

    ax4.set_title("Average Production Speed by Efficiency")
    ax4.set_xlabel("Efficiency Status")
    ax4.set_ylabel("Production Speed (units/hr)")

    for i, value in enumerate(production_avg.values):
        ax4.text(
            i,
            value,
            f"{value:.2f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    st.pyplot(fig4)

st.divider()

# 5 & 6. Network Performance vs Production Speed
col1, col2 = st.columns(2)

# 5. Network Latency vs Production Speed
with col1:
    st.subheader("📈 Network Latency vs Production Speed")

    plot_df = filtered_df[
        ["Network_Latency_ms", "Production_Speed_units_per_hr"]
    ].dropna()

    if len(plot_df) > 1:

        latency_corr = plot_df[
            "Network_Latency_ms"
        ].corr(
            plot_df["Production_Speed_units_per_hr"]
        )

        plot_sample = plot_df.sample(
            n=min(2500, len(plot_df)),
            random_state=42
        )

        fig5, ax5 = plt.subplots(figsize=(7, 5))

        sns.scatterplot(
            data=plot_sample,
            x="Network_Latency_ms",
            y="Production_Speed_units_per_hr",
            alpha=0.25,
            s=20,
            ax=ax5
        )

        sns.regplot(
            data=plot_df,
            x="Network_Latency_ms",
            y="Production_Speed_units_per_hr",
            scatter=False,
            ci=None,
            ax=ax5,
            label="Trend Line"
        )

        ax5.set_title(
            f"Latency vs Production\nCorrelation = {latency_corr:.3f}"
        )
        ax5.set_xlabel("Network Latency (ms)")
        ax5.set_ylabel("Production Speed (units/hr)")
        ax5.grid(alpha=0.2)
        ax5.legend()

        plt.tight_layout()
        st.pyplot(fig5)

    else:
        latency_corr = 0
        st.info("Not enough data for correlation analysis.")

    latency_correlation = latency_corr


# 6. Packet Loss vs Production Speed
with col2:
    st.subheader("📦 Packet Loss vs Production Speed")

    packet_df = filtered_df[
        ["Packet_Loss_%", "Production_Speed_units_per_hr"]
    ].dropna()

    if len(packet_df) > 1:

        packet_corr = packet_df[
            "Packet_Loss_%"
        ].corr(
            packet_df["Production_Speed_units_per_hr"]
        )

        packet_sample = packet_df.sample(
            n=min(2500, len(packet_df)),
            random_state=42
        )

        fig6, ax6 = plt.subplots(figsize=(7, 5))

        sns.scatterplot(
            data=packet_sample,
            x="Packet_Loss_%",
            y="Production_Speed_units_per_hr",
            alpha=0.25,
            s=20,
            ax=ax6
        )

        sns.regplot(
            data=packet_df,
            x="Packet_Loss_%",
            y="Production_Speed_units_per_hr",
            scatter=False,
            ci=None,
            ax=ax6,
            label="Trend Line"
        )

        ax6.set_title(
            f"Packet Loss vs Production\nCorrelation = {packet_corr:.3f}"
        )
        ax6.set_xlabel("Packet Loss (%)")
        ax6.set_ylabel("Production Speed (units/hr)")
        ax6.grid(alpha=0.2)
        ax6.legend()

        plt.tight_layout()
        st.pyplot(fig6)

    else:
        packet_corr = 0
        st.info("Not enough data for correlation analysis.")

    packet_correlation = packet_corr

st.divider()
# 7 & 8. Network Insights and Key Findings
col1, col2 = st.columns(2)

# 7. Network Performance Insights
with col1:
    st.subheader("📡 Network Performance Insights")

    st.metric(
        "Latency vs Production Correlation",
        f"{latency_correlation:.3f}"
    )

    st.metric(
        "Packet Loss vs Production Correlation",
        f"{packet_correlation:.3f}"
    )


# 8. Key Findings
with col2:
    st.subheader("🔍 Key Findings")

    st.write(
        "• High efficiency is associated with higher production speed."
    )

    st.write(
        f"• Network latency has a correlation of "
        f"{latency_correlation:.3f} with production speed."
    )

    st.write(
        f"• Packet loss has a correlation of "
        f"{packet_correlation:.3f} with production speed."
    )

    st.write(
        "• Manufacturing efficiency appears to be influenced "
        "by multiple operational factors, not only network performance."
    )

st.divider()
# 9. Conclusion
st.subheader("📝 Conclusion")

st.write(
    "The analysis shows that manufacturing efficiency is strongly "
    "associated with production speed, with high-efficiency operations "
    "achieving higher production rates than medium- and low-efficiency "
    "operations."
)

st.write(
    "However, network latency and packet loss show very weak linear "
    "correlations with production speed in the analyzed dataset."
)

st.write(
    "This indicates that manufacturing efficiency is influenced by "
    "multiple operational factors rather than network performance alone."
)

st.write(
    "Therefore, network performance should be monitored as part of a "
    "broader smart-factory analytics framework rather than being "
    "considered the sole determinant of manufacturing efficiency."
)