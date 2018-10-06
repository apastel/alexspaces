from __future__ import print_function


class Apple:
    COORDINATES = None

    X = None
    Y = None

    def __init__(self, coordinates, x=0, y=0):
        #print("[Apple][info] Initialising Apple")

        self.COORDINATES = coordinates
        self.X = x
        self.Y = y

    def set_coordinates(self, coordinates):
        #print("[Apple][info] Setting Apple coordinates")

        self.COORDINATES = coordinates

    def set_x(self, x):
        #print("[Apple][info] Setting Apple X position")

        self.X = x

    def set_y(self, y):
        #print("[Apple][info] Setting Apple Y position")

        self.Y = y

    def set_position(self, coordinates):
        #print("[Apple][info] Setting Apple X, Y position")

        x, y = coordinates

        self.X = x
        self.Y = y

    def coordinates(self):
        #print("[Apple][info] Getting Apple coordinates")

        return self.COORDINATES

    def x(self):
        #print("[Apple][info] Getting Apple X position")

        return self.X

    def y(self):
        #print("[Apple][info] Getting Apple Y position")

        return self.Y

    def position(self):
        #print("[Apple][info] Getting Apple X, Y position")

        return (self.X, self.Y)

    def clear(self):
        #print("[Apple][info] Clearing Apple")

        self.COORDINATES = None
        self.X = None
        self.Y = None

    def cleanup(self):
        #print("[Apple][info] Apple clean up")

        self.clear()

    def __exit__(self):
        #print("[Apple][info] Apple exit")

        self.cleanup()
