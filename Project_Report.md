# 6G Manufacturing Analytics

## 1. Introduction

Smart manufacturing systems rely on connected machines, real-time data, and reliable communication networks to maintain efficient production. With the development of Industry 4.0 and emerging 6G technologies, network performance can play an important role in smart-factory operations.

This project analyzes manufacturing data to investigate the relationship between network performance and production efficiency. The analysis focuses mainly on network latency, packet loss, production speed, and efficiency status.

An interactive Streamlit dashboard was developed to visualize these relationships and provide insights into manufacturing performance across different machines and efficiency levels.

## 2. Problem Statement

In a smart-factory environment, network issues such as latency and packet loss may affect communication between machines and manufacturing systems. However, it is important to determine whether these network-performance factors actually have a measurable relationship with production performance.

This project aims to analyze the available manufacturing data and determine how network latency and packet loss relate to production speed and manufacturing efficiency.

## 3. Objectives

- Analyze manufacturing efficiency across different efficiency levels.
- Examine the relationship between network latency and production speed.
- Examine the relationship between packet loss and production speed.
- Compare production speed across Low, Medium, and High efficiency levels.
- Provide interactive machine-level and efficiency-level analysis.
- Develop an interactive dashboard for visualizing the results.
## 4. Dataset Description

The dataset used for this project is `Thales_Group_Manufacturing.csv`.

The dataset contains 100,000 manufacturing records and provides information
about machine operations, network performance, production performance, and
manufacturing efficiency.

### Dataset Features

| Feature | Description |
|---|---|
| Date | Date of the manufacturing record |
| Timestamp | Time of the recorded operation |
| Machine_ID | Identifier of the manufacturing machine |
| Operation_Mode | Operating mode of the machine |
| Temperature_C | Machine temperature in Celsius |
| Vibration_Hz | Machine vibration measurement |
| Power_Consumption_kW | Power consumed by the machine |
| Network_Latency_ms | Network latency in milliseconds |
| Packet_Loss_% | Percentage of network packet loss |
| Quality_Control_Defect_Rate_% | Percentage of quality-control defects |
| Production_Speed_units_per_hr | Production speed in units per hour |
| Predictive_Maintenance_Score | Predictive maintenance score |
| Error_Rate_% | Machine or production error rate |
| Efficiency_Status | Manufacturing efficiency classification |

### Efficiency Distribution

The dataset contains three efficiency categories:

- Low: 77,825 records
- Medium: 19,189 records
- High: 2,986 records

The dashboard uses these efficiency categories to compare network
performance and production speed.
## 5. Methodology

The project follows a data analysis and visualization workflow to study
the relationship between network performance and manufacturing efficiency.

### Step 1: Data Loading

The manufacturing dataset was loaded using the Pandas library.

### Step 2: Data Preparation

The dataset was examined for its structure, column names, data types, and
missing values. The analysis used the relevant network and manufacturing
performance variables.

### Step 3: Data Filtering

Interactive filters were implemented in the Streamlit dashboard to allow
users to analyze the data based on:

- Efficiency Status
- Machine ID

The dashboard updates the displayed metrics and visualizations according
to the selected filters.

### Step 4: Exploratory Data Analysis

The following metrics were analyzed:

- Efficiency Status distribution
- Average Network Latency by Efficiency
- Average Packet Loss by Efficiency
- Average Production Speed by Efficiency

### Step 5: Correlation Analysis

Correlation analysis was performed to examine the linear relationship
between:

- Network Latency and Production Speed
- Packet Loss and Production Speed

Correlation values were displayed in the dashboard along with trend lines
on the scatter plots.

### Step 6: Data Visualization

Matplotlib and Seaborn were used to create bar charts and scatter plots
for visual analysis.

### Step 7: Dashboard Development

An interactive dashboard was developed using Streamlit. The dashboard
combines KPIs, filters, charts, correlation analysis, key findings, and
the final conclusion in a single interface.
## 6. Data Analysis & Visualization

