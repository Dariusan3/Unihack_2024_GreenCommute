import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=SmartTrafficManagement.azure-devices.net;DeviceId=traffic_light;SharedAccessKey=tI3D73JkDvkeXpfyC6oKNsEc/6XbvfjlvV6sg9fpqqg="

# Define traffic light states
TRAFFIC_LIGHT_STATES = ["Red", "Green", "Yellow"]

# Function to simulate the traffic light
def simulate_traffic_light():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    
    print("Starting traffic light simulation... Press Ctrl+C to exit.")
    try:
        while True:
            for state in TRAFFIC_LIGHT_STATES:
                # Create a message with the current state
                message = Message(state)
                message.content_type = "application/json"
                message.content_encoding = "utf-8"
                
                # Send the message to the IoT Hub
                print(f"Sending traffic light state: {state}")
                client.send_message(message)
                
                # Wait for a certain time before the next state
                time.sleep(5 if state == "Green" else 2)  # Longer for green light
    except KeyboardInterrupt:
        print("Simulation stopped.")
    finally:
        # Clean up
        client.disconnect()

# Run the simulation
simulate_traffic_light()
