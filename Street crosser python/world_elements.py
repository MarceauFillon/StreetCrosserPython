from enum import Enum


class Elements(Enum):
    OUTSIDE = 0
    ROAD = 1
    CROSSWALK = 2
    CAR = 3
    GROUND = 4
    GOAL = 5
    AGENT = 6


class WorldElement:
    def __init__(self, world, x, y, value, symbol, color):
        self.x = x
        self.y = y

        self.associated_world = world

        self.value = value.value
        self.symbol = symbol
        self.color = color

    # Make a Tkinter compatible color
    @staticmethod
    def rgb(red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)


class GroundSquare(WorldElement):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, Elements.GROUND, " ", "green")


class Crosswalk(WorldElement):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, Elements.CROSSWALK, "-", "yellow")


class Road(WorldElement):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, Elements.ROAD, " ", self.rgb(128, 128, 128))


class AgentInWorld(WorldElement):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, Elements.AGENT, "*", "red")


class Goal(WorldElement):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, Elements.GOAL, "G", "orange")

