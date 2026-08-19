import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="6G Manufacturing Analytics",
    page_icon="🏭",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    data = pd.read_csv("Thales_Group_Manufacturing.csv")

    if "Timestamp" in data.columns:
        data["Timestamp"] = pd.to_datetime(
            data["Timestamp"],
            format="mixed",
            errors="coerce"
        )
    elif "Date" in data.columns:
        data["Timestamp"] = pd.to_datetime(
            data["Date"],
            errors="coerce"
        )

    return data


df = load_data()

# ============================================================
# BASIC VALIDATION
# ============================================================
required_columns = [
    "Machine_ID",
    "Operation_Mode",
    "Network_Latency_ms",
    "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%",
    "Production_Speed_units_per_hr",
    "Error_Rate_%",
    "Efficiency_Status"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "The following required columns are missing from the dataset: "
        + ", ".join(missing_columns)
    )
    st.stop()

# ============================================================
# NETWORK QUALITY CLASSIFICATION
# ============================================================
latency_median = df["Network_Latency_ms"].median()
packet_median = df["Packet_Loss_%"].median()

def classify_network_quality(row):
    latency = row["Network_Latency_ms"]
    packet_loss = row["Packet_Loss_%"]

    if (
        latency <= latency_median
        and packet_loss <= packet_median
    ):
        return "Good"

    if (
        latency <= latency_median * 1.5
        and packet_loss <= packet_median * 1.5
    ):
        return "Moderate"

    return "Poor"


df["Network_Quality"] = df.apply(
    classify_network_quality,
    axis=1
)

# ============================================================
# TITLE
# ============================================================
st.title("🏭 6G Manufacturing Analytics Dashboard")

st.write(
    "Analysis of the impact of network performance "
    "on manufacturing efficiency in smart factories."
)

st.caption(
    "Connectivity-first analytics for latency, packet loss, "
    "manufacturing efficiency and operational resilience."
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("🎛️ Dashboard Filters")

efficiency_options = ["Low", "Medium", "High"]
efficiency_filter = st.sidebar.multiselect(
    "Select Efficiency Status",
    options=efficiency_options,
    default=efficiency_options
)

machine_options = sorted(df["Machine_ID"].dropna().unique())
machine_filter = st.sidebar.multiselect(
    "Select Machine ID",
    options=machine_options,
    default=machine_options
)

operation_options = sorted(
    df["Operation_Mode"].dropna().unique()
)
operation_filter = st.sidebar.multiselect(
    "Select Operation Mode",
    options=operation_options,
    default=operation_options
)

# Time filter
time_filter = "All"

if "Timestamp" in df.columns:
    valid_time = df["Timestamp"].dropna()

    if len(valid_time) > 0:
        min_date = valid_time.min().date()
        max_date = valid_time.max().date()

        time_filter = st.sidebar.date_input(
            "Select Time Window",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

network_quality_filter = st.sidebar.selectbox(
    "Select Network Quality",
    ["All", "Good", "Moderate", "Poor"]
)

# ============================================================
# APPLY FILTERS
# ============================================================
filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Efficiency_Status"].isin(efficiency_filter)
]

filtered_df = filtered_df[
    filtered_df["Machine_ID"].isin(machine_filter)
]

filtered_df = filtered_df[
    filtered_df["Operation_Mode"].isin(operation_filter)
]

if "Timestamp" in filtered_df.columns:
    if isinstance(time_filter, tuple) and len(time_filter) == 2:
        start_date = pd.Timestamp(time_filter[0])
        end_date = (
            pd.Timestamp(time_filter[1])
            + pd.Timedelta(days=1)
            - pd.Timedelta(seconds=1)
        )

        filtered_df = filtered_df[
            filtered_df["Timestamp"].between(
                start_date,
                end_date
            )
        ]

    elif hasattr(time_filter, "year"):
        selected_date = pd.Timestamp(time_filter)

        filtered_df = filtered_df[
            filtered_df["Timestamp"].dt.date
            == selected_date.date()
        ]

if network_quality_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Network_Quality"]
        == network_quality_filter
    ]

# ============================================================
# COMMON VARIABLES
# ============================================================
total_records = len(filtered_df)

total_machines = (
    filtered_df["Machine_ID"].nunique()
    if total_records > 0
    else 0
)

efficiency_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