The dashboard provides several visualizations to analyze manufacturing
efficiency and network performance.

### 6.1 Efficiency Status Distribution

The efficiency distribution shows that most records belong to the Low
efficiency category, followed by Medium and High efficiency.

- Low Efficiency: 77,825 records
- Medium Efficiency: 19,189 records
- High Efficiency: 2,986 records

This indicates that the majority of observations in the dataset are
classified as Low efficiency.

### 6.2 Average Network Latency by Efficiency

The average network latency was compared across the three efficiency
categories.

The average latency values are approximately:

- High Efficiency: 25.33 ms
- Medium Efficiency: 25.57 ms
- Low Efficiency: 25.56 ms

The values are very close to each other, suggesting that average network
latency does not vary substantially across the efficiency categories.

### 6.3 Average Packet Loss by Efficiency

Average packet loss was also compared across efficiency levels.

The average packet loss values are approximately:

- High Efficiency: 2.528%
- Medium Efficiency: 2.487%
- Low Efficiency: 2.494%

The differences are relatively small across the efficiency categories.

### 6.4 Average Production Speed by Efficiency

Production speed shows a much clearer difference across efficiency levels.

The average production speeds are approximately:

- High Efficiency: 450.79 units/hr
- Medium Efficiency: 334.13 units/hr
- Low Efficiency: 254.85 units/hr

High-efficiency operations therefore show substantially higher average
production speed than Medium- and Low-efficiency operations.

### 6.5 Network Latency vs Production Speed

A scatter plot and trend line were used to analyze the relationship between
network latency and production speed.

The correlation is approximately:

**-0.001**

This value is very close to zero, indicating a negligible linear
relationship between network latency and production speed in the analyzed
dataset.

### 6.6 Packet Loss vs Production Speed

A scatter plot and trend line were also used to analyze packet loss against
production speed.

The correlation is approximately:

**-0.007**

This value is also very close to zero, indicating a negligible linear
relationship between packet loss and production speed in the analyzed
dataset.
## 7. Key Findings

The analysis of the manufacturing dataset produced the following key
findings:

- High-efficiency operations have a substantially higher average
  production speed than Medium- and Low-efficiency operations.

- The average network latency is very similar across the Low, Medium,
  and High efficiency categories.

- Average packet loss also shows only small differences across the
  efficiency categories.

- Network latency has a correlation of approximately -0.001 with
  production speed, indicating a negligible linear relationship.

- Packet loss has a correlation of approximately -0.007 with production
  speed, also indicating a negligible linear relationship.

- The results suggest that manufacturing efficiency is influenced by
  multiple operational factors and cannot be explained by network
  performance alone.

- Interactive filtering by Efficiency Status and Machine ID allows users
  to examine the manufacturing data at different levels of detail.
  ## 8. Conclusion

This project analyzed the relationship between network performance and
manufacturing efficiency using a dataset of 100,000 manufacturing records.

The analysis shows that high-efficiency operations are associated with
higher production speeds compared with Medium- and Low-efficiency
operations.

However, network latency and packet loss show negligible linear
relationships with production speed, with correlation values of
approximately -0.001 and -0.007 respectively.

These results indicate that manufacturing efficiency is influenced by
multiple operational factors rather than network performance alone.

The interactive Streamlit dashboard provides a practical way to explore
these relationships through visualizations, correlation analysis, and
filters based on Efficiency Status and Machine ID.
## 9. Future Scope

The project can be further improved by adding advanced analytics and
real-time monitoring capabilities.

Possible future improvements include:

- Developing machine-learning models to predict manufacturing efficiency.
- Adding predictive maintenance analysis for individual machines.
- Performing time-series analysis to identify changes in network and
  production performance over time.
- Adding real-time network monitoring for latency and packet loss.
- Including additional operational factors such as temperature, vibration,
  power consumption, and error rate in the analysis.
- Developing more advanced statistical analysis to investigate non-linear
  relationships between network performance and manufacturing efficiency.
- Deploying the dashboard for real-time smart-factory monitoring.
