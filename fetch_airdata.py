import requests
import csv
import os
from datetime import datetime
import re
import pandas as pd
import json
import numpy as np


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

    CSV_FILE = "thai_air_data.csv"
    df = pd.read_csv(CSV_FILE)
    json_object = json.loads(df['JSON'].iloc[0].replace('\'','"'))
    df['JSON'] = df['JSON'].apply(lambda x: json.loads(x.replace('\'','"')))
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['geo'] = df['JSON'].apply(lambda x: x['city'].get('geo', np.nan))
    df['lat'] = df['geo'].apply(lambda x: x[0] if x is not np.nan else np.nan).astype(float)
    df['lon'] = df['geo'].apply(lambda x: x[1] if x is not np.nan else np.nan).astype(float)
    df['name'] = df['JSON'].apply(lambda x: x['city'].get('name', np.nan))
    df['co'] = df['JSON'].apply(lambda x: x['iaqi'].get('co', {'v':np.nan})['v']).astype(float)
    df['dew'] = df['JSON'].apply(lambda x: x['iaqi'].get('dew', {'v':np.nan})['v']).astype(float)
    df['h'] = df['JSON'].apply(lambda x: x['iaqi'].get('h', {'v':np.nan})['v']).astype(float)
    df['no2'] = df['JSON'].apply(lambda x: x['iaqi'].get('no2', {'v':np.nan})['v']).astype(float)
    df['o3'] = df['JSON'].apply(lambda x: x['iaqi'].get('o3', {'v':np.nan})['v']).astype(float)
    df['p'] = df['JSON'].apply(lambda x: x['iaqi'].get('p', {'v':np.nan})['v']).astype(float)
    df['pm10'] = df['JSON'].apply(lambda x: x['iaqi'].get('pm10', {'v':np.nan})['v']).astype(float)
    df['pm25'] = df['JSON'].apply(lambda x: x['iaqi'].get('pm25', {'v':np.nan})['v']).astype(float)
    df['r'] = df['JSON'].apply(lambda x: x['iaqi'].get('r', {'v':np.nan})['v']).astype(float)
    df['so2'] = df['JSON'].apply(lambda x: x['iaqi'].get('so2', {'v':np.nan})['v']).astype(float)
    df['t'] = df['JSON'].apply(lambda x: x['iaqi'].get('t', {'v':np.nan})['v']).astype(float)
    df['w'] = df['JSON'].apply(lambda x: x['iaqi'].get('w', {'v':np.nan})['v']).astype(float)
    df['s'] = df['JSON'].apply(lambda x: x['time'].get('s', np.nan))
    df['s'] = pd.to_datetime(df['s'])
    df['tz'] = df['JSON'].apply(lambda x: x['time'].get('tz', np.nan))
    df['tz'] = df['tz'].apply(lambda x: re.match(r'\+([0-9])+:[0-9]{2}',x).group(1) if x is not np.nan else np.nan).astype(int)
    df['time'] = df['s'] + pd.to_timedelta(df['tz'], unit='h')

    df = df[['Timestamp', 'City', 'name', 'lat', 'lon', 'co', 'dew', 'h', 'no2', 'o3', 'p', 'pm10', 'pm25', 'r', 'so2', 't', 'w', 'time']]
    df = df.drop_duplicates(subset=['City', 'name', 'lat', 'lon', 'co', 'dew', 'h', 'no2', 'o3', 'p', 'pm10', 'pm25', 'r', 'so2', 't', 'w', 'time'])
    df.to_csv('thai_air_data_cleaned.csv', index=False)