# ============================================================
# KPI CALCULATIONS
# ============================================================
if total_records > 1:

    # ---------------- Network Stability Index ----------------
    latency_max = df["Network_Latency_ms"].max()
    packet_max = df["Packet_Loss_%"].max()

    latency_score = (
        1
        - (
            filtered_df["Network_Latency_ms"]
            / latency_max
        )
    ) * 100

    packet_score = (
        1
        - (
            filtered_df["Packet_Loss_%"]
            / packet_max
        )
    ) * 100

    network_stability_index = (
        latency_score.mean()
        + packet_score.mean()
    ) / 2

    # ---------------- Latency Sensitivity ----------------
    efficiency_score = (
        filtered_df["Efficiency_Status"]
        .map(efficiency_map)
    )

    latency_values = filtered_df[
        "Network_Latency_ms"
    ]

    valid_latency = (
        latency_values.notna()
        & efficiency_score.notna()
    )

    if valid_latency.sum() > 1:
        latency_sensitivity_per_ms = np.polyfit(
            latency_values[valid_latency],
            efficiency_score[valid_latency],
            1
        )[0]
    else:
        latency_sensitivity_per_ms = 0

    latency_sensitivity_10ms = (
        latency_sensitivity_per_ms * 10
    )

    # ---------------- Packet Loss Impact ----------------
    packet_median_filtered = (
        filtered_df["Packet_Loss_%"].median()
    )

    low_packet_speed = filtered_df[
        filtered_df["Packet_Loss_%"]
        <= packet_median_filtered
    ]["Production_Speed_units_per_hr"].mean()

    high_packet_speed = filtered_df[
        filtered_df["Packet_Loss_%"]
        > packet_median_filtered
    ]["Production_Speed_units_per_hr"].mean()

    if (
        pd.notna(low_packet_speed)
        and low_packet_speed != 0
        and pd.notna(high_packet_speed)
    ):
        packet_loss_impact_ratio = (
            (
                low_packet_speed
                - high_packet_speed
            )
            / low_packet_speed
        ) * 100
    else:
        packet_loss_impact_ratio = 0

    # ---------------- Network-Efficiency Correlation ----------------
    network_efficiency_correlation = (
        filtered_df[
            "Network_Latency_ms"
        ].corr(efficiency_score)
    )

    if pd.isna(network_efficiency_correlation):
        network_efficiency_correlation = 0

else:
    network_stability_index = 0
    latency_sensitivity_10ms = 0
    packet_loss_impact_ratio = 0
    network_efficiency_correlation = 0

# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================
st.subheader("📌 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "🌐 Network Stability Index",
        f"{network_stability_index:.2f}"
    )
    st.caption("Higher score = more stable network conditions")

with k2:
    st.metric(
        "📉 Latency Sensitivity / 10 ms",
        f"{latency_sensitivity_10ms:.3f}"
    )
    st.caption(
        "Efficiency-score change associated with 10 ms latency"
    )

with k3:
    st.metric(
        "📦 Packet Loss Impact Ratio",
        f"{packet_loss_impact_ratio:.2f}%"
    )
    st.caption(
        "Production-speed difference above/below median packet loss"
    )

with k4:
    st.metric(
        "🔗 Network-Efficiency Correlation",
        f"{network_efficiency_correlation:.3f}"
    )
    st.caption("Linear correlation between latency and efficiency score")

st.divider()

# ============================================================
# FILTERED DATASET OVERVIEW
# ============================================================
st.subheader("📋 Filtered Dataset Overview")

o1, o2, o3, o4 = st.columns(4)

with o1:
    st.metric(
        "Total Records",
        f"{total_records:,}"
    )

with o2:
    st.metric(
        "Machines",
        total_machines
    )

with o3:
    avg_latency = (
        filtered_df["Network_Latency_ms"].mean()
        if total_records > 0
        else 0
    )

    st.metric(
        "Average Latency",
        f"{avg_latency:.2f} ms"
    )

with o4:
    avg_speed = (
        filtered_df["Production_Speed_units_per_hr"].mean()
        if total_records > 0
        else 0
    )

    st.metric(
        "Average Production Speed",
        f"{avg_speed:.2f}"
    )

st.divider()

# ============================================================
# NETWORK PERFORMANCE OVERVIEW
# ============================================================
st.subheader("📈 Network Performance Overview")

st.caption(
    "Hourly network trends are compared with the dataset median "
    "latency and packet-loss levels."
)

