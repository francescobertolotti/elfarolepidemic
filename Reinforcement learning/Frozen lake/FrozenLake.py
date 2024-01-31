import gymnasium as gym
import random
import numpy as np
import json
import os
import matplotlib.pyplot as plt

class Lake:

    def __init__(self, restore_q_table: bool = False, printBool: bool = True, dim_r: int = 4, dim_c: int = 4, render: bool = True) -> None:

        # Debug
        self.printBool = printBool
        if render: render_mode = 'human'
        else: render_mode = 'ansi'

        # Params
        self.r_t = 0.1
        self.y = 0.9
        self.a = 0.5
        self.epsilon = 0.25

        # Env
        self.enviroment = gym.make("FrozenLake-v1", map_name=f"{dim_r}x{dim_c}", is_slippery=False, render_mode=render_mode)
        self.enviroment.reset()
        if render: self.enviroment.render()
        self.success_history = []
        self.steps_history = []
        self.steps_success_history = []

        self.initial_data = self.jsonLoader("qtableStore.json")
        
        self.logs = f'''
Init:
    - restore_q_table: {restore_q_table}
    - initial_data: {self.initial_data}
    - printBool: {printBool}
    - render: {render}
    - r_t: {self.r_t}
    - y: {self.y}
    - a: {self.a}
    - epsilon: {self.epsilon}
        '''

        if self.printBool: print(self.logs)

        if restore_q_table:
            self.qtable = np.array(self.initial_data["qTables"][len(self.initial_data["qTables"]) - 1])
        else:
            self.qtable = np.zeros((self.enviroment.observation_space.n, self.enviroment.action_space.n))




    def jsonLoader(self, name: str) -> str:
        if os.path.exists(name):
            
            with open(name, encoding="utf-8") as file:
                content = json.load(file)
           
        else:
            print("Unable to find %s file in current directory." % name)
            content = ""
        return content

    def train(self, episodes: int):
        for i in range(episodes):
            state = self.enviroment.reset()[0]
            terminated = False
            truncated = False
            cont = 0
            while not terminated and not truncated:
                if random.random() < self.epsilon:
                    action = self.enviroment.action_space.sample()
                else:   
                    if max(self.qtable[state]) == 0:
                        action = self.enviroment.action_space.sample()
                    else:
                        action = np.argmax(self.qtable[state])
                    

                    
                new_state, reward, terminated, truncated, info  = self.enviroment.step(action)

                if (terminated or truncated) and reward == 0:
                    reward = -1 * self.r_t
                    self.success_history.append(0)

                if (terminated or truncated) and reward == 1:
                    self.success_history.append(1)
                    self.steps_success_history.append(cont)

                self.qtable[state, action] = self.qtable[state, action] + self.a * (reward + self.y * np.max(self.qtable[new_state]) - self.qtable[state, action])
                
                latest_log = f'''
----------------------------
Episode: {i + 1}
Action: {action}
State: {state}
NewState: {new_state}
Reward: {reward}
Terminated: {terminated}
Truncated: {truncated}
Info: {info}

QTable:\n{self.qtable}
----------------------------
'''
                if self.printBool: print(latest_log)
                self.logs += latest_log

                state = new_state

                cont += 1

            self.steps_history.append(cont)
    
    def jsonWriter(self, name: str, content) -> str:
        if os.path.exists(name):
            #try:
            with open(name, 'w') as file:
                json.dump(content, file)
            #except Exception:
                #print("Unable to write %s file, unexpected error." % name)
        else:
            print("Unable to write %s file in current directory." % name)

    def save(self):
        self.initial_data["qTables"].append(self.qtable.tolist())
        self.initial_data["SuccessHistory"].append(self.success_history)
        self.initial_data["StepsHistory"].append(self.steps_history)
        self.initial_data["SuccessStepsHistory"].append(self.steps_success_history)
        self.jsonWriter("qtableStore.json", self.initial_data)

    def show_history(self, save_plot: bool = True, show_plot: bool = False):
        
        f_n = len(next(os.walk('plots'))[1]) + 1
        if save_plot: os.mkdir(f'plots/{f_n}')

        # Success history
        plt.plot(self.success_history)
        plt.title('Success history')
        plt.xlabel('Episode')
        fig1 = plt.gcf()
        if show_plot: plt.show()
        plt.draw()
        if save_plot: fig1.savefig(f'plots/{f_n}/success_history_{f_n}.png')
        plt.clf()

        # Steps history
        plt.plot(self.steps_history)
        plt.title('Steps history')
        plt.xlabel('Episode')
        plt.ylabel('Steps')
        fig2 = plt.gcf()
        if show_plot: plt.show()
        plt.draw()
        if save_plot: fig2.savefig(f'plots/{f_n}/steps_history_{f_n}.png')
        plt.clf()

        # Success steps history
        plt.plot(self.steps_success_history)
        plt.title('Success steps history')
        plt.ylabel('Steps')
        fig3 = plt.gcf()
        if show_plot: plt.show()
        plt.draw()
        if save_plot: fig3.savefig(f'plots/{f_n}/success_steps_history_{f_n}.png')
        plt.clf()
        
        if save_plot: 
            with open(f'plots/{f_n}/logs_{f_n}.txt', 'w') as f:
                f.write(self.logs)





l = Lake(restore_q_table=True, printBool=True, dim_r=4, dim_c=4, render=True)
l.train(episodes=10)
l.save()
l.show_history(save_plot=True, show_plot=False)