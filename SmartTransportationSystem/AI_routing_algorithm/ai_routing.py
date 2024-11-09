import pandas as pd
import numpy as np
import json
from sklearn.linear_model import LinearRegression

# Load air quality data from the JSON file
with open('air_quality_PROC.json', 'r') as file:
    air_quality_data = json.load(file)

# Collect pollutant data for all entries to calculate average air quality levels
co_levels = []
no2_levels = []
pm25_levels = []

for entry in air_quality_data:
    co_levels.append(entry['data']['co'])
    no2_levels.append(entry['data']['no2'])
    pm25_levels.append(entry['data']['pm25'])

# Calculate average values for CO, NO2, and PM2.5
avg_co = np.mean(co_levels)
avg_no2 = np.mean(no2_levels)
avg_pm25 = np.mean(pm25_levels)

# Sample traffic and speed data for intersections
traffic_data = {
    'Intersection A': {'traffic_volume': 30, 'average_speed': 50},
    'Intersection B': {'traffic_volume': 50, 'average_speed': 60},
    'Intersection C': {'traffic_volume': 40, 'average_speed': 45},
    'Intersection D': {'traffic_volume': 20, 'average_speed': 55}
}

# Define the graph representing the road network (distances between intersections)
graph = {
    'Intersection A': {'Intersection B': 5, 'Intersection C': 10, 'Intersection D': 8},
    'Intersection B': {'Intersection A': 5, 'Intersection C': 4, 'Intersection D': 7},
    'Intersection C': {'Intersection A': 10, 'Intersection B': 4, 'Intersection D': 6},
    'Intersection D': {'Intersection A': 8, 'Intersection B': 7, 'Intersection C': 6}
}

# Training sample data for Linear Regression model
# This data should ideally come from historical route performance data
# Features: [Traffic Volume, 1/Avg Speed, CO, NO2, PM2.5]
# Target: Weight (cost or time)

training_data = [
    [30, 1 / 50, avg_co, avg_no2, avg_pm25, 1.5],
    [50, 1 / 60, avg_co, avg_no2, avg_pm25, 2.0],
    [40, 1 / 45, avg_co, avg_no2, avg_pm25, 1.8],
    [20, 1 / 55, avg_co, avg_no2, avg_pm25, 1.2]
]

# Separate features and target
X_train = [entry[:5] for entry in training_data]  # Features
y_train = [entry[5] for entry in training_data]   # Target

# Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Function to calculate route weights using the trained model
def calculate_route_weights(graph, avg_co, avg_no2, avg_pm25, traffic_data, model):
    route_weights = {}
    for start, neighbors in graph.items():
        for end, distance in neighbors.items():
            # Prepare the features for the model
            traffic_volume = traffic_data[start]['traffic_volume']
            avg_speed = traffic_data[start]['average_speed']
            
            # Features: [Traffic Volume, 1/Avg Speed, CO, NO2, PM2.5]
            features = [[traffic_volume, 1 / avg_speed, avg_co, avg_no2, avg_pm25]]
            
            # Predict the weight using the trained model
            weight = model.predict(features)[0]
            route_weights[(start, end)] = weight
    
    return route_weights

# Function to find the optimal route using the weighted graph
def find_optimal_route_with_ai(start, end, graph, route_weights):
    # Implement Dijkstra’s algorithm to find the path with the lowest weight
    shortest_distances = {intersection: float('inf') for intersection in graph}
    shortest_distances[start] = 0
    visited_intersections = set()
    previous_intersections = {}

    while visited_intersections != set(graph):
        current_intersection = min(
            set(graph) - visited_intersections,
            key=lambda intersection: shortest_distances[intersection]
        )
        visited_intersections.add(current_intersection)

        for neighbor in graph[current_intersection]:
            weight = route_weights[(current_intersection, neighbor)]
            new_distance = shortest_distances[current_intersection] + weight
            if new_distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = new_distance
                previous_intersections[neighbor] = current_intersection

    # Retrieve the optimal route
    route = []
    current_intersection = end
    while current_intersection != start:
        route.insert(0, current_intersection)
        current_intersection = previous_intersections[current_intersection]
    route.insert(0, start)

    # Return the optimal route
    return route, shortest_distances[end]

# Example usage
start_intersection = 'Intersection A'
end_intersection = 'Intersection D'

# Calculate route weights using the trained AI model
route_weights = calculate_route_weights(graph, avg_co, avg_no2, avg_pm25, traffic_data, model)

# Find the optimal route and total weight (time or cost)
optimal_route, total_weight = find_optimal_route_with_ai(start_intersection, end_intersection, graph, route_weights)

# Prepare results for saving to JSON
results = {
    "optimal_route": optimal_route,
    "total_weight": total_weight
}

# Write results to a JSON file
with open('optimal_route_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

print("Optimal Route:", optimal_route)
print("Total Weight (Cost or Time):", total_weight)
