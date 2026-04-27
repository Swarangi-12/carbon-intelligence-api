from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
import re
from typing import Any, Dict, Optional
from groq import Groq

app = FastAPI(title="Carbon Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

groq_client = Groq(api_key=api_key, timeout=20.0)

def generate_recommendations(
    current: float,
    predicted: float,
    country: str = "India",
    year: int = 2025,
) -> Dict[str, Any]:
    try:
        increase = predicted - current
        percent = (increase / current) * 100 if current else 0.0


        prompt = f"""
You are a senior climate policy analyst writing for a Carbon Market Intelligence dashboard.
Analyze the following CO2 emission forecast data for {country} and generate a structured insight report.

Emission Data:
- Country: {country}
- Year: {year}
- Current CO2 emissions: {current} Gt
- Predicted CO2 emissions: {predicted} Gt
- Absolute increase: {increase:.2f} Gt
- Percent increase: {percent:.2f}%

Your job:
1. Determine severity based on your expert analysis of:
   - The percent increase in context of {country}'s current development stage
   - How this trajectory compares to global climate targets (1.5°C pathway)
   - Whether this rise is sudden or part of a gradual trend
   - The urgency of intervention needed

2. Write the report in this EXACT structure with no deviations:

SEVERITY: <LOW | MEDIUM | HIGH | CRITICAL>

ANALYSIS:
Sentence 1: State the exact emission figures and percent rise for {country} in {year}.
Sentence 2: Identify the most likely cause of this rise based on {country}'s known energy and industrial patterns.
Sentence 3: Explain what this means for {country}'s climate targets or commitments.

RECOMMENDED ACTIONS:
1) <Most impactful action specific to {country}'s situation>
2) <Policy or infrastructure action to address root cause>
3) <Monitoring or efficiency measure for near-term impact>

IMPACT NOTE: <What happens specifically to {country} if no action is taken in 2 years>

STRICT RULES:
- Plain text only, zero markdown (no **, no ##, no *, no backticks)
- No extra sections, no greetings, no disclaimers
- Every sentence must be specific to {country}, not generic
- Max 18 words per sentence in ANALYSIS
- Max 14 words per recommended action
- Max 18 words in IMPACT NOTE
- Do not repeat the same word or phrase twice in the output
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
