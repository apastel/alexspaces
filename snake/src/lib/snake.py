

class Snake:
    COORDINATES = None

    SEGMENTS = None

    X = None
    Y = None

    DIRECTION = None

    DIRECTION_UP = 'up'
    DIRECTION_DOWN = 'down'
    DIRECTION_LEFT = 'left'
    DIRECTION_RIGHT = 'right'

    def __init__(self, coordinates, x=0, y=0, direction=DIRECTION_LEFT):
        #print("[Snake][info] Initialising Snake")

        self.COORDINATES = coordinates
        self.SEGMENTS = []
        self.add_segment((x, y))
        self.X = x
        self.Y = y
        self.DIRECTION = direction

    def set_coordinates(self, coordinates):
        #print("[Snake][info] Setting Snake coordinates")

        self.COORDINATES = coordinates

    def set_direction(self, direction):
        #print("[Snake][info] Setting Snake direction")

        self.DIRECTION = direction

    def set_x(self, x):
        #print("[Snake][info] Setting Snake X position")

        if self.length() > 1:
            self.remove_segment(-1)
            self.add_segment((x, self.SEGMENTS[0][1]), 0)
        else:
            self.SEGMENTS[0] = (x, self.SEGMENTS[0][1])

        self.X = x

    def set_y(self, y):
        #print("[Snake][info] Setting Snake Y position")

        if self.length() > 1:
            self.remove_segment(-1)
            self.add_segment((self.SEGMENTS[0][0], y), 0)
        else:
            self.SEGMENTS[0] = (self.SEGMENTS[0][0], y)

        self.Y = y

    def set_position(self, coordinates):
        #print("[Snake][info] Setting Snake X, Y position")

        x, y = coordinates

        if self.length() > 1:
            self.remove_segment(-1)
            self.add_segment(coordinates, 0)
        else:
            self.SEGMENTS[0] = coordinates

        self.X = x
        self.Y = y

    def add_segment(self, coordinates, position=-1):
        #print("[Snake][info] Creating Snake segment at index %d" % (position))

        self.SEGMENTS.insert(position if position != -1 else len(self.SEGMENTS), coordinates)

    def remove_segment(self, position=-1):
        #print("[Snake][info] Removing Snake segment at index %d" % (position))

        self.SEGMENTS.pop(position)

    def coordinates(self, columns=0, rows=0):
        #print("[Snake][info] Getting Snake coordinates")

        if columns == 0 and rows == 0:
            return self.COORDINATES

        coordinates = [
            [False for x in xrange(columns)]
            for y in xrange(rows)
        ]

        for segment in self.SEGMENTS:
            coordinates[segment[1]][segment[0]] = self.COORDINATES[0][0]

        return coordinates

    def direction(self):
        #print("[Snake][info] Getting Snake direction")

        return self.DIRECTION

    def x(self):
        #print("[Snake][info] Getting Snake X position")

        return self.X

    def y(self):
        #print("[Snake][info] Getting Snake Y position")

        return self.Y

    def position(self):
        #print("[Snake][info] Getting Snake X,Y position")

        return (self.X, self.Y)

    def segments(self):
        #print("[Snake][info] Getting all Snake segments")

        return self.SEGMENTS

    def head(self):
        #print("[Snake][info] Getting Snake head")

        return self.SEGMENTS[0]

    def body(self):
        #print("[Snake][info] Getting Snake body")

        if len(self.SEGMENTS) < 2:
            return None

        return self.SEGMENTS[1:]

    def tail(self):
        #print("[Snake][info] Getting Snake tail")

        return self.SEGMENTS[-1]

    def length(self):
        #print("[Snake][info] Getting Snake length")

        return len(self.SEGMENTS)

    def clear(self):
        #print("[Snake][info] Clearing Snake")

        self.COORDINATES = None
        self.SEGMENTS = None
        self.X = None
        self.Y = None
        self.DIRECTION = None

    def cleanup(self):
        #print("[Snake][info] Snake clean up")

        self.clear()

    def __exit__(self):
        #print("[Snake][info] Snake exit")

        self.cleanup()
