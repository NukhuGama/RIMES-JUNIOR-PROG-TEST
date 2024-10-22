import requests
import time
import math
import json

"""
    Candidate Name : Simiao Salvador da Gama
    In this Test I use Free API from openweathermap.org website
"""

def find_heat_index(temperature, r_humidity):
    # Function to calculate the Heat Index
    # Temperature Degrees is in temperature Fahrenheit and relative humidity is in % as per Equation from the provided formula(the NOAA website : https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml)
    
    # Generally Temperature is in Celsius (as from openweathermap.org api) so lets converted it from Celsius to Fahrenheit

    T = temperature
    RH = r_humidity
    T = (T*(1.8)) + 32 # Convert Celsius to Fahrenheit

    # Step 1: Simple formula for HI if condition is met
    if T<80 :
        HI = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))

    # Step 2: Calculate HI using the Rothfusz regression equation
    elif T>=80:
        HI = (-42.379 
            + 2.04901523 * T 
            + 10.14333127 * RH 
            - 0.22475541 * T * RH 
            - 0.00683783 * T**2 
            - 0.05481717 * RH**2 
            + 0.00122874 * T**2 * RH 
            + 0.00085282 * T * RH**2 
            - 0.00000199 * T**2 * RH**2)
        
        # Step 3: Adjustments based on RH
        if RH < 13 and 80 <= T <= 112:
            adjustment = ((13 - RH) / 4) * math.sqrt((17 - abs(T - 95)) / 17)
            HI -= adjustment
        elif RH > 85 and 80 <= T <= 87:
            adjustment = ((RH - 85) / 10) * ((87 - T) / 5)
            HI += adjustment

    HI = (HI - 32) * (5/9) #Convert Back from Fahrenheit to Celsius
    
    # Return the Heat Index Value in Celsius
    return HI 
    
        
def fetch_weather_data():
    try:
        # fetch the geolocation data
        geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={CITY}&limit=1&appid={API_KEY}'
        geo_response = requests.get(geo_url)

        # Raise an error for bad responses
        geo_response.raise_for_status() 
        geo_data = geo_response.json()

        # Check if we got valid geolocation data
        if not geo_data:
            print("Error: No geolocation data found.")
            return None, None
        
        # Extract latitude and longitude
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Now fetch the weather data using the coordinates
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()  # Raise an error for bad responses
        weather_data = weather_response.json()
        
        # Print the entire response for debugging
        # print("API Response:")
        # print(json.dumps(weather_data, indent=2))
        # Extract temperature and humidity
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        
        return temperature, humidity
    
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None, None
    except KeyError:
        print("Error: Unexpected data format.")
        return None, None

# Main loop to fetch data every 10 minutes
def main():
    #1 minute = 60 seconds
    min = 60
    while True:
        print("Description of Temperature, Humidity and Heat Index in ", CITY, "city")
        print("=====================================================================")
        temperature, humidity = fetch_weather_data()
        # temperature, humidity = 85,12
        
        if temperature is not None and humidity is not None:
            heat_index = find_heat_index(temperature, humidity)
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Heat Index: {heat_index:.2f}°C")
        
        else:
            print("Cannot find temperature and humidity data on API")

         # Wait for 10 minutes = 600 seconds to fetch next data
        time.sleep(min*10)
        print("\n")

if __name__ == "__main__":
    # Free API Key that I created from openweathermap.org website
    API_KEY = 'a93e65ffe17782e4215c99964629cca7'
    # Please input the City or Location name that we want
    CITY = input("Please Enter The City or Location Name : ")
    main()
