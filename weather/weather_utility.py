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


def get_city_coordinates(city_name, api_key):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code == 200:
        location = geo_response.json()[0]
        return location['lat'], location['lon']
    return None, None
