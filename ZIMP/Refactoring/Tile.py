from Directions import Direction


class Tile:
    # Added default arguments - Daniel
    def __init__(self, name, x=16, y=16, effect=None, doors=None, entrance=None):
        if doors is None:
            doors = []
        self.name = name
        self.x = x
        self.y = y
        self.effect = effect
        self.doors = doors
        self.entrance = entrance

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def change_door_position(self, idx, direction):
        self.doors[idx] = direction

    def set_entrance(self, direction):
        self.entrance = direction

    def rotate_entrance(self):
        if self.entrance == Direction.NORTH:
            self.set_entrance(Direction.EAST)
            return
        if self.entrance == Direction.SOUTH:
            self.set_entrance(Direction.WEST)
            return
        if self.entrance == Direction.EAST:
            self.set_entrance(Direction.SOUTH)
            return
        if self.entrance == Direction.WEST:
            self.set_entrance(Direction.NORTH)
            return

    def rotate_tile(self):
        for door in self.doors:
            if door == Direction.NORTH:
                self.change_door_position(
                    self.doors.index(door), Direction.EAST)
            if door == Direction.EAST:
                self.change_door_position(
                    self.doors.index(door), Direction.SOUTH)
            if door == Direction.SOUTH:
                self.change_door_position(
                    self.doors.index(door), Direction.WEST)
            if door == Direction.WEST:
                self.change_door_position(
                    self.doors.index(door), Direction.NORTH)
