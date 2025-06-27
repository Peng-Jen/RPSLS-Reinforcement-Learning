class BaseAgent:
    def __init__(self, config):
        self.n_actions = config.n_actions
        self.name = "BaseAgent"

    def encode_state(self, raw_state):
        return raw_state
    
    def select_action(self, state):
        raise NotImplementedError("Must implement select_action")

    def update(self, state, action, reward, next_state):
        pass

    def save_Q(self, rewards_table_name=""):
        import pickle
        import os
        if hasattr(self, "Q"):
            folder_path = './saved_Q_tables'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            if rewards_table_name:
                file_path = f"./saved_Q_tables/{self.name}_{rewards_table_name}.pkl"
            else:
                file_path = f"./saved_Q_tables/{self.name}.pkl"
            with open(file_path, "wb") as file:
                pickle.dump(self.Q, file)



