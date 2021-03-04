import numpy as np


class QLearning:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.q_values = np.zeros((rows, columns, 8))
        self.actions = ['up', 'right', 'down', 'left', 'top_left', 'top_right', 'bottom_left', 'bottom_right']
        self.rewards = None

    def create_rewards(self, world):
        self.rewards = np.full((self.rows, self.columns), -100.)
        for x in range(self.rows):
            for y in range(self.columns):
                if not world.empty_at(y, x):
                    if world.exit_at(y, x):
                        self.rewards[x, y] = 100
                    elif world.characters_at(y, x):
                        self.rewards[x, y] = -1
                else:
                    self.rewards[x, y] = -1

    def print_grid(self):
        for row in self.rewards:
            print(row)

    def is_terminal_state(self, current_row_index, current_column_index):
        if self.rewards[current_row_index, current_column_index] == -1.:
            return False
        else:
            return True

    def get_starting_location(self):
        current_row_index = np.random.randint(self.rows)
        current_column_index = np.random.randint(self.columns)
        while self.is_terminal_state(current_row_index, current_column_index):
            current_row_index = np.random.randint(self.rows)
            current_column_index = np.random.randint(self.columns)
        return current_row_index, current_column_index

    def get_next_action(self, current_row_index, current_column_index, epsilon):
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_row_index, current_column_index])
        else:
            return np.random.randint(8)

    def get_next_location(self, current_row_index, current_column_index, action_index):
        new_row_index = current_row_index
        new_column_index = current_column_index
        if self.actions[action_index] == 'up' and current_column_index > 0:
            new_column_index -= 1
        elif self.actions[action_index] == 'right' and current_row_index < self.columns - 1:
            new_row_index += 1
        elif self.actions[action_index] == 'down' and current_column_index < self.columns - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'left' and current_row_index > 0:
            new_row_index -= 1
        elif self.actions[action_index] == 'top_right' and current_column_index > 0 and current_row_index < self.columns - 1:
            new_column_index -= 1
            new_row_index += 1
        elif self.actions[action_index] == 'top_left' and current_row_index > 0 and current_column_index > 0:
            new_row_index -= 1
            new_column_index -= 1
        elif self.actions[action_index] == 'bottm_right' and current_column_index < self.columns - 1 and current_row_index < self.columns - 1:
            new_column_index += 1
            new_row_index += 1
        elif self.actions[action_index] == 'bottom_left' and current_column_index < self.columns - 1 and current_row_index > 0:
            new_column_index += 1
            new_row_index -= 1
        return new_row_index, new_column_index

    def get_shortest_path(self, start_row_index, start_column_index):
        if self.is_terminal_state(start_row_index, start_column_index):
            return []
        else:
            current_row_index, current_column_index = start_row_index, start_column_index
            shortest_path = [[current_row_index, current_column_index]]
            while not self.is_terminal_state(current_row_index, current_column_index):
                action_index = self.get_next_action(current_row_index, current_column_index, 1.)
                current_row_index, current_column_index = self.get_next_location(current_row_index,
                                                                                 current_column_index, action_index)
                shortest_path.append([current_row_index, current_column_index])
            return shortest_path

    def train(self):
        epsilon = 0.7
        discount_factor = 0.9
        learning_rate = 0.9

        for episode in range(1000):
            row_index, column_index = self.get_starting_location()
            count = 0
            while not self.is_terminal_state(row_index, column_index) and count < 10000:
                count += 1
                action_index = self.get_next_action(row_index, column_index, epsilon)

                old_row_index, old_column_index = row_index, column_index
                row_index, column_index = self.get_next_location(row_index, column_index, action_index)

                reward = self.rewards[row_index, column_index]
                old_q_value = self.q_values[old_row_index, old_column_index, action_index]
                temporal_difference = reward + (
                            discount_factor * np.max(self.q_values[row_index, column_index])) - old_q_value

                new_q_value = old_q_value + (learning_rate * temporal_difference)
                self.q_values[old_row_index, old_column_index, action_index] = new_q_value
        print('Training complete!')