if total_records > 1 and "Timestamp" in filtered_df.columns:

    trend_df = (
        filtered_df
        .dropna(
            subset=[
                "Timestamp",
                "Network_Latency_ms",
                "Packet_Loss_%"
            ]
        )
        .sort_values("Timestamp")
        .copy()
    )

    if len(trend_df) > 1:

        trend_hourly = (
            trend_df
            .set_index("Timestamp")
            .resample("1h")
            .agg({
                "Network_Latency_ms": "mean",
                "Packet_Loss_%": "mean"
            })
            .dropna()
            .reset_index()
        )

        trend_hourly["Network_Status"] = np.where(
            (
                (
                    trend_hourly["Network_Latency_ms"]
                    <= latency_median
                )
                &
                (
                    trend_hourly["Packet_Loss_%"]
                    <= packet_median
                )
            ),
            "Stable",
            "Unstable"
        )

        c1, c2 = st.columns(2)

        with c1:
            fig_latency, ax_latency = plt.subplots(
                figsize=(7, 5)
            )

            ax_latency.plot(
                trend_hourly["Timestamp"],
                trend_hourly["Network_Latency_ms"],
                marker="o",
                markersize=3
            )

            ax_latency.axhline(
                latency_median,
                linestyle="--",
                label=f"Median: {latency_median:.2f} ms"
            )

            ax_latency.set_title(
                "Hourly Network Latency Trend"
            )
            ax_latency.set_xlabel("Time")
            ax_latency.set_ylabel("Latency (ms)")
            ax_latency.legend()
            ax_latency.grid(alpha=0.2)

            plt.xticks(rotation=30)
            plt.tight_layout()

            st.pyplot(fig_latency)
            plt.close(fig_latency)

        with c2:
            fig_packet, ax_packet = plt.subplots(
                figsize=(7, 5)
            )

            ax_packet.plot(
                trend_hourly["Timestamp"],
                trend_hourly["Packet_Loss_%"],
                marker="o",
                markersize=3
            )

            ax_packet.axhline(
                packet_median,
                linestyle="--",
                label=f"Median: {packet_median:.2f}%"
            )

            ax_packet.set_title(
                "Hourly Packet Loss Trend"
            )
            ax_packet.set_xlabel("Time")
            ax_packet.set_ylabel("Packet Loss (%)")
            ax_packet.legend()
            ax_packet.grid(alpha=0.2)

            plt.xticks(rotation=30)
            plt.tight_layout()

            st.pyplot(fig_packet)
            plt.close(fig_packet)

        stable_periods = (
            trend_hourly["Network_Status"]
            == "Stable"
        ).sum()

        unstable_periods = (
            trend_hourly["Network_Status"]
            == "Unstable"
        ).sum()

        st.write("### 🌐 Network Stability Periods")

        s1, s2 = st.columns(2)

        with s1:
            st.metric(
                "Stable Hourly Periods",
                f"{stable_periods:,}"
            )

        with s2:
            st.metric(
                "Unstable Hourly Periods",
                f"{unstable_periods:,}"
            )

        st.caption(
            "Stable/Unstable is a relative classification based on "
            "dataset median latency and packet-loss thresholds; "
            "it is not a causal diagnosis."
        )

    else:
        st.info(
            "Insufficient timestamp data for trend analysis."
        )

else:
    st.info(
        "Insufficient data for network trend analysis."
    )

st.divider()

# ============================================================
# MANUFACTURING EFFICIENCY ANALYSIS
# ============================================================
st.subheader("📊 Manufacturing Efficiency Analysis")

col1, col2 = st.columns(2)

