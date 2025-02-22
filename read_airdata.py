import re
import pandas as pd
import json
import numpy as np

# CSV File Name
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