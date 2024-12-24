import streamlit as st
import requests


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



# Streamlit UI
def main():
    # Title of the app
    st.title("My Weather App")

    # Ask the user for the city
    city = st.text_input("Please Enter City Name", "")

    # Access the OpenWeatherMap API key stored in Streamlit secrets
    api_key = st.secrets["api_key"]

    # When the user submits a city name
    if city:
        try:
            weather_data = get_weather(city, api_key)

            # Extract relevant data
            main = weather_data["main"]
            weather = weather_data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]
            icon = weather["icon"]

            # Display weather info
            st.subheader(f"Weather in {city.capitalize()}:")
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