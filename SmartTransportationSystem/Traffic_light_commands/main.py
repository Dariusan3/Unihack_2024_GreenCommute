import numpy as np
from traffic_env import TrafficEnv
from q_learning_agent import QLearningAgent

# Load the trained Q-table
q_table = np.load("q_table.npy")

# Initialize environment
env = TrafficEnv(num_intersections=4)

# Main loop for real-time control
while True:
    state = env.reset()  # Get current state (real-time vehicle counts and light states)
    state = np.argmax(state)  # Convert observation to state index
    
    # Use Q-learning agent's policy to decide the next action
    action = np.argmax(q_table[state])  # Select best action based on learned policy
    
    # Update the traffic light states in the environment
    next_state, reward, done, _ = env.step(action)
    
    # Optionally, log or display results (e.g., vehicle counts, rewards, etc.)
    print(f"Vehicle counts: {env.vehicle_counts}, Traffic light states: {env.light_states}")

    # Exit condition (example: break after a set number of iterations or based on real-time data)
    if done:
        break
