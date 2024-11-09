from pymongo import MongoClient, errors
import json

try:
    # Step 1: Load MongoDB connection details from 'mongo_connection.json'
    # with open('mongo_connection.json') as file:
        # config = json.load(file)

    # Extract connection details
    connection_string = "mongodb+srv://dariusosadici:Parola0509@monitoring-cluster.qm4du.mongodb.net/?retryWrites=true&w=majority&appName=Monitoring-Cluster"
    database_name = "GreenCommuteDB"
    collection_name = "SensorReadings"

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
            with open('../SimulatedDevices/Air_Quality_Sensor_Simulation/air_quality_sensor_data.json') as data_file:
                data = json.load(data_file)
            print("Data loaded from JSON file successfully.")
        except FileNotFoundError:
            print("Data JSON file not found. Please check the file path.")
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
