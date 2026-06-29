# Touchpoint Analytics: Business Intelligence Case Study

![Dashboard Preview](https://img.shields.io/badge/Status-Complete-success) ![Stack](https://img.shields.io/badge/Stack-Streamlit%20|%20DuckDB%20|%20Plotly-blue)

## 📌 Project Overview
This repository contains the solution for the **TouchPoint Consulting Junior Analyst Recruitment Case**. The objective was to analyze raw retail data for *Beverama*, the world's largest beverage producer, and extract meaningful business insights regarding their recent entry into the local market.

The solution goes beyond basic reporting by implementing a **Native ELT Pipeline (Medallion Architecture)** and an **AI-driven Executive Dashboard**.

## 🏗️ Architecture & Stack

1. **Extract, Load, Transform (ELT):** `DuckDB` (In-memory columnar SQL engine).
2. **Data Modeling:** Kimball Star Schema (Gold Layer) to optimize UI queries.
3. **Data Visualization:** `Streamlit` & `Plotly Express`.
4. **Machine Learning:** `XGBoost` for 6-month Revenue Forecasting.
5. **Documentation:** `FPDF2` for automated report generation.

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the ELT Pipeline
This script consumes the raw CSV files located in the `data/` folder and generates a highly optimized `gold_layer.duckdb` database.
```bash
python etl_pipeline.py
```

### 3. Launch the Dashboard
Run the interactive Streamlit application:
```bash
streamlit run app.py
```

## 🧠 Key Business Insights Addressed

* **Missing Master Data Strategy:** Unmapped product SKUs were intelligently absorbed into the Parent Brand ("Beverama") to preserve 100% of the C-level Revenue metrics, while flagging "⚠️ UNMAPPED (Missing SKU)" to the MDM team.
* **AI Forecasting:** An XGBoost model predicts the next 6 months of revenue, intelligently dropping incomplete periods (ML Poisoning prevention).
* **Interactive Filtering:** Slices data by Client, City, and Sub-Brand Portfolio instantly.
* **Dynamic Targets:** The KPI Gauge dynamically calculates the "All-Time Best Historic Year" based on the selected filters, challenging management to beat their records.

---
*Disclaimer: Data provided was fictional and created purely for recruitment assessment purposes.*