with col1:

    st.write("### Efficiency Status Distribution")

    if total_records > 0:

        efficiency_count = (
            filtered_df["Efficiency_Status"]
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"]
            )
            .fillna(0)
        )

        fig1, ax1 = plt.subplots(
            figsize=(7, 4.5)
        )

        sns.barplot(
            x=efficiency_count.index,
            y=efficiency_count.values,
            ax=ax1,
            hue=efficiency_count.index,
            palette="Set2",
            legend=False
        )

        ax1.set_title(
            "Manufacturing Efficiency Distribution"
        )
        ax1.set_ylabel("Number of Records")

        for i, value in enumerate(
            efficiency_count.values
        ):
            ax1.text(
                i,
                value,
                f"{int(value):,}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    else:
        st.info("No data available.")

with col2:

    st.write("### Average Latency by Efficiency")

    if total_records > 0:

        latency_avg = (
            filtered_df
            .groupby("Efficiency_Status")
            ["Network_Latency_ms"]
            .mean()
            .reindex(
                ["Low", "Medium", "High"]
            )
            .dropna()
        )

        fig2, ax2 = plt.subplots(
            figsize=(7, 4.5)
        )

        sns.barplot(
            x=latency_avg.index,
            y=latency_avg.values,
            ax=ax2,
            hue=latency_avg.index,
            palette="viridis",
            legend=False
        )

        ax2.set_title(
            "Average Network Latency by Efficiency"
        )
        ax2.set_ylabel("Average Latency (ms)")

        for i, value in enumerate(
            latency_avg.values
        ):
            ax2.text(
                i,
                value,
                f"{value:.2f}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    else:
        st.info("No data available.")

st.divider()

# ============================================================
# NETWORK QUALITY VS EFFICIENCY
# ============================================================
st.subheader(
    "🌐 Efficiency Distribution by Network Quality"
)

st.caption(
    "Network Quality is a relative analytical classification: "
    "Good, Moderate and Poor based on latency and packet-loss thresholds."
)

if total_records > 0:

    quality_efficiency = pd.crosstab(
        filtered_df["Network_Quality"],
        filtered_df["Efficiency_Status"]
    ).reindex(
        index=["Good", "Moderate", "Poor"],
        columns=["Low", "Medium", "High"],
        fill_value=0
    )

    quality_efficiency_pct = (
        quality_efficiency
        .div(
            quality_efficiency.sum(axis=1),
            axis=0
        )
        * 100
    ).round(2)

    st.write("### Efficiency Distribution (%)")

    st.dataframe(
        quality_efficiency_pct,
        use_container_width=True
    )

    fig_quality, ax_quality = plt.subplots(
        figsize=(10, 5)
    )

    quality_efficiency_pct.plot(
        kind="bar",
        stacked=True,
        ax=ax_quality
    )

    ax_quality.set_title(
        "Manufacturing Efficiency by Network Quality (%)"
    )
    ax_quality.set_xlabel("Network Quality")
    ax_quality.set_ylabel("Percentage of Records")
    ax_quality.set_ylim(0, 100)

    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig_quality)
    plt.close(fig_quality)

else:
    st.info(
        "No data available for network quality analysis."
    )

st.divider()

# ============================================================
# LATENCY THRESHOLD ANALYSIS
# ============================================================
st.subheader(
    "🎯 Latency Threshold & Efficiency Drop Analysis"
)

st.caption(
    "Analytical benchmark zones: Optimal <15 ms, "
    "Moderate 15–35 ms, Degraded >35 ms. "
    "These are comparison thresholds, not causal limits."
)

if total_records > 0:

    threshold_df = filtered_df.copy()

    threshold_df["Latency_Band"] = pd.cut(
        threshold_df["Network_Latency_ms"],
        bins=[
            -np.inf,
            15,
            35,
            np.inf
        ],
        labels=[
            "Optimal (<15 ms)",
            "Moderate (15–35 ms)",
            "Degraded (>35 ms)"
        ]
    )

    threshold_df["Efficiency_Score"] = (
        threshold_df["Efficiency_Status"]
        .map(efficiency_map)
    )

    latency_analysis = (
        threshold_df
        .groupby(
            "Latency_Band",
            observed=False
        )
        .agg(
            Average_Efficiency=(
                "Efficiency_Score",
                "mean"
            ),
            Average_Production_Speed=(
                "Production_Speed_units_per_hr",
                "mean"
            ),
            Average_Packet_Loss=(
                "Packet_Loss_%",
                "mean"
            ),
            Records=(
                "Latency_Band",
                "size"
            )
        )
        .round(2)
    )

    st.write(
        "### Manufacturing Performance across Latency Zones"
    )

    st.dataframe(
        latency_analysis,
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:

        fig_threshold1, ax_threshold1 = plt.subplots(
            figsize=(7, 4.5)
        )

        sns.barplot(
            data=latency_analysis.reset_index(),
            x="Latency_Band",
            y="Average_Efficiency",
            ax=ax_threshold1,
            hue="Latency_Band",
            palette="viridis",
            legend=False
        )

        ax_threshold1.set_title(
            "Efficiency Score across Latency Zones"
        )
        ax_threshold1.set_xlabel("Latency Zone")
        ax_threshold1.set_ylabel(
            "Average Efficiency Score"
        )

        plt.xticks(rotation=15)
        plt.tight_layout()

        st.pyplot(fig_threshold1)
        plt.close(fig_threshold1)

    with c2:

        fig_threshold2, ax_threshold2 = plt.subplots(
            figsize=(7, 4.5)
        )

        sns.barplot(
            data=latency_analysis.reset_index(),
            x="Latency_Band",
            y="Average_Production_Speed",
            ax=ax_threshold2,
            hue="Latency_Band",
            palette="Set2",
            legend=False
        )

        ax_threshold2.set_title(
            "Production Speed across Latency Zones"
        )
        ax_threshold2.set_xlabel("Latency Zone")
        ax_threshold2.set_ylabel(
            "Production Speed (units/hr)"
        )

        plt.xticks(rotation=15)
        plt.tight_layout()

        st.pyplot(fig_threshold2)
        plt.close(fig_threshold2)

else:
    st.info(
        "No data available for latency threshold analysis."
    )

st.divider()

# ============================================================
# LATENCY IMPACT DIAGNOSTICS
# ============================================================
st.subheader("📉 Latency Impact Diagnostics")

col1, col2 = st.columns(2)

with col1:

    st.write(
        "### Production Speed vs Network Latency"
    )

    plot_df = filtered_df[
        [
            "Network_Latency_ms",
            "Production_Speed_units_per_hr"
        ]
    ].dropna()

    if len(plot_df) > 1:

        latency_production_corr = (
            plot_df["Network_Latency_ms"]
            .corr(
                plot_df[
                    "Production_Speed_units_per_hr"
                ]
            )
        )

        plot_sample = plot_df.sample(
            n=min(2500, len(plot_df)),
            random_state=42
        )

        fig5, ax5 = plt.subplots(
            figsize=(7, 5)
        )

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
            f"Latency vs Production\n"
            f"Correlation = {latency_production_corr:.3f}"
        )

        ax5.set_xlabel(
            "Network Latency (ms)"
        )

        ax5.set_ylabel(
            "Production Speed (units/hr)"
        )

        ax5.grid(alpha=0.2)
        ax5.legend()

        plt.tight_layout()

        st.pyplot(fig5)
        plt.close(fig5)

    else:
        st.info(
            "Not enough data for latency analysis."
        )

with col2:

    st.write(
        "### Production Speed vs Packet Loss"
    )

    packet_df = filtered_df[
        [
            "Packet_Loss_%",
            "Production_Speed_units_per_hr"
        ]
    ].dropna()

    if len(packet_df) > 1:

        packet_production_corr = (
            packet_df["Packet_Loss_%"]
            .corr(
                packet_df[
                    "Production_Speed_units_per_hr"
                ]
            )
        )

        packet_sample = packet_df.sample(
            n=min(2500, len(packet_df)),
            random_state=42
        )

        fig6, ax6 = plt.subplots(
            figsize=(7, 5)
        )

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
            f"Packet Loss vs Production\n"
            f"Correlation = {packet_production_corr:.3f}"
        )

        ax6.set_xlabel(
            "Packet Loss (%)"
        )

        ax6.set_ylabel(
            "Production Speed (units/hr)"
        )

        ax6.grid(alpha=0.2)
        ax6.legend()

        plt.tight_layout()

        st.pyplot(fig6)
        plt.close(fig6)

    else:
        st.info(
            "Not enough data for packet-loss analysis."
        )

