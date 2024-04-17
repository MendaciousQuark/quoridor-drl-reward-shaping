import numpy as np

class RewardNormalizer:
    def __init__(self, alpha=0.5):
        self.mean = 0
        self.var = 1
        self.alpha = alpha

    def normalize(self, reward):
        self.mean = self.alpha * self.mean + (1 - self.alpha) * reward
        new_var = self.alpha * self.var + (1 - self.alpha) * (reward - self.mean) ** 2
        self.var = max(new_var, 1e-2)  # Prevent division by very small number
        std_dev = np.sqrt(self.var)
        return (reward - self.mean) / std_dev
