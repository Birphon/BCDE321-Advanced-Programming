class Tile:
    def __init__(self, name, x=16, y=16, effect=None, doors=None, entrance=None):  # Added default arguments - Daniel
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
        if self.entrance == dir.NORTH:
            self.set_entrance(dir.EAST)
            return
        if self.entrance == dir.SOUTH:
            self.set_entrance(dir.WEST)
            return
        if self.entrance == dir.EAST:
            self.set_entrance(dir.SOUTH)
            return
        if self.entrance == dir.WEST:
            self.set_entrance(dir.NORTH)
            return

    def rotate_tile(self):
        for door in self.doors:
            if door == dir.NORTH:
                self.change_door_position(self.doors.index(door), dir.EAST)
            if door == dir.EAST:
                self.change_door_position(self.doors.index(door), dir.SOUTH)
            if door == dir.SOUTH:
                self.change_door_position(self.doors.index(door), dir.WEST)
            if door == dir.WEST:
                self.change_door_position(self.doors.index(door), dir.NORTH)
