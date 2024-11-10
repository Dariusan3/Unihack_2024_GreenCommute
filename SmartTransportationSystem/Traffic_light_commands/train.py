import numpy as np
from traffic_env import TrafficEnv
from q_learning_agent import QLearningAgent

# Initialize environment and agent
env = TrafficEnv(num_intersections=4)
agent = QLearningAgent(num_states=env.observation_space.shape[0], num_actions=env.action_space.n)

# Training loop
num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()  # Get initial state
    state = np.argmax(state)  # Convert observation to a state index
    done = False
    
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        next_state = np.argmax(next_state)  # Convert next state to index
        agent.learn(state, action, reward, next_state)  # Learn from experience
        state = next_state  # Move to the next state
    
    if episode % 100 == 0:
        print(f"Episode {episode}, Q-table updated.")

# Save the Q-table for future use
np.save("q_table.npy", agent.q_table)
