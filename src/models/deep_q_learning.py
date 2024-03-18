import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from .action_lookup import action_lookup, action_id_to_q_index
from .model import Model
from game import Move
from logic import validateMove
import time

class DQNAgent (Model):
    def __init__(self, state_shape, action_size, colour, pawns, epsilon=0.5, name='DQNAgent', description='A Deep Q-Learning agent.', trained_model_path=None):
        super().__init__(colour, pawns, name, description)
        self.state_shape = state_shape
        self.batch_size = 100 #arbitrarilly chosen
        self.action_size = action_size
        self.memory = deque(maxlen=1000)  # Experience replay buffer
        self.gamma = 0.95  # Discount factor
        self.pawns = pawns
        self.trained_model_path = trained_model_path
        
        # Exploration parameters
        self.epsilon = epsilon  # Exploration rate (arbitrarily chosen)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.5
        
        self.learning_rate = 0.001
        self.model = create_q_model(state_shape, action_size)
        self.model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))

    def remember(self, state, action_id, reward, next_state, done):
        self.memory.append((state, action_id, reward, next_state, done))

    def act(self, state, board, verbose=False):
        if np.random.rand() <= self.epsilon:
            # chose a random action but try to move first
            while True:
                try:
                    random_action = random.choice(self.action_state_movements)
                except:
                    random_action = random.choice(self.action_state)
                if verbose:
                    print('Random action:', random_action[1])
                if validateMove(random_action[0], board, self.pawns[self.colour])[0] and random_action[1] != None:
                    break
            return random_action[1] #return the action id
        # Predict Q-values for all actions
        all_q_values = self.model.predict(state)

        # Initialize variables to keep track of the best legal action and its Q-value
        best_action = None
        best_q_value = -np.inf  # Start with a very low Q-value
        for action in self.action_state:
            if validateMove(action[0], board, self.pawns[self.colour])[0] and action[1] != None:
                q_value = self.get_q_value_for_action(all_q_values, action[1])
                if q_value > best_q_value:
                    best_action = action[1]
                    best_q_value = q_value
        if best_action == None:
            print('\nNo legal moves found. Attempting random action.')
            return random.choice(self.action_state)[1]
        if verbose:
            print('Decided on best action:', best_action)
        return best_action

    def replay(self, batch_size):
        start_time = time.time()  # Start tracking time

        minibatch = random.sample(self.memory, int(batch_size/100))
        for state, action_id, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][0][0][action_id_to_q_index[action_id]] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        end_time = time.time()  # Stop tracking time
        elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
        minutes, seconds = divmod(elapsed_time, 60)  # Convert elapsed time to minutes and seconds
        print(f'Replay time: {int(minutes)} minutes {int(seconds)} seconds')  # Print elapsed time
            
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