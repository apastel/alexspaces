from __future__ import print_function
from sensehatsnake.lib.apple import Apple
import unittest


class AppleTestCase(unittest.TestCase):
    COORDINATES = [
        [1]
    ]

    apple = None

    def setUp(self):
        self.apple = Apple(self.COORDINATES)

    def test__init__(self):
        self.assertIsInstance(self.apple, Apple)

    def test_set_coordinates(self):
        self.assertIs(self.apple.set_coordinates([[0]]), None)
        self.assertEquals(self.apple.coordinates(), [[0]])

    def test_set_x(self):
        self.assertIs(self.apple.set_x(1), None)
        self.assertEquals(self.apple.x(), 1)

    def test_set_y(self):
        self.assertIs(self.apple.set_y(1), None)
        self.assertEquals(self.apple.y(), 1)

    def test_set_position(self):
        self.assertIs(self.apple.set_position((1, 1)), None)
        self.assertEquals(self.apple.x(), 1)
        self.assertEquals(self.apple.y(), 1)

    def test_coordinates(self):
        self.assertEquals(self.apple.coordinates(), self.COORDINATES)

    def test_x(self):
        self.assertEquals(self.apple.x(), 0)

    def test_y(self):
        self.assertEquals(self.apple.y(), 0)

    def test_position(self):
        self.assertEquals(self.apple.position(), (0, 0))

    def test_cleanup(self):
        self.assertIs(self.apple.cleanup(), None)

    def test__exit__(self):
        self.assertIs(self.apple.__exit__(), None)


if __name__ == '__main__':
    unittest.main()