st.divider()

# ============================================================
# OPERATION MODE INTERACTION
# ============================================================
st.subheader(
    "⚙️ Operation Mode Interaction Analysis"
)

if total_records > 0:

    operation_summary = (
        filtered_df
        .groupby("Operation_Mode")
        .agg(
            Average_Production_Speed=(
                "Production_Speed_units_per_hr",
                "mean"
            ),
            Average_Latency=(
                "Network_Latency_ms",
                "mean"
            ),
            Average_Packet_Loss=(
                "Packet_Loss_%",
                "mean"
            ),
            Average_Defect_Rate=(
                "Quality_Control_Defect_Rate_%",
                "mean"
            ),
            Average_Error_Rate=(
                "Error_Rate_%",
                "mean"
            ),
            Records=(
                "Operation_Mode",
                "size"
            )
        )
        .round(2)
    )

    st.dataframe(
        operation_summary,
        use_container_width=True
    )

    c1, c2 = st.columns(2)

    with c1:

        fig_operation1, ax_operation1 = plt.subplots(
            figsize=(7, 4.5)
        )

        operation_summary[
            "Average_Production_Speed"
        ].plot(
            kind="bar",
            ax=ax_operation1
        )

        ax_operation1.set_title(
            "Production Speed by Operation Mode"
        )

        ax_operation1.set_xlabel(
            "Operation Mode"
        )

        ax_operation1.set_ylabel(
            "Production Speed (units/hr)"
        )

        plt.xticks(rotation=30)
        plt.tight_layout()

        st.pyplot(fig_operation1)
        plt.close(fig_operation1)

    with c2:

        fig_operation2, ax_operation2 = plt.subplots(
            figsize=(7, 4.5)
        )

        operation_summary[
            "Average_Latency"
        ].plot(
            kind="bar",
            ax=ax_operation2
        )

        ax_operation2.set_title(
            "Network Latency by Operation Mode"
        )

        ax_operation2.set_xlabel(
            "Operation Mode"
        )

        ax_operation2.set_ylabel(
            "Latency (ms)"
        )

        plt.xticks(rotation=30)
        plt.tight_layout()

        st.pyplot(fig_operation2)
        plt.close(fig_operation2)

