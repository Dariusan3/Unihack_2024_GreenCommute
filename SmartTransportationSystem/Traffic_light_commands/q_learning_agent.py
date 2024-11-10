import numpy as np

class QLearningAgent:
    def __init__(self, num_states, num_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha    # Learning rate
        self.gamma = gamma    # Discount factor
        self.epsilon = epsilon  # Exploration rate
        
        # Initialize Q-table: state-action value table
        self.q_table = np.zeros((num_states, num_actions))
        
    def choose_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.num_actions)  # Exploration
        else:
            return np.argmax(self.q_table[state])  # Exploitation
    
    def learn(self, state, action, reward, next_state):
        # Q-learning update rule
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error
