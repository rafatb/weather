import streamlit as st
from weather_utility import *

def main():
    # Title of the app
    st.title("My Weather App")
    st.image("data/weather.png")

    # Ask the user for the city
    city = st.text_input("Please Enter City Name", "")
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
            st.subheader(f"Weather in {city.capitalize()} , lat={lat} , lon={lon}:")
            st.write(f"**Temperature**: {temperature}°C")
            st.write(f"**Humidity**: {humidity}%")
            st.write(f"**Description**: {description.capitalize()}")

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
            st.image(icon_url, width=100)

        except Exception as e :
            match str(e):
                case "401":
                    st.error(f'Could not retrieve weather data for {city}, Authorization failed, \n\n Response Code {str(e)}  ')
                case "404":
                    st.error(f'Could not retrieve weather data for {city},  City not exists, \n\n Response Code {str(e)}  ')
                case _:
                    st.error(f'Could not retrieve weather data for {city}, \n\n Response Code {str(e)}  ')
    else:
        st.info("Please enter a city name to get the weather data.")


if __name__ == "__main__":
    main()