else:
    st.info(
        "No data available for operation mode analysis."
    )

st.divider()

# ============================================================
# QUALITY & ERROR IMPACT
# ============================================================
st.subheader(
    "🧪 Quality & Error Impact"
)

col1, col2 = st.columns(2)

with col1:

    st.write(
        "### Error Rate vs Packet Loss"
    )

    error_df = filtered_df[
        [
            "Packet_Loss_%",
            "Error_Rate_%"
        ]
    ].dropna()

    if len(error_df) > 1:

        error_sample = error_df.sample(
            n=min(2500, len(error_df)),
            random_state=42
        )

        error_corr = (
            error_df["Packet_Loss_%"]
            .corr(
                error_df["Error_Rate_%"]
            )
        )

        fig_error, ax_error = plt.subplots(
            figsize=(7, 5)
        )

        sns.scatterplot(
            data=error_sample,
            x="Packet_Loss_%",
            y="Error_Rate_%",
            alpha=0.25,
            s=20,
            ax=ax_error
        )

        sns.regplot(
            data=error_df,
            x="Packet_Loss_%",
            y="Error_Rate_%",
            scatter=False,
            ci=None,
            ax=ax_error,
            label="Trend Line"
        )

        ax_error.set_title(
            f"Error Rate vs Packet Loss\n"
            f"Correlation = {error_corr:.3f}"
        )

        ax_error.set_xlabel(
            "Packet Loss (%)"
        )

        ax_error.set_ylabel(
            "Error Rate (%)"
        )

        ax_error.grid(alpha=0.2)
        ax_error.legend()

        plt.tight_layout()

        st.pyplot(fig_error)
        plt.close(fig_error)

    else:
        st.info(
            "Not enough data."
        )

with col2:

    st.write(
        "### Defect Rate vs Network Latency"
    )

    defect_df = filtered_df[
        [
            "Network_Latency_ms",
            "Quality_Control_Defect_Rate_%"
        ]
    ].dropna()

    if len(defect_df) > 1:

        defect_sample = defect_df.sample(
            n=min(2500, len(defect_df)),
            random_state=42
        )

        defect_corr = (
            defect_df["Network_Latency_ms"]
            .corr(
                defect_df[
                    "Quality_Control_Defect_Rate_%"
                ]
            )
        )

        fig_defect, ax_defect = plt.subplots(
            figsize=(7, 5)
        )

        sns.scatterplot(
            data=defect_sample,
            x="Network_Latency_ms",
            y="Quality_Control_Defect_Rate_%",
            alpha=0.25,
            s=20,
            ax=ax_defect
        )

        sns.regplot(
            data=defect_df,
            x="Network_Latency_ms",
            y="Quality_Control_Defect_Rate_%",
            scatter=False,
            ci=None,
            ax=ax_defect,
            label="Trend Line"
        )

        ax_defect.set_title(
            f"Defect Rate vs Latency\n"
            f"Correlation = {defect_corr:.3f}"
        )

        ax_defect.set_xlabel(
            "Network Latency (ms)"
        )

        ax_defect.set_ylabel(
            "Defect Rate (%)"
        )

        ax_defect.grid(alpha=0.2)
        ax_defect.legend()

        plt.tight_layout()

        st.pyplot(fig_defect)
        plt.close(fig_defect)

    else:
        st.info(
            "Not enough data."
        )

