# -*- coding: utf-8 -*-
"""code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14G9L61bDZNvnkAwZBa0_YSX6EY3MfUyr
"""


import os
os.system("pip install streamlit")


import streamlit as st
import requests
from datetime import datetime

# ✅ Your WeatherAPI key
API_KEY = "c81b89c0b3d2af0b038127b24b6a4732"
BASE_URL = "http://api.weatherapi.com/v1"

st.title("🌤️ Weather Forecast App")

# --- Inputs ---
city = st.text_input("Enter City", "New York")
date_input = st.text_input("Enter Date (YYYY-MM-DD)", datetime.today().strftime("%Y-%m-%d"))

if st.button("Get Weather"):

    try:
        # Parse input date
        user_date = datetime.strptime(date_input, "%Y-%m-%d")
        today = datetime.now()

        # Choose endpoint based on date
        if user_date.date() < today.date():
            endpoint = "history.json"
        elif user_date.date() == today.date():
            endpoint = "current.json"
        else:
            endpoint = "forecast.json"

        # Set up request parameters
        params = {
            "key": API_KEY,
            "q": city,
            "dt": user_date.strftime("%Y-%m-%d")
        }

        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        data = response.json()

        # Handle response
        if "error" in data:
            st.error(data["error"]["message"])

        elif endpoint == "current.json":
            current = data["current"]
            st.subheader("📍 Current Weather")
            st.write(f"Condition: {current['condition']['text']}")
            st.write(f"Temperature: {current['temp_c']} °C")
            st.write(f"Humidity: {current['humidity']}%")

        elif endpoint == "history.json":
            day = data["forecast"]["forecastday"][0]["day"]
            st.subheader("📍 Historical Weather")
            st.write(f"Avg Temp: {day['avgtemp_c']} °C")
            st.write(f"Condition: {day['condition']['text']}")

        elif endpoint == "forecast.json":
            day = data["forecast"]["forecastday"][0]["day"]
            st.subheader("📍 Forecasted Weather")
            st.write(f"Max Temp: {day['maxtemp_c']} °C")
            st.write(f"Min Temp: {day['mintemp_c']} °C")
            st.write(f"Condition: {day['condition']['text']}")

    except Exception as e:
        st.error(f"Error: {e}")
