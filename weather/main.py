import streamlit as st
import requests
import datetime


# Function to fetch weather data
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



def get_city_coordinates(city_name, api_key):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code == 200:
        location = geo_response.json()[0]
        return location['lat'], location['lon']
    return None, None

# def get_seven_day_forecast(lat, lon, api_key):
#     onecall_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={api_key}&units=metric"
#     response = requests.get(onecall_url)
#     if response.status_code == 200:
#         return response.json()  # Returns the 7-day forecast
#     return None
#



# Streamlit UI
def main():
    # Title of the app
    st.title("My Weather App")
    st.image("data/weather.png")
    # Ask the user for the city
    city = st.text_input("Please Enter City Name", "")

    # Access the OpenWeatherMap API key stored in Streamlit secrets
    api_key = st.secrets["api_key"]

    # When the user submits a city name
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