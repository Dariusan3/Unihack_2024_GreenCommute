import requests
import time
import json
from azure.iot.device import IoTHubDeviceClient, Message

# Load connection string for Azure IoT Hub
def load_connection_string(filename="primary_connection_string.txt"):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("CONNECTION_STRING="):
                return line.split("=", 1)[1].strip()

CONNECTION_STRING = load_connection_string()
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# WAQI API configuration for Timisoara
STATION_ID = "timisoara"  # Using 'timisoara' station for this example
API_URL = f"http://api.waqi.info/feed/{STATION_ID}/?token=demo"  # demo token for free access

# Function to get air quality data from WAQI API
def get_air_quality_data():
    # Make the GET request to the WAQI API
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check if the response status is 'ok'
        if data['status'] == 'ok' and 'data' in data:
            # Extract air quality components (PM2.5, CO, NO2, etc.)
            components = data['data']['iaqi']
            
            # Extract the required data (CO, NO2, PM2.5)
            co_level = components.get("co", {}).get("v", 0)  # Default to 0 if not available
            no2_level = components.get("no2", {}).get("v", 0)  # Default to 0 if not available
            pm25 = components.get("pm25", {}).get("v", 0)  # Default to 0 if not available
            
            # Format the telemetry data as per your specified format
            telemetry_data = {
                "sensorType": "AirQualitySensor",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),  # Add timestamp
                "data": {
                    "co": co_level,
                    "no2": no2_level,
                    "pm25": pm25
                }
            }
            
            return telemetry_data
        else:
            print("Error: Invalid data or station is down.")
            return None
    else:
        print(f"Failed to connect to WAQI API. HTTP Status Code: {response.status_code}")
        return None

# Function to send telemetry data to Azure IoT Hub
def send_telemetry_to_iothub():
    telemetry_data = get_air_quality_data()
    
    if telemetry_data:
        # Convert telemetry data to JSON format
        message = Message(json.dumps(telemetry_data))
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        
        # Send the message to Azure IoT Hub
        client.send_message(message)
        print(f"Sent data: {json.dumps(telemetry_data)}")
    else:
        print("No data to send.")

# Continuously send telemetry data (you can adjust the frequency)
while True:
    send_telemetry_to_iothub()
    time.sleep(8)  



# 