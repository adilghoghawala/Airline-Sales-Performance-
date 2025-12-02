# Airline Sales Performance Insights ✈️

This project analyzes **US airline route performance** using the  
**“US Airline Flight Routes and Fares 1993–2024”** dataset (Kaggle).  

The goal is to build a lightweight **commercial / revenue analytics** model that:

- Aggregates **route-level revenue** and **market size**
- Focuses on a **single carrier** (e.g. UA / DL / AA) as “our airline”
- Identifies **underperforming routes** where:
  - Our market share is low, and
  - Revenue is flat or declining over time
- Produces CSV outputs you can use for slides, dashboards, or a written strategy brief.

This is the backbone for a realistic **“Airline Sales Performance Insights Model”** project you can talk about in interviews.

---

## 📂 Project structure

```text
airline-sales-performance/
  ├─ data/
  │   └─ us-airline-flight-routes-and-fares-1993-2024.csv   # Kaggle dataset
  ├─ src/
  │   ├─ download_data.py   # optional: download from Kaggle via kagglehub
  │   └─ analysis.py        # main analysis script
  ├─ outputs/
  │   ├─ UA_route_summary.csv                # per-route metrics for our carrier
  │   └─ UA_underperforming_routes.csv       # low-share & declining routes
  ├─ requirements.txt
  ├─ INSIGHTS.md         # (optional) hand-written summary of key findings
  └─ README.md
```
## 🧱 Tech stack
- <strong>Language</strong>: Python
- <strong>Data</strong>: Kaggle - US Airline Flight Routes and Fares 1993-2024
- <strong>Libraries</strong>: pandas, numpy, kagglehub
- <strong>Outputs</strong>: Aggregated CSVs + text summary 

## ⚙️ Setup
1️⃣ Install dependencies
```text
py -m pip install -r requirements.txt
```
- requirements.txt:
```text
pandas
numpy
kagglehub    # recommended 
```

2️⃣ Get the Kaggle dataset
- Go to Kaggle: US Airline Flight Routes and Fares 1993-2024.
- Download the CSV
- Place it in the data/ folder and name it, for example
```
data/us-airline-flight-routes-and-fares-1993-2024.csv
```
- Or use download_data.py:
```text
py src/download_data.py
```

## 🧱 Conclusion
This project demonstrates:
- Building a route-level revenue & market share model from real DOT/Kaggle data
- Using Python to:
    - Aggregate large datasets to route–year level
    - Approximate market size and carrier revenue
    - Identify underperforming routes based on share + trend
- Translating outputs into data-backed commercial recommendations for:
    - Network planning
    - Revenue management
    - Sales / corporate account teams


