import random
import numpy as np
import threading

from tkinter import StringVar
import matplotlib.pyplot as plt

from state_generator import StateHandler
from world_elements import *
from car import Car

from statistics import *

#from lib import plotting

#matplotlib.style.use('ggplot')


class Actions(Enum):
    WAIT = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Status(Enum):
    CRASHED = 0
    ALIVE = 1
    SAFE = 2


class Agent:
    def __init__(self, x_init, y_init, associated_world):
        self.x = x_init
        self.y = y_init

        self.world = associated_world
        self.world.set_agent(x_init, y_init)

        self.state = Status.ALIVE.value

    def move(self, direction):
        movement = direction
        prev_x = self.x
        prev_y = self.y

        if movement == Actions.UP.value:
            if self.x-1 == -1:
                self.state = Status.CRASHED.value
                return
            else:
                self.x += -1

        if movement == Actions.DOWN.value:
            if self.x+1 == self.world.lines:
                self.state = Status.CRASHED.value
                return
            else:
                self.x += 1

        if movement == Actions.RIGHT.value:
            if self.y+1 == self.world.columns:
                self.state = Status.CRASHED.value
                return
            else:
                self.y += 1

        if movement == Actions.LEFT.value:
            if self.y-1 == -1:
                self.state = Status.CRASHED.value
                return
            else:
                self.y += -1

        if isinstance(self.world.grid[self.x][self.y], Car):
            self.state = Status.CRASHED.value
            return

        if not isinstance(self.world.grid[prev_x][prev_y], Car):
            self.world.set_back_cell(prev_x, prev_y)

        if self.world.road_lines_start-1 <= self.x <= self.world.road_lines_end+1 \
                and self.y in self.world.crosswalk_columns:
            self.world.agent_in_safe_zone = True
            self.state = Status.SAFE.value
        else:
            self.world.agent_in_safe_zone = False
            self.state = Status.ALIVE.value

        self.world.move_agent(self.x, self.y)


