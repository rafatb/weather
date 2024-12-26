from weather_utility import *


def main():
    # Title of the app
    headerContainer = st.container(border=True)
    headerContainer.title("Welcome to my Weather App")
    imageCointainer = st.container(border=True)
    imageCointainer.image("data/weather5.png")

    # Ask the user for the city
    inputContainer = st.container(border=True)
    city = inputContainer.text_input("Please enter a city name to get the weather data", "")

    api_key = st.secrets["api_key"]


    if city:
        try:
            # get current weather detail
            weather_data = get_weather(city, api_key)

            # get city coordinates
            lat, lon = get_city_coordinates(city, api_key)

            # Extract current weather relevant data
            main = weather_data["main"]
            weather = weather_data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]
            icon = weather["icon"]

            # Display current weather info
            resultContainer = st.container(border=True)
            resultContainer.subheader(f"Weather in {city.capitalize()} , lat={lat} , lon={lon}:")
            resultContainer.write(f"**Temperature**: {temperature}°C")
            resultContainer.write(f"**Humidity**: {humidity}%")
            resultContainer.write(f"**Description**: {description.capitalize()}")

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
            resultContainer.image(icon_url, width=100)

            # get forcast fopr the next 3 days
            weather_data = get_forecast_data_v25(city, api_key)
            if weather_data:

                # display the 3 days forcast as line graph
                display_forecast_chart(weather_data)
        except Exception as e :
            match str(e):
                case "401":
                    st.error(f'Could not retrieve weather data for {city}, Authorization failed, \n\n Response Code {str(e)}  ')
                case "404":
                    st.error(f'Could not retrieve weather data for {city},  City not exists, \n\n Response Code {str(e)}  ')
                case _:
                    st.error(f'Could not retrieve weather data for {city}, \n\n Response Code {str(e)}  ')
if __name__ == "__main__":
    main()