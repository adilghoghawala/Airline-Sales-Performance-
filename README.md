# Airline-Sales-Performance-
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

## 🧱 Tech stack
- <strong>Language<strong>: Python