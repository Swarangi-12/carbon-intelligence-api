from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="Carbon Intelligence API")

#Load datasets
historical_emission = pd.read_csv('historical_co2_emission.csv')
forecast_emission = pd.read_csv('future_co2_emission.csv')
carbon_credit_price_forecast = pd.read_csv('carbon_price_forecast.csv')
historical_carbon_credit_price = pd.read_csv('historical_carbon_price.csv')

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