import pandas as pd

df = pd.read_csv("Thales_Group_Manufacturing.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())
print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())
print("\nEfficiency Status Distribution:")
print(df["Efficiency_Status"].value_counts())

print("\nEfficiency Status Percentage:")
print(df["Efficiency_Status"].value_counts(normalize=True) * 100)
print("\nAverage Network Latency by Efficiency:")
print(df.groupby("Efficiency_Status")["Network_Latency_ms"].mean())
print("\nAverage Packet Loss by Efficiency:")
print(df.groupby("Efficiency_Status")["Packet_Loss_%"].mean())
print("\nAverage Production Speed by Efficiency:")
print(df.groupby("Efficiency_Status")["Production_Speed_units_per_hr"].mean())
print("\nCorrelation between Network Latency and Packet Loss:")
print(df["Network_Latency_ms"].corr(df["Packet_Loss_%"]))
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Network_Latency_ms",
    data=df
)

plt.title("Network Latency by Efficiency Status")
plt.xlabel("Efficiency Status")
plt.ylabel("Network Latency (ms)")

plt.show()
plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Packet_Loss_%",
    data=df
)

plt.title("Packet Loss by Efficiency Status")
plt.xlabel("Efficiency Status")
plt.ylabel("Packet Loss (%)")

plt.show()
plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Production_Speed_units_per_hr",
    data=df
)

plt.title("Production Speed by Efficiency Status")
plt.xlabel("Efficiency Status")
plt.ylabel("Production Speed (units/hr)")

plt.show()
plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Production_Speed_units_per_hr",
    data=df
)

plt.title("Production Speed by Efficiency Status")
plt.xlabel("Efficiency Status")
plt.ylabel("Production Speed (units/hr)")

plt.show()
plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Packet_Loss_%",
    data=df
)

plt.title("Packet Loss by Efficiency Status")
plt.xlabel("Efficiency Status")
plt.ylabel("Packet Loss (%)")

plt.show()
plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Packet_Loss_%",
    data=df
)

plt.title("Packet Loss by Efficiency Status")
plt.xlabel("Efficiency Status")
plt.ylabel("Packet Loss (%)")

plt.show()
print("\nComplete Efficiency Comparison:")

