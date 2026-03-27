# 🌍 Carbon Intelligence Platform

A data-driven project that analyzes global energy consumption, CO₂ emissions, and predicts carbon credit prices using machine learning and time-series forecasting.

---

## 🚀 Project Overview

This project aims to understand the relationship between energy consumption and carbon emissions, and to forecast carbon credit prices using historical data.

It combines:
- 📊 Data Analysis (Energy & Emissions)
- 🤖 Machine Learning (Time Series Forecasting)
- 🌐 API Development (FastAPI)
- 📈 Dashboard Integration (Frontend)

---

## 🎯 Objectives

- Analyze global energy consumption patterns
- Understand the impact of fossil fuels on CO₂ emissions
- Forecast future CO₂ emissions
- Predict carbon credit prices
- Build a backend API for real-time data access
- Integrate with a frontend dashboard

---

## 🧠 Key Insights

- Fossil fuels (coal, oil, gas) dominate energy consumption
- Increasing energy demand leads to rising CO₂ emissions
- Carbon credit markets are essential to control emissions
- Carbon credit prices can be forecasted using time-series models

---

## 🧩 Project Structure

```
carbon-intelligence-api/
│
├── main.py                          # FastAPI backend
├── requirements.txt                # Dependencies
│
├── historical_co2_emission.csv
├── future_co2_emission.csv
├── carbon_credit_price_forecast.csv
├── historical_carbon_credit_price.csv
│
└── README.md
```

---

## ⚙️ Technologies Used

- Python 🐍
- FastAPI ⚡
- Pandas 📊
- Prophet (for forecasting) 📈
- Matplotlib (for visualization)
- React (Frontend Dashboard)

---

## 📊 Analysis Performed

### 1️⃣ Energy Consumption Analysis
- Source-wise energy usage (coal, oil, gas, renewables)
- Insight: Fossil fuels dominate global energy consumption

### 2️⃣ CO₂ Emissions Forecasting
- Time-series forecasting using Prophet
- Predicts future emission trends

### 3️⃣ Carbon Credit Price Prediction
- Log transformation + Prophet model
- Outputs:
  - Predicted price
  - Confidence range
  - Trend direction

---

## 🔗 API Endpoints

Base URL:
```
https://carbon-intelligence-api.onrender.com
```

### 📊 CO₂ Emissions

- `/emissions` → Historical emissions  
- `/emissions-forecast` → Future emissions  

### 💰 Carbon Credit Prices

- `/price-history` → Historical prices  
- `/price-forecast` → Predicted prices  

---

## 🧪 Example API Usage

```javascript
axios.get("https://carbon-intelligence-api.onrender.com/price-forecast")
  .then(res => console.log(res.data));
```

---

## 📈 Dashboard Integration

The frontend dashboard consumes API data and displays:

- CO₂ emission trends
- Carbon credit price forecasts
- Fuel consumption analysis (charts/images)

---

## 🔄 How It Works

```
Data → Model → API → Frontend Dashboard
```

1. Data is cleaned and processed  
2. ML models generate forecasts  
3. FastAPI exposes endpoints  
4. Frontend fetches and visualizes data  

---

## 📌 Key Concepts

- **Carbon Credit** = Permission to emit 1 tonne of CO₂  
- Price Unit = € per tonne CO₂  

---

## ⚠️ Limitations

- Forecasts depend on historical trends
- External factors (policy, economy) not included
- Render free tier may have cold start delay

---

## 🚀 Future Improvements

- Add real-time data updates
- Improve model accuracy with external features
- Convert static charts to interactive visualizations
- Deploy frontend publicly

---

## 👩‍💻 Contributors

- Swarangi Shingote — Backend, ML, API  
- Rutuja Pandhare — Frontend, Dashboard  

---

## 📢 Conclusion

This project demonstrates how data science and web technologies can be combined to analyze environmental trends and support decision-making in carbon markets.

---

## ⭐ Final Note

This is a full-stack data science project involving:
- Data analysis  
- Machine learning  
- API development  
- Frontend integration  

```
From raw data → to live deployed system 🌐
```

---
