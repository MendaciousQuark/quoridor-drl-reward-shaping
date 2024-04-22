import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from .action_lookup import action_lookup, action_id_to_q_index
from .model import Model
from pathlib import Path
import time
import pdb

class DQNAgent (Model):
    def __init__(self, state_shape, action_size, colour, pawns, epsilon=0.5, name='DQNAgent', description='A Deep Q-Learning agent.', trained_model_path=None):
        super().__init__(colour, pawns, name, description, trained_model_path)
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
        
        self.learning_rate = 0.01
        self.model = create_q_model(state_shape, action_size)
        self.model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate, clipvalue=1.0))

    def remember(self, state, action_id, reward, next_state, done):
        self.memory.append((state, action_id, reward, next_state, done))

    def act(self, state, verbose=False):
        # Check if there are no legal moves
        if not self.action_state:
            print("No legal moves available.")
            pdb.set_trace()  # Debugging state
            return None  # Appropriate error handling or default action

        # Epsilon-greedy policy decision
        if np.random.rand() <= self.epsilon:
            # Prefer movement actions if available with a 70% probability
            actions = self.action_state_movements if np.random.rand() < 0.7 and self.action_state_movements else self.action_state
            random_action = random.choice(actions)
            
            if verbose:
                print('Random action:', random_action[1])
            self.random_action = random_action[1]
            return random_action[1]

        try:
            # Predict Q-values for all potential actions
            all_q_values = self.model.predict(state, verbose=0)  # Assume shape is (1, num_possible_actions)
            q_values = all_q_values.flatten()  # Flatten the array for easier indexing
            
            # Prepare a list of valid action indices from action_state and their corresponding Q-indices
            valid_actions = [(act[1], action_id_to_q_index[act[1]]) for act in self.action_state if act[1] in action_id_to_q_index]
            action_ids, indices = zip(*valid_actions)  # Unzip into separate lists

            # Fetch the Q-values for the indexed actions
            relevant_q_values = q_values[list(indices)]

            # Find the index of the best Q-value in the filtered list
            best_index = np.argmax(relevant_q_values)
            best_action_id = action_ids[best_index]  # Correctly map back to the action ID

            if best_action_id is None:
                print("\nNo legal moves found. Attempting random action.")
                self.random_action = random.choice(self.action_state)[1]
                return self.random_action  # Return a random legal action

            if verbose:
                print(f"Decided on best action: {best_action_id} with Q-value: {relevant_q_values[best_index]}")

            return best_action_id

        except KeyError as e:
            print(f"Error: Action ID mapping issue - {str(e)}")
            return None
        except IndexError as e:
            print(f"Error: Index out of bounds - {str(e)}")
            return None

    def replay(self, batch_size):
        start_time = time.time()  # Start tracking time

        minibatch = random.sample(self.memory, int(batch_size/100))
        for state, action_id, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][0][0][action_id_to_q_index[action_id]] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        end_time = time.time()  # Stop tracking time
        elapsed_time = end_time - start_time  # Calculate elapsed time in seconds
        minutes, seconds = divmod(elapsed_time, 60)  # Convert elapsed time to minutes and seconds
        print(f'\nReplay time: {int(minutes)} minutes {int(seconds)} seconds')  # Print elapsed time
            
    def save_model(self, directory_path='src/trained_models/DQNagents/agent_0/'):
        # Ensure the directory_path is a Path object for consistency
        directory_path = Path(directory_path)
        
        # Create the directory if it doesn't exist, including any necessary parent directories
        directory_path.mkdir(parents=True, exist_ok=True)

        # Specify the model filename.
        model_filename = 'model.keras'
        
        # Combine the directory path and model filename to form the full path
        full_model_path = directory_path / model_filename

        # Save the model at the full path
        self.model.save(str(full_model_path))
    
        print(f"Model saved to {full_model_path}")

        
    def load_model(self, directory_path='src/trained_models/DQNagents/agent_0/'):
        # Ensure the directory_path is a Path object for consistency
        directory_path = Path(directory_path)

        # Specify the model filename.
        model_filename = 'model.keras'
        
        # Combine the directory path and model filename to form the full path
        full_model_path = directory_path / model_filename

        self.model = load_model(full_model_path)

        print(f"Model loaded from {directory_path}")
    
    def get_q_value_for_action(self ,all_q_values, action_id):
        try:
            q_index = action_id_to_q_index[action_id]  # Mapping from action ID to Q-value index
            return all_q_values[0][0][0][q_index]
        except KeyError:
            print(f"Error: Action ID {action_id} not found in index mapping.")
            return None
        except IndexError:
            print(f"Error: Index {q_index} out of bounds for Q-values array.")
            return None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        #less than comparision between two agents is based on name of save location
        return self.trained_model_path < other.trained_model_path

    def __gt__(self, other):
        #greater than comparision between two agents is based on name of save location
        return self.trained_model_path > other.trained_model_path

    def __le__(self, other):
        #less than or equal to comparision between two agents is based on name of save location
        return self.trained_model_path <= other.trained_model_path

    def __ge__(self, other):
        #greater than or equal to comparision between two agents is based on name of save location
        return self.trained_model_path >= other.trained_model_path

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __hash__(self) -> int:
        return hash(self.trained_model_path)

    def __str__(self):
        return f"{self.name} - {self.description},\n state_shape: {self.state_shape},\n batch_size: {self.batch_size},\n action_size: {self.action_size},\n memory: {self.memory},\n gamma: {self.gamma},\n pawns: {self.pawns},\n trained_model_path: {self.trained_model_path},\n epsilon: {self.epsilon},\n epsilon_min: {self.epsilon_min},\n epsilon_decay: {self.epsilon_decay},\n learning_rate: {self.learning_rate},\n model: {self.model}"

def create_q_model(state_shape, action_size=len(action_lookup), dropout_rate=0.2):
    print('Creating Q model with state shape:', state_shape, 'and action size:', action_size)
    """Creates a Deep Q-Learning Model with regularizations."""
    inputs = layers.Input(shape=state_shape)
    
    x = inputs
    for _ in range(3):
        x = layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)  # L2 Regularization
        x = layers.Dropout(dropout_rate)(x)  # Dropout
        x = layers.BatchNormalization()(x)  # Batch Normalization
    
    action = layers.Dense(action_size, activation='linear')(x)
    model = models.Model(inputs=inputs, outputs=action)
    model.summary()
    return model