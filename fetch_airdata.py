import requests
import csv
import os
from datetime import datetime

# Read more from
# https://aqicn.org/api/
# https://aqicn.org/data-platform/register/
# https://aqicn.org/historical/#city:bangkok

# Replace with your API key
API_KEY = "e9e7fb50ce278cd6ecd386a1699bb363127ffad3"
# API_KEY = os.getenv("API_KEY")

# List of cities
cities = ["Samut Prakan", "Nakhon Ratchasima", "Surin", "Sakon Nakhon", "Mueang Khon Kaen", "Nong Khai", "Kanchanaburi", "Suphan Buri", "Uthai Thani", "Nakhon Sawan", 
          "Phitsanulok", "Kamphaeng Phet", "Lamphun", "Lampang", "Phayao", "Bangkok", "Trat", "Nonthaburi", "Nan", "Ubon Ratchathani", "Samut Sakhon", 
          "Chiang Mai", "Mueang Chiang Rai", "Ayutthaya", "Uttaradit", "Rayong", "Pathum Thani", "Chonburi", "Nakhon Pathom", "Ratchaburi", "Phuket", 
          "Yala", "Krabi", "Trang", "Satun", "Pattani", "Narathiwat", "Prachuap Khiri Khan", "Saraburi",
         ]

# CSV File Name
CSV_FILE = "thai_air_data.csv"

def fetch_pm25_data(city):
    """
    Fetch PM2.5 data for a given city from the AQICN API.
    """
    api_url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if data["status"] == "ok":
            return data["data"]
        else:
            print(f"Error fetching data for {city}: {data['data']}")
            return None

    except Exception as e:
        print(f"Failed to retrieve data for {city}: {e}")
        return None

def save_to_csv(data, filename):
    """
    Save the fetched data to a CSV file.
    """
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header if file is newly created
        if not file_exists:
            writer.writerow(["Timestamp", "City", "AQI", "PM2.5", "JSON"])

        writer.writerow(data)

if __name__ == "__main__":
    for city in cities:
        pm25_data = fetch_pm25_data(city)
        aqi = pm25_data.get("aqi", "N/A")
        pm25 = pm25_data.get("iaqi", {}).get("pm25", {}).get("v", "N/A")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if pm25_data:
            save_to_csv([timestamp, city, aqi, pm25, pm25_data], CSV_FILE)
            print(f"Data saved for {city}: {pm25_data}")