st.divider()

# ============================================================
# 6G OPTIMIZATION INSIGHTS
# ============================================================
st.subheader(
    "🚀 6G Optimization Insights & Recommendations"
)

if total_records > 0:

    avg_latency_current = (
        filtered_df["Network_Latency_ms"].mean()
    )

    avg_packet_current = (
        filtered_df["Packet_Loss_%"].mean()
    )

    avg_error_current = (
        filtered_df["Error_Rate_%"].mean()
    )

    avg_defect_current = (
        filtered_df[
            "Quality_Control_Defect_Rate_%"
        ].mean()
    )

    st.write(
        "### 📡 Network Performance Assessment"
    )

    i1, i2, i3, i4 = st.columns(4)

    with i1:
        st.metric(
            "Average Latency",
            f"{avg_latency_current:.2f} ms"
        )

    with i2:
        st.metric(
            "Average Packet Loss",
            f"{avg_packet_current:.2f}%"
        )

    with i3:
        st.metric(
            "Average Error Rate",
            f"{avg_error_current:.2f}%"
        )

    with i4:
        st.metric(
            "Average Defect Rate",
            f"{avg_defect_current:.2f}%"
        )

    st.write(
        "### 🎯 Recommended Actions"
    )

    st.markdown(
        """
        **1. Prioritize Ultra-Low Latency Connectivity**

        Deploy low-latency network slices for critical production,
        robotics and real-time automation.

        **2. Monitor Packet Loss Continuously**

        Establish real-time monitoring and automated alerts when
        packet-loss levels enter critical zones.

        **3. Use Network Threshold Monitoring**

        Track latency zones such as optimal, moderate and degraded
        operating ranges.

        **4. Adopt Predictive Network Management**

        Combine network monitoring with predictive maintenance
        and manufacturing analytics.

        **5. Build Resilient Smart-Factory Infrastructure**

        Critical manufacturing systems should use reliable
        connectivity, redundancy and proactive network management.
        """
    )

st.divider()

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
st.subheader(
    "🏛️ Executive Summary for Government & Industry Stakeholders"
)

st.markdown(
    """
    ### Strategic Findings

    This analysis evaluates whether 6G network performance,
    particularly network latency and packet loss, is associated
    with manufacturing efficiency in smart-factory environments.

    **Key observations:**

    - Network latency and packet loss provide measurable
      indicators of communication quality.

    - The observed Network-Efficiency Correlation is weak,
      indicating that network performance alone does not explain
      the variation in manufacturing efficiency within this dataset.

    - Production speed, error rate and quality metrics should
      therefore be evaluated together with network conditions.

    - Different operation modes can experience different network
      and production characteristics.

    ### Recommended Actions

    1. **Prioritize Ultra-Low Latency Connectivity**

       Deploy low-latency network slices for critical production,
       robotics and real-time automation.

    2. **Monitor Packet Loss Continuously**

       Establish real-time monitoring and automated alerts when
       packet-loss levels enter critical zones.

    3. **Use Network Threshold Monitoring**

       Track latency zones such as optimal, moderate and degraded
       operating ranges.

    4. **Adopt Predictive Network Management**

       Combine network monitoring with predictive maintenance
       and manufacturing analytics.

    5. **Build Resilient Smart-Factory Infrastructure**

       Critical manufacturing systems should use reliable
       connectivity, redundancy and proactive network management.

    ### Policy & Infrastructure Perspective

    Future smart-factory and Industry 5.0 infrastructure planning
    should consider network reliability as one component of overall
    manufacturing resilience rather than treating connectivity as
    the only driver of efficiency.
    """
)

st.divider()

# ============================================================
# CONCLUSION
# ============================================================
st.subheader("📝 Conclusion")

st.write(
    "The analysis evaluates network latency and packet loss "
    "as potential contributors to manufacturing performance."
)

st.write(
    "In the analyzed dataset, network latency and packet loss "
    "show weak linear relationships with manufacturing efficiency "
    "and production speed."
)

st.write(
    "This indicates that manufacturing efficiency is influenced "
    "by multiple operational factors rather than network performance alone."
)

st.write(
    "Therefore, network performance should be monitored as part "
    "of a broader smart-factory analytics framework."
)

st.success(
    "Connectivity-first analytics can support resilient "
    "6G-enabled smart manufacturing by combining network monitoring "
    "with production, quality and operational data."
)