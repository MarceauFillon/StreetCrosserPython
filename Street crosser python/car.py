from world_elements import *


class Car(WorldElement):
    def __init__(self, destination_world, line):
        self.initial_position = 0 if line % 2 == 0 else len(destination_world.grid[0]) - 1

        super().__init__(destination_world, line, self.initial_position, Elements.CAR, "O", "blue")

        self.going_right = 1 if line % 2 == 0 else 0
        self.position_on_road = self.initial_position

        self.line = line
        self.associated_world = destination_world

        self.moving = 1

        self.associated_world.grid[self.line][self.position_on_road] = self

    def get_position_to_check(self, i):
        position_to_check = self.position_on_road + i if self.going_right else self.position_on_road - i

        if position_to_check < 0 or position_to_check >= self.associated_world.columns:
            position_to_check = abs(self.associated_world.columns - abs(position_to_check))

        return position_to_check

    def check_after_crosswalk(self):
        position_to_check = self.get_position_to_check(1)

        if not isinstance(self.associated_world.grid[self.line][position_to_check], Crosswalk):
            return True

        position_to_check = self.get_position_to_check(2)

        if not isinstance(self.associated_world.grid[self.line][position_to_check], Car):
            return True

        if self.associated_world.grid[self.line][position_to_check].moving == 1:
            return True

        return False

    def check_crosswalk(self):
        position_to_check = self.get_position_to_check(1)

        if position_to_check not in self.associated_world.crosswalk_columns:
            return True

        if not self.associated_world.agent_in_safe_zone:
            return True

        return False

    def check_security_distance(self, distance):
        for i in range(1, distance + 2):
            position_to_check = self.get_position_to_check(i)

            if isinstance(self.associated_world.grid[self.line][position_to_check], Car):
                return False

        return True

    def move(self):
        if self.check_crosswalk() and self.check_after_crosswalk() and self.check_security_distance(1):

            self.moving = 1

            self.associated_world.set_back_cell(self.line, self.position_on_road)

            self.move_forward()

            if self.position_on_road >= len(self.associated_world.grid[0]) or self.position_on_road < 0:
                self.associated_world.remove_car(self)
            else:
                self.associated_world.grid[self.line][self.position_on_road] = self
        else:
            self.moving = 0

    def move_forward(self):
        if self.going_right:
            self.position_on_road += 1
        else:
            self.position_on_road -= 1

        self.y = self.position_on_road
