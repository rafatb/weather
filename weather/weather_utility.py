import requests
import datetime
import plotly.express as px
import streamlit as st


# Function to fetch the current weather data
def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    # Construct the URL with the city and API key
    url = f"{base_url}?q={city}&appid={api_key}&units=metric"

    # Send the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)

# fetch the next 3 days forcast with 3 hours intervals
def get_forecast_data_v25(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"HTTP error occurred: {err}")
    except Exception as err:
        raise Exception(f"Error occurred: {err}")

# get city coordinates
def get_city_coordinates(city_name, api_key):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code == 200:
        location = geo_response.json()[0]
        return location['lat'], location['lon']
    return None, None

# Function to display 3-hour interval temperature chart for the next 3 days
def display_forecast_chart(weather_data):
    if weather_data and 'list' in weather_data:
        forecast_list = weather_data['list'][:24]  # Limit to 24 intervals (3-hour each)
        times = []
        temperatures = []

        for forecast in forecast_list:
            timestamp = forecast['dt']
            temp = forecast['main']['temp']

            time = datetime.datetime.fromtimestamp(timestamp)

            times.append(time)
            temperatures.append(temp)

        # Create a line chart using Plotly
        fig = px.line(x=times, y=temperatures, labels={'x': 'Time', 'y': 'Temperature (°C)'}, title='3-Hour Interval Temperature Forecast')
        plotlyContainer = st.container(border=True)
        plotlyContainer.plotly_chart(fig)
