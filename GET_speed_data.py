import requests

# API  

station_id = 23234
api_url = f"https://tie.digitraffic.fi/api/tms/v1/stations/{station_id}/data"

# Request
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()  # Puts the json formatted data to Python object
    
# searches trough the station_data which was formed in upper code
if data:
    # Collects sensors 5056 and 5057
    speeds = []
    sensor_values = data.get('sensorValues')

    for s in sensor_values:
        if s.get('id') in (5056, 5057):
            speeds.append(s['value'])

    print("All speeds found: ", speeds)
    # Calculates mean speed, if there was sensor data
    if speeds:
        mean_speed = sum(speeds) / len(speeds)
        print(f"Mean speed at station {station_id} in last hour: {mean_speed} km/h")
    else:
        print(f"Could't find sensors 5056 and 5057 from {station_id}.")
else:
    print(f"Asemaa id:llä {station_id} ei löytynyt.")
