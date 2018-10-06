from __future__ import print_function


class Board:
    COLUMNS = None

    ROWS = None

    COORDINATES = None

    def __init__(self, columns, rows):
        ##print("[Board][info] Initialising Board")

        self.COLUMNS = columns
        self.ROWS = rows
        self.__generate()

    def __generate(self):
        self.COORDINATES = [
            [0 for x in xrange(self.COLUMNS)]
            for y in xrange(self.ROWS)
        ]

    def columns(self):
        #print("[Board][info] Getting Board columns")

        return self.COLUMNS

    def rows(self):
        #print("[Board][info] Getting Board rows")

        return self.ROWS

    def coordinates(self):
        #print("[Board][info] Getting Board coordinates")

        return self.COORDINATES

    def check_collision(self, snake, offset):
        #print("[Board][info] Checking for Snake collision")

        offset_x, offset_y = offset

        if 0 > offset_x or offset_x > self.ROWS - 1 or 0 > offset_y or offset_y > self.COLUMNS - 1:
            return True
        else:
            for segment in snake.segments():
                if segment[0] == offset_x and segment[1] == offset_y:
                    return True

        return False

    def clear(self):
        #print("[Board][info] Clearing board")

        self.COORDINATES = None
        self.COLUMNS = None
        self.ROWS = None

    def cleanup(self):
        #print("[Board][info] Board clean up")

        self.clear()

    def __exit__(self):
        #print("[Board][info] Board exit")

        self.cleanup()
