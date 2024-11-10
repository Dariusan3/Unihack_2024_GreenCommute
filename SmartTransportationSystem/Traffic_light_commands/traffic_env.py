import numpy as np
import gym
from gym import spaces

class TrafficEnv(gym.Env):
    def __init__(self, num_intersections, optimal_route, total_weight):
        super(TrafficEnv, self).__init__()
        self.num_intersections = num_intersections
        self.optimal_route = optimal_route
        self.total_weight = total_weight
        self.vehicle_counts = np.random.randint(0, 10, size=num_intersections)
        self.light_states = ['Red'] * num_intersections
        
        # Action space: Each intersection has 3 possible states (Red, Green, Yellow)
        self.action_space = spaces.MultiDiscrete([3] * num_intersections)  # 3 states per intersection

        # Observation space: Vehicle count at each intersection (Discrete)
        self.observation_space = spaces.MultiDiscrete([10] * num_intersections)  # Vehicle counts range from 0 to 9
        
    def reset(self):
        self.vehicle_counts = np.random.randint(0, 10, size=self.num_intersections)
        self.light_states = ['Red'] * self.num_intersections
        return self.vehicle_counts
    
    def step(self, action):
        # Update the light states and vehicle counts based on the action
        action_str = self.decode_action(action)
        for i, state in enumerate(action_str):
            self.light_states[i] = state
        
        # Calculate the reward (based on congestion and optimal route)
        reward = self.calculate_reward()
        
        return self.vehicle_counts, reward, False, {}
    
    def decode_action(self, action):
        action_str = []
        for i in range(self.num_intersections):
            action_str.append(['Red', 'Green', 'Yellow'][action[i]])
        return action_str
    
    def calculate_reward(self):
        # Reward for prioritizing the optimal route and reducing congestion
        reward = 0
        for i, intersection in enumerate(self.optimal_route):
            if self.light_states[i] == 'Green':
                reward += self.total_weight
        reward -= np.sum(self.vehicle_counts)  # Penalize for congestion
        return reward
