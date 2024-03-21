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
import pdb

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
            if(self.action_state == None):
                pdb.set_trace()
            # chose a random action but try to move more than placing
            while True:
                try:
                    movement_prob = 0.5 if len(self.action_state_movements) > 0 else 0
                    if np.random.rand() > 1 - movement_prob:
                        #choose a random action from the movement actions
                        random_action_index = random.randint(0, len(self.action_state_movements) - 1)
                        random_action = self.action_state_movements[random_action_index]
                    else:
                        #choose a random action from the placement and movement actions
                        random_action_index = random.randint(0, len(self.action_state) - 1)
                        random_action = self.action_state[random_action_index]
                except Exception as e:
                    if(len(self.action_state) > 0):
                        continue
                    else:
                        print('No legal moves found. Attempting random action.')
                        pdb.set_trace()
                        break
                if verbose:
                    print('Random action:', random_action[1])
                if random_action[1] == None:
                    pdb.set_trace()
                else:
                    break
            self.last_action = random_action[1]
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
        if best_action == None:
            print('\nNo legal moves found. Attempting random action.')
            pdb.set_trace()
            self.last_action = random.choice(self.action_state)[1]
            return random.choice(self.action_state)[1]
        if verbose:
            print('Decided on best action:', best_action)
        self.last_action = best_action
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