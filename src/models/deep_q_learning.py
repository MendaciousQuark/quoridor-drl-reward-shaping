import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
from .action_lookup import action_lookup
from game import Move

class DQNAgent:
    def __init__(self, state_shape, action_size, pawns):
        self.state_shape = state_shape
        self.batch_size = 32 #arbitrarilly chosen
        self.action_size = action_size
        self.memory = deque(maxlen=10000)  # Experience replay buffer
        self.gamma = 0.95  # Discount factor
        self.pawns = pawns
        
        # Exploration parameters
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
        self.learning_rate = 0.001
        self.model = create_q_model(state_shape, action_size)
        self.model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def create_q_model(state_shape, action_size=len(action_lookup)):
    """Creates a Deep Q-Learning Model."""
    inputs = layers.Input(shape=state_shape)
    
    # Example architecture
    layer1 = layers.Dense(128, activation='relu')(inputs)
    layer2 = layers.Dense(128, activation='relu')(layer1)
    action = layers.Dense(action_size, activation='linear')(layer2)
    
    return tf.keras.Model(inputs=inputs, outputs=action)
