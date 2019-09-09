import math
import random

from car import *


class World:
    def __init__(self, lines, columns, road_lines, max_cars):
        self.grid = []
        for item in range(lines):
            self.grid.append([None] * columns)

        self.lines = lines
        self.columns = columns

        self.road_lines = road_lines
        self.road_lines_start = math.floor((self.lines - 1) / 2) - math.floor(self.road_lines / 2) + 1
        self.road_lines_end = math.floor((self.lines - 1) / 2) + math.floor(self.road_lines / 2)

        self.crosswalk_columns = [2, 7]

        self.cars = []

        for i in range(0, self.road_lines_end - self.road_lines_start +1):
            self.cars.append([])

        self.goal_coordinates = [0, 0]

        self.max_cars = max_cars

        self.agent_in_safe_zone = False

    def add_elements(self):
        for el in range(self.lines):
            for col in range(self.columns):
                self.set_back_cell(el, col)

    def add_car(self, road_for_car):
        if self.road_lines_start <= road_for_car <= self.road_lines_end:
            self.cars[self.road_lines_end-road_for_car].append(Car(self, road_for_car))

    def remove_car(self, car):
        self.cars[self.road_lines_end-car.line].remove(car)

    def cars_handler(self):
        for road_line in range(self.road_lines_start, self.road_lines_end+1):
            can_add_car = True

            if self.cars[self.road_lines_end-road_line].__len__() >= self.max_cars:
                continue

            for car in self.cars[self.road_lines_end-road_line]:
                if car.position_on_road <= 1 or car.position_on_road >= 8:
                    can_add_car = False
                    break

            probability = random.randint(1, 2)

            if can_add_car and probability == 2:
                self.add_car(road_line)

    # Clear the world => All grass
    def clear(self):
        self.grid = [[GroundSquare(self, x, y) for x in range(self.lines)] for y in range(self.columns)]

    def set_back_cell(self, el, col):
        if self.road_lines_start <= el <= self.road_lines_end:  # road lines
            self.grid[el][col] = Road(self, el, col)  # corresponds to a road element

            for crosswalk_col in self.crosswalk_columns:
                if col == crosswalk_col:
                    self.grid[el][col] = Crosswalk(self, el, col)  # corresponds to a crosswalk square

        elif el == self.goal_coordinates[0] and col == self.goal_coordinates[1]:
            self.grid[el][col] = Goal(self, el, col)

        else:  # ground
            self.grid[el][col] = GroundSquare(self, el, col)  # corresponds to a ground square

    def set_agent(self, x, y):
        self.grid[x][y] = AgentInWorld(self, x, y)

    def move_agent(self, x, y):
        self.grid[x][y] = AgentInWorld(self, x, y)

    def set_goal(self, x, y):
        self.grid[x][y] = Goal(self, x, y)
        old_goal = self.goal_coordinates
        self.goal_coordinates = [x, y]
        self.set_back_cell(old_goal[0], old_goal[1])

    def get_value(self, x, y):
        if 0 <= x < self.lines and 0 <= y < self.columns:
            return self.grid[x][y].value

        return 0

    def get_inverse_x(self, x):
        return self.lines - 1 - x