summary = df.groupby("Efficiency_Status")[
    [
        "Network_Latency_ms",
        "Packet_Loss_%",
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean()

print(summary)
plt.figure(figsize=(10, 7))

correlation_data = df[
    [
        "Network_Latency_ms",
        "Packet_Loss_%",
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%",
        "Predictive_Maintenance_Score"
    ]
]

sns.heatmap(
    correlation_data.corr(),
    annot=True,
    fmt=".2f"
)

plt.title("Correlation Between Network and Manufacturing Performance")
plt.show()
plt.figure(figsize=(10, 7))

correlation_data = df[
    [
        "Network_Latency_ms",
        "Packet_Loss_%",
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%",
        "Predictive_Maintenance_Score"
    ]
]

sns.heatmap(
    correlation_data.corr(),
    annot=True,
    fmt=".2f"
)

plt.title("Correlation Between Network and Manufacturing Performance")
plt.show()
latency_median = df["Network_Latency_ms"].median()

low_latency = df[df["Network_Latency_ms"] <= latency_median]
high_latency = df[df["Network_Latency_ms"] > latency_median]

print("\nMedian Network Latency:")
print(latency_median)

print("\nLow Latency Group:")
print(low_latency[
    [
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean())

print("\nHigh Latency Group:")
print(high_latency[
    [
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean())
latency_median = df["Network_Latency_ms"].median()

low_latency = df[df["Network_Latency_ms"] <= latency_median]
high_latency = df[df["Network_Latency_ms"] > latency_median]

print("\nMedian Network Latency:")
print(latency_median)

print("\nLow Latency Group:")
print(low_latency[
    [
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean())

print("\nHigh Latency Group:")
print(high_latency[
    [
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean())
packet_median = df["Packet_Loss_%"].median()

low_packet_loss = df[df["Packet_Loss_%"] <= packet_median]
high_packet_loss = df[df["Packet_Loss_%"] > packet_median]

print("\nMedian Packet Loss:")
print(packet_median)

print("\nLow Packet Loss Group:")
print(low_packet_loss[
    [
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean())

print("\nHigh Packet Loss Group:")
print(high_packet_loss[
    [
        "Production_Speed_units_per_hr",
        "Quality_Control_Defect_Rate_%",
        "Error_Rate_%"
    ]
].mean())
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

monthly = df.groupby(df["Date"].dt.month).agg({
    "Network_Latency_ms": "mean",
    "Packet_Loss_%": "mean",
    "Production_Speed_units_per_hr": "mean",
    "Error_Rate_%": "mean"
})

print("\nMonthly Performance:")
print(monthly)
plt.figure(figsize=(10, 5))

plt.plot(
    monthly.index,
    monthly["Production_Speed_units_per_hr"],
    marker="o"
)

plt.title("Monthly Production Speed Trend")
plt.xlabel("Month")
plt.ylabel("Production Speed (units/hr)")
plt.xticks(range(1, 13))

plt.show()
plt.figure(figsize=(10, 5))

plt.plot(
    monthly.index,
    monthly["Network_Latency_ms"],
    marker="o"
)

plt.title("Monthly Network Latency Trend")
plt.xlabel("Month")
plt.ylabel("Network Latency (ms)")
plt.xticks(range(1, 13))

plt.show()
efficiency_summary = df.groupby("Efficiency_Status").agg({
    "Production_Speed_units_per_hr": "mean",
    "Quality_Control_Defect_Rate_%": "mean",
    "Error_Rate_%": "mean"
})

print("\nEfficiency Performance Summary:")
print(efficiency_summary)
plt.figure(figsize=(8, 5))

efficiency_order = ["Low", "Medium", "High"]

sns.barplot(
    x="Efficiency_Status",
    y="Production_Speed_units_per_hr",
    data=df,
    order=efficiency_order
)

plt.title("Production Speed by Efficiency Level")
plt.xlabel("Efficiency Status")
plt.ylabel("Average Production Speed (units/hr)")

plt.show()
plt.figure(figsize=(9, 5))

plt.scatter(
    df["Network_Latency_ms"],
    df["Production_Speed_units_per_hr"],
    alpha=0.2
)

plt.title("Network Latency vs Production Speed")
plt.xlabel("Network Latency (ms)")
plt.ylabel("Production Speed (units/hr)")

plt.show()
plt.figure(figsize=(9, 5))

plt.scatter(
    df["Packet_Loss_%"],
    df["Production_Speed_units_per_hr"],
    alpha=0.2
)

plt.title("Packet Loss vs Production Speed")
plt.xlabel("Packet Loss (%)")
plt.ylabel("Production Speed (units/hr)")

plt.show()
df["Latency_Level"] = pd.qcut(
    df["Network_Latency_ms"],
    q=3,
    labels=["Low Latency", "Medium Latency", "High Latency"]
)

latency_analysis = df.groupby("Latency_Level", observed=False).agg({
    "Production_Speed_units_per_hr": "mean",
    "Error_Rate_%": "mean",
    "Quality_Control_Defect_Rate_%": "mean"
})

print("\nPerformance by Latency Level:")
print(latency_analysis)
df["Latency_Level"] = pd.qcut(
    df["Network_Latency_ms"],
    q=3,
    labels=["Low Latency", "Medium Latency", "High Latency"]
)

latency_analysis = df.groupby("Latency_Level", observed=False).agg({
    "Production_Speed_units_per_hr": "mean",
    "Error_Rate_%": "mean",
    "Quality_Control_Defect_Rate_%": "mean"
})

print("\nPerformance by Latency Level:")
print(latency_analysis)
plt.figure(figsize=(8, 5))

sns.countplot(
    x="Efficiency_Status",
    data=df,
    order=["Low", "Medium", "High"]
)

plt.title("Manufacturing Efficiency Status Distribution")
plt.xlabel("Efficiency Status")
plt.ylabel("Number of Records")

plt.show()
plt.figure(figsize=(8, 5))

sns.boxplot(
    x="Efficiency_Status",
    y="Network_Latency_ms",
    data=df,
    order=["Low", "Medium", "High"]
)

plt.title("Network Latency by Manufacturing Efficiency")
plt.xlabel("Efficiency Status")
plt.ylabel("Network Latency (ms)")

plt.show()
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Efficiency Distribution
sns.countplot(
    x="Efficiency_Status",
    data=df,
    order=["Low", "Medium", "High"],
    ax=axes[0, 0]
)
axes[0, 0].set_title("Efficiency Status Distribution")
axes[0, 0].set_xlabel("Efficiency Status")
axes[0, 0].set_ylabel("Number of Records")

# 2. Production Speed by Efficiency
sns.barplot(
    x="Efficiency_Status",
    y="Production_Speed_units_per_hr",
    data=df,
    order=["Low", "Medium", "High"],
    ax=axes[0, 1]
)
axes[0, 1].set_title("Production Speed by Efficiency")
axes[0, 1].set_xlabel("Efficiency Status")
axes[0, 1].set_ylabel("Production Speed (units/hr)")

# 3. Network Latency by Efficiency
sns.boxplot(
    x="Efficiency_Status",
    y="Network_Latency_ms",
    data=df,
    order=["Low", "Medium", "High"],
    ax=axes[1, 0]
)
axes[1, 0].set_title("Network Latency by Efficiency")
axes[1, 0].set_xlabel("Efficiency Status")
axes[1, 0].set_ylabel("Latency (ms)")

# 4. Packet Loss vs Production Speed
axes[1, 1].scatter(
    df["Packet_Loss_%"],
    df["Production_Speed_units_per_hr"],
    alpha=0.2
)
axes[1, 1].set_title("Packet Loss vs Production Speed")
axes[1, 1].set_xlabel("Packet Loss (%)")
axes[1, 1].set_ylabel("Production Speed (units/hr)")

plt.suptitle(
    "6G Network Performance & Manufacturing Efficiency Dashboard",
    fontsize=16
)

plt.tight_layout()
plt.show()
plt.savefig("6G_Manufacturing_Dashboard.png", dpi=300, bbox_inches="tight")
plt.show()
