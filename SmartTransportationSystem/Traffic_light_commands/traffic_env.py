import gym
from gym import spaces
import numpy as np

class TrafficEnv(gym.Env):
    def __init__(self, num_intersections):
        super(TrafficEnv, self).__init__()
        self.num_intersections = num_intersections
        self.vehicle_counts = np.zeros(num_intersections)
        self.light_states = np.array(["Red"] * num_intersections)
        
        # Define action space: 0 for Red, 1 for Green, 2 for Yellow for each intersection
        self.action_space = spaces.MultiDiscrete([3] * num_intersections)
        
        # Define observation space: vehicle count and light state for each intersection
        self.observation_space = spaces.Box(
            low=0, high=100, shape=(num_intersections * 2,), dtype=np.int32
        )
        
    def reset(self):
        # Reset vehicle counts and light states to initial conditions
        self.vehicle_counts = np.random.randint(0, 50, size=self.num_intersections)
        self.light_states = np.array(["Red"] * self.num_intersections)
        return self._get_obs()
    
    def _get_obs(self):
        # Convert light states to numeric values (0=Red, 1=Green, 2=Yellow)
        light_encoded = np.array([0 if state == "Red" else 1 if state == "Green" else 2 for state in self.light_states])
        return np.concatenate([self.vehicle_counts, light_encoded])
    
    def step(self, action):
        # Update light states based on the action
        self.light_states = np.array(["Red" if act == 0 else "Green" if act == 1 else "Yellow" for act in action])
        
        # Update vehicle counts based on the current light states
        for i, light_state in enumerate(self.light_states):
            if light_state == "Green":
                self.vehicle_counts[i] = max(0, self.vehicle_counts[i] - np.random.randint(1, 10))  # Reduce count when green
            else:
                self.vehicle_counts[i] += np.random.randint(1, 5)  # Increase count when not green
        
        # Calculate reward: negative of total vehicle count (minimize congestion)
        reward = -np.sum(self.vehicle_counts)
        
        # Define done condition (arbitrary for this example)
        done = np.sum(self.vehicle_counts) < 10
        
        return self._get_obs(), reward, done, {}
