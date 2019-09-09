from tkinter import *
import tkinter as tk
from tkinter import ttk
import seaborn as sns

import threading
from time import *

from q_learning import *
from world import World


class InterfaceGui(tk.Frame):
    def __init__(self, master, connecting_world):
        Frame.__init__(self, master)

        if master:
            master.title("Street crosser")
            master.geometry("900x550")

        self.world = connecting_world

        self.square_height = 513 / self.world.lines
        self.square_width = 513 / self.world.columns

        self.canvas = Canvas(self, bg="green", width='513', height='513')

        self.handles = [[None for y in range(self.world.columns)] for y in range(self.world.lines)]

        self.learning_handler = QLearning(self.world)

        self.start_simulation_button = None
        self.stop_simulation_button = None
        self.update_simulation_button = None

        self.learn_button = None
        self.use_learning_button = None
        self.reset_learning_button = None
        self.load_table_button = None
        self.multiple_learns_button = None

        self.speed_scale = None
        self.entries = {}

        self.multiple_learning_entries = {}
        self.multiple_learning_parameters = None
        self.multiple_learning_results_steps = None
        self.multiple_learning_results_mean_reward = None

        self.thread_simulation = None
        self.thread_learning = None
        self.thread_acting = None
        self.thread_multiple_learning = None
        self.thread_plotting = None
        self.threads = [self.thread_simulation, self.thread_learning, self.thread_acting, self.thread_multiple_learning, self.thread_plotting]
        self.simulation_speed = 0.5

        self.make_grid()
        self.make_control_bar()

        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=510, mode="determinate")
        self.progress.grid(row=1, column=0, columnspan=2)

        self.current = None
        self.pack()

        self.RUN = False
        self.MULTIPLE_RUN = False

    def connect_world_into_canvas(self):
        for el in range(self.world.lines):
            for col in range(self.world.columns):
                grid_element = self.world.grid[el][col]

                self.canvas.itemconfig(self.handles[el][col][1],
                                       text=grid_element.symbol)
                self.canvas.itemconfig(self.handles[el][col][0],
                                       fill=grid_element.color)

    def make_grid(self):
        s_height = self.square_height
        s_width = self.square_width
        c = self.canvas

        c.grid(row=0, column=1, sticky='n s e w')

        for x in range(self.world.lines):
            for y in range(self.world.columns):
                    (xr, yr) = (x*s_height, y*s_width)
                    r = c.create_rectangle(xr, yr, xr+s_height, yr+s_width, width=1, fill="white")
                    t = c.create_text(xr+s_height/2, yr+s_width/2, text=" ",
                                      font="System 15 bold")
                    self.handles[y][x] = (r, t)

        self.connect_world_into_canvas()

    def add_control_number(self, frame, title, start_value, learning_value = True):
        row = Frame(frame)
        lab = Label(row, width=15, text=title + ": ", anchor='w')
        sv = StringVar()
        sv.set(str(start_value))

        ent = Entry(row, textvariable=sv)
        if not learning_value:
            ent.bind("<KeyRelease>", self.reset)
        else:
            ent.bind("<KeyRelease>", self.reset_learning)

        row.pack(side=TOP, fill=X, padx=5, pady=3)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        self.entries[title] = ent

    def add_control_scale(self, frame, title, start_value, min_value, max_value):
        row = Frame(frame)
        lab = Label(row, width=15, text=title + ": ", anchor='w')
        ent = Scale(row, from_=min_value, to=max_value, orient=HORIZONTAL)
        ent.set(start_value)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        self.entries[title] = ent

    @staticmethod
    def make_title(frame, title):
        row = Frame(frame)
        lab = Label(row, width=30, text=title, anchor='w')
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)

    @staticmethod
    def add_button(frame, button, title, command):
        button = Button(frame, text=title, command=command)
        button.pack(side=LEFT, fill='none', expand='1')

        return button

    def add_buttons_simulation(self, frame):
        row = Frame(frame)
        self.start_simulation_button = self.add_button(row, self.start_simulation_button, "Run Simulation",
                                                       self.run_simulation)

        self.stop_simulation_button = self.add_button(row, self.stop_simulation_button, "Stop",
                                                      command=lambda: self.stop_simulation(True))

        self.update_simulation_button = self.add_button(row, self.update_simulation_button,
                                                        "Reset Simulation", self.reset)

        row.pack(side=TOP, fill=X)

    def make_control_bar(self):
        control_frame = Frame(self)

        self.add_buttons_simulation(control_frame)

        self.make_title(control_frame, "Environment parameters")
        self.add_control_number(control_frame, "Number of roads", 2, False)
        self.add_control_number(control_frame, "Max number of cars per line", 2, False)
        self.add_control_scale(control_frame, "Speed", 0, -100, +100)

        self.make_title(control_frame, "Learning parameters")
        self.add_control_number(control_frame, "Total episodes", 50000)  # Total episodes
        self.add_control_number(control_frame, "Total test episodes", 100)  # Total test episodes
        self.add_control_number(control_frame, "Max steps", 99)  # Max steps per episode

        self.add_control_number(control_frame, "Learning rate", 0.7)  # Learning rate
        self.add_control_number(control_frame, "Gamma", 0.618)  # Discounting rate

        # Exploration parameters
        self.add_control_number(control_frame, "Epsilon", 1.0)  # Exploration rate
        self.add_control_number(control_frame, "Max epsilon", 1.0)  # Exploration probability at start
        self.add_control_number(control_frame, "Min epsilon", 0.01)  # Minimum exploration probability
        self.add_control_number(control_frame, "Decay rate", 0.01)  # Exponential decay rate for exploration prob

        self.add_control_number(control_frame, "Q Table file", "q_table.txt")

        self.learn_button = self.add_button(control_frame, self.learn_button, "Learn", self.learn)

        self.use_learning_button = self.add_button(control_frame, self.use_learning_button, "Use learning",
                                                   self.act_from_learning)

        self.reset_learning_button = self.add_button(control_frame, self.reset_learning_button, "Reset learning",
                                                     self.reset_learning)

        self.load_table_button = self.add_button(control_frame, self.load_table_button, "Load q_table",
                                                 self.load_q_table)

        self.multiple_learns_button = self.add_button(control_frame, self.multiple_learns_button, "Multiple runs",
                                                      self.multiple_learns_window)

        control_frame.grid(row=0, column=0, sticky='n s e w')

    def simulation_loop(self):
        step = 0
        while self.RUN:
            if step == 7:
                o = 1
            for cars in self.world.cars:
                for car in cars:
                    car.move()
            if step == 0 or step == 1:
                self.learning_handler.agent.move(1)
            elif step == 7:
                self.learning_handler.agent.move(0)
            else:
                self.learning_handler.agent.move(3)

            if self.learning_handler.agent.state == Status.CRASHED.value:
                self.stop_simulation()
                break

            self.world.cars_handler()
            self.connect_world_into_canvas()

            step += 1
            sleep(self.simulation_speed)

    def learning_loop(self, multiple_runs=False, run_index=0):
        if not multiple_runs:
            self.learning_handler.learning_algorithm(self, True, self.entries["Q Table file"].get(), multiple_runs, run_index)
        else:
            self.learning_handler.learning_algorithm(self, False, "", multiple_runs, run_index)

    def acting_loop(self):
        self.learning_handler.play_crosser(self)

    def disable_entries(self):
        for key, value in self.entries.items():
            value.config(state='disabled')

    def enable_entries(self):
        for key, value in self.entries.items():
            value.config(state='normal')

    def disable_buttons(self):
        self.start_simulation_button.config(state='disabled')
        self.update_simulation_button.config(state='disabled')
        self.learn_button.config(state='disabled')
        self.reset_learning_button.config(state='disabled')
        self.use_learning_button.config(state='disabled')
        self.load_table_button.config(state='disabled')

        self.stop_simulation_button.config(state='normal')

    def enable_buttons(self):
        self.start_simulation_button.config(state='normal')
        self.update_simulation_button.config(state='normal')
        self.learn_button.config(state='normal')
        self.reset_learning_button.config(state='normal')
        self.use_learning_button.config(state='normal')
        self.load_table_button.config(state='normal')

        self.stop_simulation_button.config(state='disabled')

    def run_simulation(self):
        self.disable_entries()

        self.disable_buttons()

        self.RUN = True
        self.thread_simulation = threading.Thread(target=self.simulation_loop)
        self.thread_simulation.start()

    def stop_simulation(self, stop_all=False):
        self.enable_entries()

        self.enable_buttons()

        self.RUN = False

        if stop_all:
            self.MULTIPLE_RUN = False

        for thread in self.threads:
            if thread is not None and thread.isActive():
                thread.join()

    def reset_progress_bar(self, max_value):
        self.progress["value"] = 0
        self.progress["maximum"] = max_value - 1

    def update_canvas(self):
        self.square_height = 513 / self.world.lines
        self.square_width = 513 / self.world.columns

        self.canvas.delete("all")
        self.handles = [[None for y in range(self.world.columns)] for y in range(self.world.lines)]
        self.make_grid()

    def set_simulation_speed(self, speed_percentage):
        self.simulation_speed = 0.5 - 0.5 * speed_percentage/100

    def reset(self, event = None):
        try:
            roads = int(self.entries['Number of roads'].get())
            max_cars = int(self.entries['Max number of cars per line'].get())
            speed_percentage = int(self.entries['Speed'].get())

            self.set_simulation_speed(speed_percentage)
            updated_world = World(10, 10, roads, max_cars)

            updated_world.add_elements()
            updated_world.set_goal(self.learning_handler.x_goal, self.learning_handler.y_goal)

            self.world = updated_world

            self.learning_handler.agent = Agent(random.randint(self.world.road_lines_end, self.world.lines-1),
                                                random.randint(0, self.world.columns-1), self.world)

            self.update_canvas()

        except :
            print("Error in reset")

    def reset_learning(self, event = None):
        total_episodes = int(self.entries["Total episodes"].get())
        total_test_episodes = int(self.entries["Total test episodes"].get())
        max_steps = int(self.entries["Max steps"].get())

        learning_rate = float(self.entries["Learning rate"].get())
        gamma = float(self.entries["Gamma"].get())

        epsilon = float(self.entries["Epsilon"].get())
        max_epsilon = float(self.entries["Max epsilon"].get())
        min_epsilon = float(self.entries["Min epsilon"].get())
        decay_rate = float(self.entries["Decay rate"].get())

        self.learning_handler = QLearning(self.world, total_episodes, total_test_episodes, max_steps, learning_rate,
                                          gamma, epsilon, max_epsilon, min_epsilon, decay_rate)

        self.reset()
        self.progress["value"] = 0

    def learn(self, multiple_learns=False, run_index=0):
        self.disable_entries()

        self.disable_buttons()

        self.reset()

        self.RUN = True

        self.reset_progress_bar(self.learning_handler.total_episodes)

        self.thread_learning = threading.Thread(target=self.learning_loop, args=[multiple_learns, run_index])

        self.thread_learning.start()

    def act_from_learning(self):
        self.disable_entries()

        self.disable_buttons()

        self.RUN = True

        self.reset_progress_bar(self.learning_handler.total_test_episodes)

        self.reset()

        self.thread_acting = threading.Thread(target=self.acting_loop)
        self.thread_acting.start()

    def load_q_table(self):
        self.learning_handler.load_q_table(self.entries["Q Table file"].get())

    def multiple_learns_window(self):
        new_window = tk.Toplevel(self)
        new_window.grab_set()
        new_window.title("Multiple learning")
        new_window.geometry("300x150")

        choices = {}
        for key, value in self.entries.items():
            if key is not "Speed" and key != "Q Table file":
                choices[key] = key

        row1 = Frame(new_window)

        tkvar = StringVar(row1)
        tkvar.set('Gamma')  # set the default option
        self.multiple_learning_entries["Parameter option"] = tkvar

        popup_menu = OptionMenu(row1, tkvar, *choices)
        lab1 = Label(row1, text="Choose a parameter")
        lab1.pack(side=LEFT)
        popup_menu.pack(side=RIGHT, expand=YES, fill=X)
        row1.grid(row=1, column=1)

        row2 = Frame(new_window)
        lab = Label(row2, width=30, text="Number of episodes for each learn" + ": ", anchor='w')
        sv = StringVar()
        sv.set(str(1000))

        ent = Entry(row2, textvariable=sv)
        self.multiple_learning_entries["Number of episodes for each learn"] = ent

        row2.grid(row=2, column=1)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)

        row3 = Frame(new_window)
        lab2 = Label(row3, width=30, text="Start value" + ": ", anchor='w')
        sv2 = StringVar()
        sv2.set(str(0.1))

        ent2 = Entry(row3, textvariable=sv2)

        row3.grid(row=3, column=1)
        lab2.pack(side=LEFT)
        ent2.pack(side=RIGHT, expand=YES, fill=X)
        self.multiple_learning_entries["Start value"] = ent2

        row4 = Frame(new_window)
        lab3 = Label(row4, width=30, text="End value" + ": ", anchor='w')
        sv3 = StringVar()
        sv3.set(str(0.9))

        ent3 = Entry(row4, textvariable=sv3)

        row4.grid(row=4, column=1)
        lab3.pack(side=LEFT)
        ent3.pack(side=RIGHT, expand=YES, fill=X)
        self.multiple_learning_entries["End value"] = ent3

        Button(new_window, text="Start multiple learns", command=self.start_multiple_learns).grid(row=5, column=1)

        self.multiple_learning_parameters = new_window

    def start_multiple_learns(self):
        self.thread_multiple_learning = threading.Thread(target=self.multiple_learns)
        self.thread_multiple_learning.start()
        self.MULTIPLE_RUN = True
        #self.multiple_learns_window()

    def multiple_learns(self):
        coefficient = 1

        start_value = float(self.multiple_learning_entries["Start value"].get())
        end_value = float(self.multiple_learning_entries["End value"].get())
        number_of_episodes = int(self.multiple_learning_entries["Number of episodes for each learn"].get())
        parameter = self.multiple_learning_entries["Parameter option"].get()

        if start_value < 1:
            if start_value < 0.1:
                coefficient = 100
            else:
                coefficient = 10

        start_value = int(start_value * coefficient)
        end_value = int(end_value * coefficient)

        self.multiple_learning_results_steps = []
        self.multiple_learning_results_mean_reward = []
        run_index = 0

        self.multiple_learning_parameters.grab_release()
        self.multiple_learning_parameters.destroy()

        if parameter == "Gamma":
            self.run_multiple_gammas(start_value, end_value, run_index, number_of_episodes, coefficient, parameter)

    def run_multiple_gammas(self, start_value, end_value, run_index, number_of_episodes, coefficient, parameter):
        initial_value = float(self.entries["Gamma"].get())
        step_for = 3

        for value in range(start_value, end_value + 1, step_for):

            if not self.MULTIPLE_RUN:
                break

            sv = StringVar()
            sv.set(str(float(value/coefficient)))
            self.entries["Gamma"].config(textvariable=sv)
            sv2 = StringVar()
            sv2.set(str(number_of_episodes))
            self.entries["Total episodes"].config(textvariable=sv2)
            self.reset_learning()

            self.learn(True, run_index)
            self.thread_learning.join()

            run_index += 1

        sv = StringVar()
        sv.set(str(initial_value))
        self.entries["Gamma"].config(textvariable=sv)

        self.thread_plotting = threading.Thread(target=self.plot, args=[coefficient, parameter, step_for])
        self.thread_plotting.start()

        self.stop_simulation(True)

    def plot(self, coefficient, parameter, step_for):
        # plot the average reward dependent on the number of steps
        plt.title('Benchmark')

        if len(self.multiple_learning_results_steps):
            plt.subplot(2, 1, 1)
            sns.set()
            for i in range(0, len(self.multiple_learning_results_steps)):
                steps = self.multiple_learning_results_steps[i]

                label_string = parameter + " = " + str(float(((i+1)*step_for)/coefficient))
                sns.distplot(steps, label=label_string)

            plt.xlabel('Steps')
            plt.ylabel('Percentage')
            plt.legend()

        plt.subplot(2, 1, 2)
        for i in range(0, len(self.multiple_learning_results_mean_reward)):
            averages = self.multiple_learning_results_mean_reward[i]

            label_string = parameter + " = " + str((float(((i+1)*step_for)) / coefficient))
            plt.plot(averages, label=label_string)

        plt.xlabel('Episodes')
        plt.ylabel('Reward')
        plt.legend()

        plt.show(block=True)





