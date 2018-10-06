from __future__ import print_function
from sensehatsnake.lib.snake import Snake
import unittest


class SnakeTestCase(unittest.TestCase):
    COORDINATES = [
        [1]
    ]

    COLUMNS = 2
    ROWS = 2

    snake = None

    def setUp(self):
        self.snake = Snake(self.COORDINATES)

    def test__init__(self):
        self.assertIsInstance(self.snake, Snake)

    def test_set_coordinates(self):
        self.assertIs(self.snake.set_coordinates([[0]]), None)
        self.assertEquals(self.snake.coordinates(), [[0]])

    def test_set_direction(self):
        self.assertIs(self.snake.set_direction(self.snake.DIRECTION_UP), None)
        self.assertEquals(self.snake.direction(), self.snake.DIRECTION_UP)

    def test_set_x(self):
        self.assertIs(self.snake.set_x(1), None)
        self.assertEquals(self.snake.x(), 1)

    def test_set_y(self):
        self.assertIs(self.snake.set_y(1), None)
        self.assertEquals(self.snake.y(), 1)

    def test_set_position(self):
        self.assertIs(self.snake.set_position((1, 1)), None)
        self.assertEquals(self.snake.x(), 1)
        self.assertEquals(self.snake.y(), 1)

    def test_add_segment(self):
        self.assertIs(self.snake.add_segment((1, 1)), None)
        self.assertEquals(self.snake.length(), 2)

    def test_remove_segment(self):
        self.assertIs(self.snake.remove_segment(), None)
        self.assertEquals(self.snake.length(), 0)

    def test_coordinates(self):
        self.assertEquals(self.snake.coordinates(), self.COORDINATES)
        self.assertEquals(self.snake.coordinates(self.COLUMNS, self.ROWS), [[self.COORDINATES[0][0], False], [False, False]])

    def test_direction(self):
        self.assertEquals(self.snake.direction(), self.snake.DIRECTION_LEFT)

    def test_x(self):
        self.assertEquals(self.snake.x(), 0)

    def test_y(self):
        self.assertEquals(self.snake.y(), 0)

    def test_position(self):
        self.assertEquals(self.snake.position(), (0, 0))

    def test_segments(self):
        self.assertEquals(self.snake.segments(), [(0, 0)])

    def test_head(self):
        self.assertEquals(self.snake.head(), (0, 0))

    def test_body(self):
        self.assertEquals(self.snake.body(), None)

    def test_tail(self):
        self.assertEquals(self.snake.tail(), (0, 0))

    def test_length(self):
        self.assertEquals(self.snake.length(), 1)

    def test_cleanup(self):
        self.assertIs(self.snake.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.snake.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
