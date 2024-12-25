import streamlit as st
from weather_utility import *
import datetime
import plotly.express as px

# Function to display 3-hour interval temperature chart
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

def main():
    # Title of the app
    headerContainer = st.container(border=True)
    headerContainer.title("My Weather App")
    imageCointainer = st.container(border=True)
    imageCointainer.image("data/weather5.png")

    # Ask the user for the city
    inputContainer = st.container(border=True)
    city = inputContainer.text_input("Please enter a city name to get the weather data", "")
    api_key = st.secrets["api_key"]


    if city:
        try:
            weather_data = get_weather(city, api_key)
            lat, lon = get_city_coordinates(city, api_key)

            # Extract relevant data
            main = weather_data["main"]
            weather = weather_data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]
            icon = weather["icon"]

            # Display weather info
            resultContainer = st.container(border=True)
            resultContainer.subheader(f"Weather in {city.capitalize()} , lat={lat} , lon={lon}:")
            resultContainer.write(f"**Temperature**: {temperature}°C")
            resultContainer.write(f"**Humidity**: {humidity}%")
            resultContainer.write(f"**Description**: {description.capitalize()}")

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
            resultContainer.image(icon_url, width=100)

            weather_data = get_forecast_data_v25(city, api_key)
            if weather_data:
                display_forecast_chart(weather_data)
        except Exception as e :
            match str(e):
                case "401":
                    st.error(f'Could not retrieve weather data for {city}, Authorization failed, \n\n Response Code {str(e)}  ')
                case "404":
                    st.error(f'Could not retrieve weather data for {city},  City not exists, \n\n Response Code {str(e)}  ')
                case _:
                    st.error(f'Could not retrieve weather data for {city}, \n\n Response Code {str(e)}  ')
    # else:
    #     st.info("Please enter a city name to get the weather data.")

if __name__ == "__main__":
    main()