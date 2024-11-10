import gym
from gym import spaces
import numpy as np

class TrafficEnv(gym.Env):
    def __init__(self, num_intersections, optimal_route, total_weight):
        super(TrafficEnv, self).__init__()
        self.num_intersections = num_intersections
        self.vehicle_counts = np.zeros(num_intersections)  # Initial vehicle counts at intersections
        self.light_states = np.array(["Red"] * num_intersections)  # All lights are initially Red
        
        # Define optimal route (priority intersections) and total weight (priority level)
        self.optimal_route = [ord(i[-1]) - ord('A') for i in optimal_route]  # Convert "Intersection A" -> index 0, etc.
        self.total_weight = total_weight
        
        # Define action space (each intersection can have 3 possible states: Red, Green, Yellow)
        self.action_space = spaces.MultiDiscrete([3] * num_intersections)
        
        # Define observation space: vehicle counts and light states
        self.observation_space = spaces.Box(low=0, high=100, shape=(num_intersections * 2,), dtype=np.int32)

    def reset(self):
        self.vehicle_counts = np.random.randint(0, 50, size=self.num_intersections)  # Random vehicle counts
        self.light_states = np.array(["Red"] * self.num_intersections)  # Reset all lights to Red
        return self._get_obs()

    def _get_obs(self):
        # Convert light states to numeric values (Red=0, Green=1, Yellow=2)
        light_encoded = np.array([0 if state == "Red" else 1 if state == "Green" else 2 for state in self.light_states])
        return np.concatenate([self.vehicle_counts, light_encoded])

    def step(self, action):
        # Update the light states based on the chosen action
        self.light_states = np.array(["Red" if act == 0 else "Green" if act == 1 else "Yellow" for act in action])

        # Update vehicle counts based on light states
        for i, light_state in enumerate(self.light_states):
            if light_state == "Green":
                self.vehicle_counts[i] = max(0, self.vehicle_counts[i] - np.random.randint(1, 10))  # Green reduces vehicle count
            else:
                self.vehicle_counts[i] += np.random.randint(1, 5)  # Red/Yellow increases vehicle count

        # Reward: Prioritize green lights on optimal route intersections with total_weight
        reward = -np.sum(self.vehicle_counts)  # Negative reward for higher vehicle counts (minimizing congestion)
        
        for i in self.optimal_route:
            if self.light_states[i] == "Green":
                reward += self.total_weight  # Give extra reward for green on optimal route intersections

        done = np.sum(self.vehicle_counts) < 10  # Arbitrary stopping condition when traffic is low
        return self._get_obs(), reward, done, {}
