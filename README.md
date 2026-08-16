 📡 Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories

 📌 Project Overview

This project analyzes the relationship between network performance and manufacturing efficiency in a smart factory environment.

The analysis focuses mainly on **Network Latency** and **Packet Loss** and examines how these network parameters relate to production speed, error rate, quality defects, and overall manufacturing efficiency.

The objective is to understand whether network performance has a measurable impact on smart-factory operations and to identify useful insights for manufacturing decision-making.

---

## 🎯 Business Problem

Modern smart factories depend on reliable and fast communication between machines, sensors, control systems, and data-driven applications.

Network issues such as high latency and packet loss may potentially affect manufacturing operations.

This project investigates:

- How network latency varies across efficiency levels
- How packet loss varies across efficiency levels
- Whether network latency is related to packet loss
- How production speed differs across efficiency levels
- How error rates and quality defects vary with efficiency
- Whether network performance alone can explain manufacturing efficiency

---

## 📊 Dataset

The dataset contains:

- **100,000 records**
- **14 columns**
- Machine, manufacturing, network, quality, and efficiency information

### Important Variables

| Variable | Description |
|---|---|
| Date | Manufacturing date |
| Timestamp | Time of observation |
| Machine_ID | Machine identifier |
| Operation_Mode | Machine operating mode |
| Temperature_C | Machine temperature |
| Vibration_Hz | Machine vibration |
| Power_Consumption_kW | Power consumption |
| Network_Latency_ms | Network latency |
| Packet_Loss_% | Network packet loss |
| Quality_Control_Defect_Rate_% | Quality defect rate |
| Production_Speed_units_per_hr | Production speed |
| Predictive_Maintenance_Score | Predictive maintenance score |
| Error_Rate_% | Manufacturing error rate |
| Efficiency_Status | Manufacturing efficiency category |

---

## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- VS Code
- Git
- GitHub

---

## 🔍 Analysis Performed

### 1. Data Understanding

- Dataset shape
- Column names
- Data types
- Missing-value analysis
- Initial dataset inspection

### 2. Efficiency Analysis

- Efficiency status distribution
- Efficiency percentage
- Production speed by efficiency
- Error rate by efficiency
- Quality defect rate by efficiency

### 3. Network Performance Analysis

- Average network latency by efficiency
- Average packet loss by efficiency
- Network latency vs efficiency
- Packet loss vs production speed
- Correlation between latency and packet loss
- Low vs high latency comparison
- Low vs high packet-loss comparison

### 4. Time-Based Analysis

- Monthly network performance
- Monthly production performance
- Monthly error-rate analysis

### 5. Data Visualization

The project includes visualizations for:

- Efficiency distribution
- Production speed by efficiency
- Network latency by efficiency
- Network performance comparisons
- Packet loss vs production speed
- Overall manufacturing performance

---

## 📈 Key Findings

### Manufacturing Efficiency

Production performance differs significantly across efficiency categories.

| Efficiency Status | Avg. Production Speed | Avg. Error Rate |
|---|---:|---:|
| High | 450.79 units/hr | 1.01% |
| Medium | 334.13 units/hr | 2.73% |
| Low | 254.85 units/hr | 8.93% |

High-efficiency records have substantially higher production speeds and lower error rates compared with low-efficiency records.

### Network Latency

Average network latency was approximately **25.5 ms** across the efficiency categories.

The difference between the efficiency groups was relatively small.

### Packet Loss

Average packet loss was approximately **2.5%** across the efficiency categories.

### Latency and Packet Loss Correlation

The correlation between network latency and packet loss was:

**-0.0069**

This indicates an extremely weak relationship between these two network variables in this dataset.

### Network Performance Impact

The low-vs-high latency and packet-loss comparisons showed only small differences in average production speed.

Therefore, the analysis does **not** provide strong evidence that network latency or packet loss alone determines manufacturing efficiency.

Other manufacturing and operational factors may have a stronger influence.

---

## 💡 Business Recommendations

1. **Monitor network performance continuously**  
   Smart factories should monitor latency and packet loss together with production KPIs.

2. **Do not rely on network metrics alone**  
   Manufacturing efficiency should be evaluated using network, machine, operational, and quality variables together.

3. **Monitor production and error rates**  
   Production speed and error rate show strong differences across efficiency categories.

4. **Combine network and machine analytics**  
   Future systems can combine network telemetry with machine-condition and production data.

5. **Use predictive analytics**  
   Machine-learning models can be developed in the future to identify complex relationships between network conditions and manufacturing efficiency.

---

📊 Dashboard

The project includes a dashboard containing important manufacturing and network-performance visualizations.

![6G Manufacturing Analytics Dashboard](6G_Manufacturing_Dashboard.png)

---


## 📁 Project Structure

```text
6G_Manufacturing_Analytics/
├── .gitignore
├── 6G_Manufacturing_Dashboard.png
├── Project_Report.md
├── README.md
├── Thales_Group_Manufacturing.csv
├── analysis.py
└── dashboard.py
