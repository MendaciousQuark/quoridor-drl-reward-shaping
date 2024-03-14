import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from .action_lookup import action_lookup, action_id_to_q_index
from .model import Model
from game import Move

class DQNAgent (Model):
    def __init__(self, state_shape, action_size, colour, pawns, name='DQNAgent', description='A Deep Q-Learning agent.'):
        super().__init__(colour, pawns, name, description)
        self.state_shape = state_shape
        self.batch_size = 32 #arbitrarilly chosen
        self.action_size = action_size
        self.memory = deque(maxlen=10000)  # Experience replay buffer
        self.gamma = 0.95  # Discount factor
        self.pawns = pawns
        
        # Exploration parameters
        self.epsilon = 1#0.23  # Exploration rate (arbitrarily chosen)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
        self.learning_rate = 0.001
        self.model = create_q_model(state_shape, action_size)
        self.model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            random_action = random.choice(self.action_state)
            print('Random action:', random_action)#random_action[1])
            return random_action[1] #return the action id
        # Predict Q-values for all actions
        all_q_values = self.model.predict(state)

        # Initialize variables to keep track of the best legal action and its Q-value
        best_action = None
        best_q_value = -np.inf  # Start with a very low Q-value
        for action in self.action_state:
            q_value = self.get_q_value_for_action(all_q_values, action[1])
            if q_value > best_q_value:
                best_action = action[1]
                best_q_value = q_value
        print('Decided on best action:', best_action)
        return best_action

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
            
    def save_model(self, file_path='path_to_my_model.h5'):
        self.model.save(file_path)
        
    def load_model(self, file_path='path_to_my_model.h5'):
        self.model = load_model(file_path)
    
    def get_q_value_for_action(self ,all_q_values, action_id):
        q_index = action_id_to_q_index[action_id]  # Use the mapping
        return all_q_values[0][0][0][q_index]

def create_q_model(state_shape, action_size=len(action_lookup)):
    print('Creating Q model with state shape:', state_shape, 'and action size:', action_size)
    """Creates a Deep Q-Learning Model."""
    inputs = layers.Input(shape=state_shape)
    
    # Example architecture
    layer1 = layers.Dense(128, activation='relu')(inputs)
    layer2 = layers.Dense(128, activation='relu')(layer1)
    #layer2 = layers.Flatten()(layer2)
    action = layers.Dense(action_size, activation='linear')(layer2)
    model = tf.keras.Model(inputs=inputs, outputs=action)
    print('Model summary:', model.summary())
    return model