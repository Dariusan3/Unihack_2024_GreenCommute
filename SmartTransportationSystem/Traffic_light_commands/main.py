import streamlit as st
import numpy as np
import time
from traffic_env import TrafficEnv
from q_learning_agent import QLearningAgent

# Load trained Q-table from file
q_table = np.load("q_table.npy")

# Define the optimal route and weight for simulation
optimal_route = ["Intersection A", "Intersection D"]
total_weight = 8.0

# Initialize the traffic environment and Q-learning agent
env = TrafficEnv(num_intersections=4, optimal_route=optimal_route, total_weight=total_weight)
agent = QLearningAgent(num_states=env.observation_space.n, num_actions=env.action_space.n)

# Streamlit Interface: Display the title of the app
st.title("Traffic Light Control System")

# Display function for current vehicle counts and light states
def display_traffic_info():
    st.write("### Vehicle Counts at Each Intersection")
    st.write(env.vehicle_counts)

    st.write("### Current Traffic Light States")
    st.write(env.light_states)

# Main loop for real-time control of the traffic lights
st.write("### Real-time Traffic Light Control")

# Simulate and update the traffic lights
for step in range(5):  # Simulate for 5 steps
    state = env.reset()
    state = np.argmax(state)  # Convert the observation to a state index
    
    # Agent chooses the best action based on the trained Q-table
    action = np.argmax(q_table[state])
    
    # Apply the action and get the next state and reward
    next_state, reward, done, _ = env.step(action)
    
    # Display the current traffic info (vehicle counts and light states)
    display_traffic_info()
    
    # Wait for 1 second before simulating the next step
    time.sleep(1)

    if done:
        break
