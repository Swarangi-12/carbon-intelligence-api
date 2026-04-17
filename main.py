from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
import re
from typing import Any, Dict, Optional
from groq import Groq

app = FastAPI(title="Carbon Intelligence API")
class EmissionInput(BaseModel):
    current: float
    predicted: float
    country: str = "India"
    year: int = 2025

#Load datasets
historical_emission = pd.read_csv('historical_co2_emission.csv')
forecast_emission = pd.read_csv('future_co2_emission.csv')
carbon_credit_price_forecast = pd.read_csv('carbon_credit_price_forecast.csv')
historical_carbon_credit_price = pd.read_csv('historical_carbon_credit_price.csv')

@app.get('/')
def home():
    return {'message': 'Carbon Intelligence API is running'}


# CO2 Emission APIs

@app.get('/historical_emission')
def get_historical_emission():
    return historical_emission.to_dict(orient='records')

@app.get('/emission_forecast')
def get_emission_forecast():
    return forecast_emission.to_dict(orient='records')

# Carbon Price APIs

@app.get('/price_forecast')
def get_carbon_credit_price(months: int = 12):
    return carbon_credit_price_forecast.head(months).to_dict(orient='records')

@app.get('/historical__price')
def get_historical_price():
    return historical_carbon_credit_price.to_dict(orient='records')



#Integarting with Groq
import os

api_key = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY, timeout=20.0)

def generate_recommendations(
    current: float,
    predicted: float,
    country: str = "India",
    year: int = 2025,
    energy_mix: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    try:
        increase = predicted - current
        percent = (increase / current) * 100 if current else 0.0

        if energy_mix is None:
            energy_mix = {"coal": 60, "solar": 10, "gas": 20, "other": 10}

        energy_mix_str = ", ".join([f"{k}: {v}%" for k, v in energy_mix.items()])

        prompt = f"""
Write a professional insight report for a Carbon Market Intelligence Platform for {country} ({year}).
Ground the analysis in the energy mix and the emissions change.

Inputs:
- Current CO2 emissions: {current} Gt
- Predicted CO2 emissions: {predicted} Gt
- Absolute increase: {increase:.2f} Gt
- Percent increase: {percent:.2f}%
- Energy mix (approx.): {energy_mix_str}

IMPORTANT FORMATTING RULES:
- Do NOT use any markdown (no **, no ##, no *, no backticks)
- Use plain text only
- Follow this EXACT structure, no extra sections, no extra lines:
- Keep it concise for a dashboard:
  - ANALYSIS must be exactly 3 short sentences (max ~18 words each)
  - Each recommended action must be one short line (max ~14 words)
  - IMPACT NOTE must be max ~18 words
  - Total output should be under ~900 characters
  - The first sentence of ANALYSIS must explicitly mention:
    "{country}'s predicted CO2 emissions increase of {increase:.2f} Gt by {year}, representing a {percent:.2f}% rise."

SEVERITY: <one of LOW | MEDIUM | HIGH | CRITICAL>

ANALYSIS: <exactly 3 short sentences explaining why emissions are rising, grounded in the energy mix and {country} context>

RECOMMENDED ACTIONS:
1) <specific action>
2) <specific action>
3) <specific action>

IMPACT NOTE: <1 sentence describing consequences of no action>
"""

        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior carbon market + energy transition analyst. Follow the output structure exactly.",
                },
                {"role": "user", "content": prompt.strip()},
            ],
            temperature=0.3,
            max_tokens=280,
        )

        insight = (completion.choices[0].message.content or "").strip()

        # Enforce "plain text only" even if the model slips.
        if insight:
            insight = insight.replace("**", "").replace("##", "").replace("`", "")
            # Remove leading bullet markdown while preserving numbering/meaning.
            insight = re.sub(r"(?m)^\s*[\-\*]\s+", "", insight)
            # Normalize spacing: collapse 3+ newlines down to 2 newlines.
            insight = re.sub(r"\n{3,}", "\n\n", insight).strip()

        severity = "UNKNOWN"
        if insight:
            m = re.search(
                r"^\s*SEVERITY\s*:\s*(LOW|MEDIUM|HIGH|CRITICAL)\s*$",
                insight,
                flags=re.IGNORECASE | re.MULTILINE,
            )
            if m:
                severity = m.group(1).upper()

        # Fallback severity only if parsing fails (insight remains AI-generated).
        if severity == "UNKNOWN":
            if percent > 12:
                severity = "CRITICAL"
            elif percent > 8:
                severity = "HIGH"
            elif percent > 3:
                severity = "MEDIUM"
            else:
                severity = "LOW"

        return {
            "increase": round(increase, 2),
            "percent_increase": round(percent, 2),
            "severity": severity,
            "insight": insight
        }

    except Exception as e:
        return {
            "increase": round((predicted - current), 2),
            "percent_increase": round(((predicted - current) / current) * 100, 2) if current else 0.0,
            "severity": "UNKNOWN",
            "insight": f"AI generation failed: {str(e)}"
        }




# Recommendation API
@app.post('/recommend_ai')
def recommend(data: EmissionInput):
    result = generate_recommendations(        
        current=data.current,
        predicted=data.predicted,
        country=data.country,
        year=data.year
        )
    return result
