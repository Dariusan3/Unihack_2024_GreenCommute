import sys
import json
from pymongo import MongoClient, errors

try:
    # Step 1: Get collection_name from the first command line argument
    if len(sys.argv) < 2:
        raise ValueError("Collection name is missing. Please provide it as the first argument.")
    
    collection_name = sys.argv[1]

    # Set the path to the JSON file based on the collection name
    if collection_name == "SensorReadings":
        json_file_path = "../SimulatedDevices/Air_Quality_Sensor_Simulation/air_quality_sensor_data.json"
    elif collection_name == "OptimalRouteResults":
        json_file_path = "optimal_route_results.json"
    else:
        raise ValueError("Unsupported collection name. Please use 'SensorReadings' or 'OptimalRouteResults'.")

    # MongoDB connection details
    connection_string = "mongodb+srv://dariusosadici:Parola0509@monitoring-cluster.qm4du.mongodb.net/?retryWrites=true&w=majority&appName=Monitoring-Cluster&tls=true&tlsAllowInvalidCertificates=true"
    database_name = "GreenCommuteDB"

    # Verify if essential connection details are present
    if not all([connection_string, database_name, collection_name]):
        raise ValueError("Missing essential connection information in mongo_connection.json.")

    # Step 2: Connect to MongoDB
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
        client.admin.command('ping')  # Try to ping the server to check the connection
        print("Successfully connected to MongoDB!")
    except errors.ServerSelectionTimeoutError as err:
        print(f"Failed to connect to MongoDB: {err}")
        client = None

    # Proceed only if the connection is successful
    if client:
        db = client[database_name]
        collection = db[collection_name]

        # Step 3: Load data from the JSON file
        try:
            with open(json_file_path) as data_file:
                data = json.load(data_file)
            print("Data loaded from JSON file successfully.")
        except FileNotFoundError:
            print(f"Data JSON file not found at {json_file_path}. Please check the file path.")
            data = None
        except json.JSONDecodeError:
            print("Error decoding JSON. Please ensure the JSON file is valid.")
            data = None

        # Step 4: Insert data into MongoDB
        if data:
            try:
                if isinstance(data, list):
                    collection.insert_many(data)
                    print("List of documents successfully inserted into MongoDB!")
                else:
                    collection.insert_one(data)
                    print("Single document successfully inserted into MongoDB!")
            except errors.PyMongoError as e:
                print(f"Error inserting data into MongoDB: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