class QLearning:
    def __init__(self, world, total_episodes=50000, total_test_episodes=100, max_steps=99, learning_rate=0.7,
                 gamma=0.618, epsilon=1.0, max_epsilon=1.0, min_epsilon=0.01, decay_rate=0.01):

        self.state_handler = StateHandler("states.txt")
        self.state_size = self.state_handler.get_states_length()
        self.states = self.state_handler.states

        self.action_size = Actions.__len__()

        self.agent = Agent(world.lines-1, world.columns - 1, world)

        #  Just to test for a goal position
        self.x_goal = 0
        self.y_goal = 0

        self.initial_distance = self.distance_to_goal(self.agent.x, self.agent.y)

        self.q_table = np.zeros((self.state_size, self.action_size))

        self.total_episodes = total_episodes  # Total episodes
        self.total_test_episodes = total_test_episodes  # Total test episodes
        self.max_steps = max_steps  # Max steps per episode

        self.learning_rate = learning_rate  # Learning rate
        self.gamma = gamma  # Discounting rate

        # Exploration parameters
        self.epsilon = epsilon  # Exploration rate
        self.max_epsilon = max_epsilon  # Exploration probability at start
        self.min_epsilon = min_epsilon  # Minimum exploration probability
        self.decay_rate = decay_rate  # Exponential decay rate for exploration prob

        self.number_of_steps = 0        # Number of total steps done during learning
        self.average_reward = []
        self.total_reward_arr = []
        self.total_reward = 0

    def distance_to_goal(self, x_actual, y_actual):
        # distance = math.sqrt(((self.x_goal-x_actual)**2)+((self.y_goal-y_actual)**2))
        distance = abs(self.x_goal - x_actual) + abs(self.y_goal - y_actual)
        return distance

    def step(self, action):
        direction = action

        self.agent.move(direction)

        new_distance = self.distance_to_goal(self.agent.x, self.agent.y)

        done = False

        if self.agent.state == Status.CRASHED.value:
            reward = -100           # Reward if it crashed
            done = True
        else:
            reward = (self.initial_distance - new_distance) * 5  # reward get higher when getting closer to the goal
            if self.agent.state == Status.SAFE.value and not reward == 0:
                reward = reward + 40                    # Bonus reward for taking the zebra

            if self.x_goal == self.agent.x and self.y_goal == self.agent.y:
                reward = reward + 1000                  # Bonus reward for reaching the goal
                done = True

        new_state = self.get_state()

        return new_state, reward, done

    def get_state(self):
        state_index = -1

        x_act = self.agent.x
        y_act = self.agent.y

        #  Need to prevent from stepping out of the grid. Right now it is not good.
        act_state = np.matrix([[self.agent.world.get_value(x_act - 2, y_act - 2),
                                self.agent.world.get_value(x_act - 2, y_act - 1),
                                self.agent.world.get_value(x_act - 2, y_act - 0),
                                self.agent.world.get_value(x_act - 2, y_act + 1),
                                self.agent.world.get_value(x_act - 2, y_act + 2)],
                               [self.agent.world.get_value(x_act - 1, y_act - 2),
                                self.agent.world.get_value(x_act - 1, y_act - 1),
                                self.agent.world.get_value(x_act - 1, y_act - 0),
                                self.agent.world.get_value(x_act - 1, y_act + 1),
                                self.agent.world.get_value(x_act - 1, y_act + 2)]])

        for i in range(0, self.states.__len__()):
            if np.equal(self.states[i], act_state).all():
                state_index = i
                break

        if state_index == -1:
            print("State at position (" + str(self.agent.x) + "," + str(self.agent.y) + "), NOT FOUND ; ", end='')
            print("State: (", end='')
            for number in np.ravel(act_state[0].getA()):
                print(str(number) + " ", end='')
            print()
            print("       ", end='')
            for number in np.ravel(act_state[1].getA()):
                print(str(number)  + " ", end='')
            print(")")

        return state_index

    def learning_algorithm(self, environment, save=False, q_file="", multiple_runs=False, run_index=0):
        initial_epsilon = self.epsilon
        step_successes = []
        average_rewards = []

        # 2 For life or until learning is stopped
        for episode in range(self.total_episodes):
            # Reset the environment
            environment.progress["value"] = episode
            environment.reset()

            rewards_for_average = []

            state_index = self.get_state()
            step = 0
            done = False

            if not environment.RUN:
                break

            for step in range(self.max_steps):
                for cars in environment.world.cars:
                    for car in cars:
                        car.move()

                environment.world.cars_handler()

                # 3. Choose an action a in the current world state (s)
                #  First we randomize a number
                exp_trade_off = random.uniform(0, 1)

                #  If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)??????????
                if exp_trade_off > self.epsilon:
                    action = np.argmax(self.q_table[state_index, :])

                # Else doing a random choice --> exploration  ?????????
                else:
                    action = random.randint(0, 4)       # Would be better with variables as boarders!!!!!!!!

                # Take the action (a) and observe the outcome state(s') and reward (r) ?????????
                new_state_index, reward, done = self.step(action)

                self.number_of_steps += 1
                self.total_reward += reward

                # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
                self.q_table[state_index, action] = self.q_table[state_index, action] + self.learning_rate * (reward + self.gamma * np.max(self.q_table[new_state_index, :]) - self.q_table[state_index, action])

                # Our new state is state
                state_index = new_state_index

                rewards_for_average.append(reward)

                if done and self.agent.state != Status.CRASHED.value and step != self.max_steps:
                    step_successes.append(step)
                # If done : finish episode
                if done or not environment.RUN:
                    break

                environment.connect_world_into_canvas()

            if multiple_runs:
                average_rewards.append(mean(rewards_for_average))

            # Reduce epsilon (because we need less and less exploration)
            self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)

            self.set_epsilon_display(environment)

            self.total_reward_arr.append(self.total_reward)
            self.average_reward.append(self.total_reward/(episode + 1))

        environment.stop_simulation()

        self.set_epsilon_display(environment, initial_epsilon)

        if save:
            self.save_q_table(q_file)
        if not multiple_runs:
            environment.thread_plotting = threading.Thread(target=self.plot)
            environment.thread_plotting.start()

        if multiple_runs:
            if step_successes.__len__():
                environment.multiple_learning_results_steps.append(step_successes)
            environment.multiple_learning_results_mean_reward.append(average_rewards)

    def plot(self):
        # plot the average reward dependent on the number of steps
        x1 = np.arange(len(self.average_reward))

        # plot cumulative reward as a function of the number of steps
        x2 = np.arange(len(self.total_reward_arr))

        plt.subplot(2, 1, 1)
        plt.plot(x1, self.average_reward, 'ko-')
        plt.title('Benchmark')
        # plt.subtitle('Average reward dependent on the number of steps')
        plt.xlabel('Number of steps')
        plt.ylabel('Average reward')

        plt.subplot(2, 1, 2)
        plt.plot(x2, self.total_reward_arr, 'r.-')
        plt.suptitle('Cumulative reward as a function of the number of steps')
        plt.xlabel('Number of steps')
        plt.ylabel('Cumulative reward')

        plt.show()
    
    def play_crosser(self, environment):
        rewards = []
        best_score = 0

        for episode in range(self.total_test_episodes):
            environment.progress["value"] = episode
            environment.reset()
            total_rewards = 0
            state = self.get_state()

            if not environment.RUN:
                break

            print("EPISODE ", episode)

            for step in range(self.max_steps):
                for cars in environment.world.cars:
                    for car in cars:
                        car.move()

                environment.world.cars_handler()

                action = np.argmax(self.q_table[state, :])

                new_state, reward, done = self.step(action)

                total_rewards += reward

                state = new_state

                environment.connect_world_into_canvas()

                if done or not environment.RUN:
                    rewards.append(total_rewards)
                    if total_rewards > best_score:
                        best_score = total_rewards
                    break

        print("Score over time: " + str(sum(rewards) / self.total_test_episodes))
        print("Best score: " + str(best_score))
        environment.stop_simulation()

    def save_q_table(self, filename):
        file = open(filename, "w+")

        for row in self.q_table:
            row_array = np.ravel(row)
            for number in row_array:
                file.write("%s " % number)
            file.write("\n")

        file.close()

    def load_q_table(self, filename):
        try:
            file = open(filename, "r+")
            self.q_table = np.zeros((self.state_size, self.action_size))
            index_x = 0

            for line in file:
                line1 = [float(x) for x in line.split()]
                index_y = 0
                for number in line1:
                    self.q_table[index_x][index_y] = number
                    index_y += 1
                index_x += 1

        except IOError:
            print("File doesn't exist, generation of empty q_table")
            self.q_table = np.zeros((self.state_size, self.action_size))

    def set_epsilon_display(self, environment, value=0):
        sv = StringVar()
        if not value:
            sv.set(str(self.epsilon))
        else:
            sv.set(str(value))

        environment.entries["Epsilon"].config(textvariable=sv)
