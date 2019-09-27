from __future__ import print_function
from .board import Board
from .apple import Apple
from mock import MagicMock, patch
from random import randint
from .snake import Snake
from tinydb import TinyDB, Query
from inputs import get_gamepad
import math
import pygame
import sys


# try:
#     from sense_hat import SenseHat
# except ImportError:
#     #print("[Game][error] An error occurred importing 'sense_hat.SenseHat'")
#     mock = MagicMock()
#     mock.clear.return_value = True
#     mock.set_pixel.return_value = True
#     mock.show_message.return_value = True

#     with patch.dict('sys.modules', {'sense_hat': mock, 'sense_hat.SenseHat': mock.RTIMU}):
#         from sense_hat import SenseHat


class Game:
    BLOCK_SIZE = 36

    COLUMNS = 8
    ROWS = 8

    FPS = None

    COLORS = [
        # 0 - Black
        (0, 0, 0),
        # 1 - Green
        (0, 255, 0),
        # 2 - Red
        (255, 0, 0),
        # 3 - Purple
        (128, 0, 128),
        # 4 - Blue
        (0, 0, 255),
        # 5 - Orange
        (255, 165, 0),
        # 6 - Cyan
        (0, 255, 255),
        # 7 - Yellow
        (255, 255, 0),
        # 8 - Dark Grey
        (35, 35, 35),
        # 9 - White
        (255, 255, 255)
    ]

    SHAPES = [
        # Snake
        [
            [1],
        ],

        # Apple
        [
            [2]
        ],
    ]

    WIDTH = None
    HEIGHT = None

    COUNTDOWN = None

    SCORE_INCREMENT = None

    SCORE = 0
    APPLES = 0

    INTERVAL = None
    INTERVAL_INCREMENT = None

    LEVEL = 1
    LEVEL_INCREMENT = None

    PAUSED = False

    GAMEOVER = False

    BACKGROUND_GRID = None

    SNAKE_MOVED = True

    pygame = None
    pygame_font = None
    pygame_screen = None
    sensehat = None
    db = None

    board = None
    snake = None
    apple = None

    def __init__(self, columns, rows, fps, countdown, interval, score_increment, level_increment, interval_increment, sense, pygame_instance=None):
        self.COLUMNS = columns
        self.ROWS = rows
        self.FPS = fps
        self.COUNTDOWN = countdown
        self.INTERVAL = interval
        self.SCORE_INCREMENT = score_increment
        self.LEVEL_INCREMENT = level_increment
        self.INTERVAL_INCREMENT = interval_increment

        if pygame_instance is None:
            self.pygame = pygame
        else:
            self.pygame = pygame_instance

        self.sensehat = sense

        self.db = TinyDB('snake/data/database.json')

        try:
            self.WIDTH = self.BLOCK_SIZE * self.COLUMNS + 150
            self.HEIGHT = self.BLOCK_SIZE * self.ROWS

            self.BACKGROUND_GRID = [
                [8 if x % 2 == y % 2 else 0 for x in range(self.COLUMNS)]
                for y in range(self.ROWS)
            ]

            self.pygame.init()
            self.pygame.key.set_repeat(0, 0)
            self.pygame_font = self.pygame.font.Font(self.pygame.font.get_default_font(), 12)
            self.pygame_screen = self.pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 24)
            self.pygame.event.set_blocked(self.pygame.MOUSEMOTION)
            self.pygame.joystick.init()
            self.gamepad = self.pygame.joystick.Joystick(0)
            self.gamepad.init()

            self.board = Board(self.COLUMNS, self.ROWS)
            self.__generate_snake()
            self.__generate_apple()
            self.__display_message("Snake")
        except AttributeError:
            print("[Game][error] An error occurred initialising game")

    def start(self, run_once=False):
        #print("[Game][info] Starting game")

        try:
            self.pygame.event.get()
            self.pygame_screen.fill(self.COLORS[0])
            self.pygame.display.update()

            self.sensehat.clear()
        except AttributeError:
            print("[Game][error] An error occurred starting game")

        self.__countdown()
        self.__loop()
        self.finish()

        if run_once is not True:
            self.start()

    def __countdown(self):
        #print("[Game][info] Starting game countdown")
        self.__display_message("Ready...Go!")

    def __loop(self):
        #print("[Game][info] Starting game loop")

        try:
            self.pygame.time.set_timer(pygame.USEREVENT + 1, self.INTERVAL)

            key_actions = {
                'ESCAPE': lambda: self.quit(),
                'LEFT': lambda: self.__direction_left(),
                'RIGHT': lambda: self.__direction_right(),
                'DOWN': lambda: self.__direction_down(),
                'UP': lambda: self.__direction_up(),
                'p': lambda: self.toggle_pause(),
            }

            pygame_clock = self.pygame.time.Clock()

            while not self.GAMEOVER:
                self.sensehat.clear()
                self.pygame_screen.fill(self.COLORS[0])

                if self.PAUSED:
                    self.__display_message("Paused")
                else:
                    self.__draw_line(
                        ((self.BLOCK_SIZE * self.COLUMNS) + 1, 0),
                        ((self.BLOCK_SIZE * self.COLUMNS) + 1, (self.HEIGHT - 1)),
                        self.COLORS[9]
                    )

                    self.__display_message(
                        "Score: %d\n\nLevel: %d\n\nApples: %d" % (self.SCORE, self.LEVEL, self.APPLES),
                        ((self.BLOCK_SIZE * self.COLUMNS) + self.BLOCK_SIZE, 2),
                        self.COLORS[9],
                        self.COLORS[0],
                        False
                    )

                    self.__draw_matrix(self.BACKGROUND_GRID, (0, 0), None, False)
                    self.__draw_matrix(self.board.coordinates(), (0, 0), None, False)
                    self.__draw_matrix(self.snake.coordinates(self.COLUMNS, self.ROWS), (0, 0))
                    self.__draw_matrix(self.apple.coordinates(), (self.apple.x(), self.apple.y()))

                self.pygame.display.update()

                for event in self.pygame.event.get():
                    if event.type == self.pygame.USEREVENT + 1:
                        self.__move()
                    elif event.type == self.pygame.JOYHATMOTION:
                        if self.gamepad.get_hat(0) == (-1, 0):
                            key_actions['LEFT']()
                        elif self.gamepad.get_hat(0) == (1, 0):
                            key_actions['RIGHT']()
                        elif self.gamepad.get_hat(0) == (0, -1):
                            key_actions['DOWN']()
                        elif self.gamepad.get_hat(0) == (0, 1):
                            key_actions['UP']()
                    elif event.type == self.pygame.JOYAXISMOTION:
                        if self.gamepad.get_axis(0) < -0.7:
                            key_actions['LEFT']()
                        elif self.gamepad.get_axis(0) > 0.7:
                            key_actions['RIGHT']()
                        elif self.gamepad.get_axis(1) > 0.7:
                            key_actions['DOWN']()
                        elif self.gamepad.get_axis(1) < -0.7:
                            key_actions['UP']()

                pygame_clock.tick(self.FPS)
        except AttributeError:
            print("[Game][error] An error occurred during game loop")

    def __generate_snake(self):
        #print("[Game][info] Generating snake")

        self.snake = Snake(self.SHAPES[0], int(math.floor(self.COLUMNS / 2)), int(math.floor(self.ROWS / 2)))

    def __generate_apple(self):
        #print("[Game][info] Generating apple")

        apple_collision = True
        offset_x, offset_y = (0, 0)

        while apple_collision:
            offset_x = randint(0, self.ROWS - 1)
            offset_y = randint(0, self.COLUMNS - 1)

            apple_collision = self.board.check_collision(self.snake, (offset_x, offset_y))

        self.apple = Apple(self.SHAPES[1], offset_x, offset_y)

    def __display_message(self, message, coordinates=None, color=COLORS[9], background_color=COLORS[0], sensehat=True):
        #print("[Game][info] Displaying message")

        if sensehat:
            self.sensehat.show_message(message, text_colour=color, scroll_speed=0.05)

        for i, line in enumerate(message.splitlines()):
            message_image = self.pygame_font.render(line, False, color, background_color)

            if coordinates is not None:
                position_x, position_y = coordinates
            else:
                message_image_center_x, message_image_center_y = message_image.get_size()
                message_image_center_x //= 2
                message_image_center_y //= 2
                position_x = self.WIDTH // 2 - message_image_center_x
                position_y = self.HEIGHT // 2 - message_image_center_y

            self.pygame_screen.blit(
                message_image,
                (position_x, position_y + i * 22)
            )

    def __draw_line(self, start_position, end_position, color=COLORS[9], sensehat=True):
        #print("[Game][info] Drawing line")

        if sensehat:
            start_x, start_y = start_position
            end_x, end_y = start_position

            for i in range(start_y, end_y):
                for j in range(start_x, end_x):
                    if start_x == end_x or start_y == end_y:
                        self.sensehat.set_pixel(j, i, color)

        self.pygame.draw.line(self.pygame_screen, color, start_position, end_position)

    def __draw_matrix(self, matrix, offset, color=None, sensehat=True):
        #print("[Game][info] Drawing matrix")

        offset_x, offset_y = offset

        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    if color is None:
                        shape_color = self.COLORS[val]
                    else:
                        shape_color = color

                    if sensehat:
                        self.sensehat.set_pixel((offset_x + x), (offset_y + y), shape_color)

                    self.pygame.draw.rect(
                        self.pygame_screen,
                        shape_color,
                        self.pygame.Rect((offset_x + x) * self.BLOCK_SIZE, (offset_y + y) * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE),
                        0
                    )

    def __count_clear_apples(self, apples):
        #print("[Game][info] Counting cleared apples")

        if apples > 0:
            self.APPLES += apples
            self.SCORE += self.SCORE_INCREMENT * self.LEVEL

        if self.APPLES >= self.LEVEL * self.LEVEL_INCREMENT:
            self.LEVEL += 1
            delay = self.INTERVAL - self.INTERVAL_INCREMENT * (self.LEVEL - 1)
            delay = 100 if delay < 100 else delay
            self.pygame.time.set_timer(self.pygame.USEREVENT + 1, delay)

    def __move(self):
        #print("[Game][info] Moving snake %s" % (self.snake.direction()))

        if not self.GAMEOVER and not self.PAUSED:
            new_x, new_y = self.snake.head()

            if self.snake.direction() == self.snake.DIRECTION_UP:
                new_y = self.snake.y() - 1
            elif self.snake.direction() == self.snake.DIRECTION_DOWN:
                new_y = self.snake.y() + 1
            elif self.snake.direction() == self.snake.DIRECTION_LEFT:
                new_x = self.snake.x() - 1
            elif self.snake.direction() == self.snake.DIRECTION_RIGHT:
                new_x = self.snake.x() + 1

            if self.board.check_collision(self.snake, (new_x, new_y)):
                self.GAMEOVER = True

                return False

            tail_x, tail_y = self.snake.tail()
            self.snake.set_position((new_x, new_y))
            cleared_apples = 0

            if new_x == self.apple.x() and new_y == self.apple.y():
                self.snake.add_segment((tail_x, tail_y))
                cleared_apples += 1
                self.__generate_apple()

            self.__count_clear_apples(cleared_apples)
            self.SNAKE_MOVED = True

            return True

    def __direction_up(self):
        #print("[Game][info] Event direction up")

        if self.snake.direction() != self.snake.DIRECTION_DOWN and self.SNAKE_MOVED is True:
            self.snake.set_direction(self.snake.DIRECTION_UP)
            self.SNAKE_MOVED = False

    def __direction_down(self):
        #print("[Game][info] Event direction down")

        if self.snake.direction() != self.snake.DIRECTION_UP and self.SNAKE_MOVED is True:
            self.snake.set_direction(self.snake.DIRECTION_DOWN)
            self.SNAKE_MOVED = False

    def __direction_left(self):
        #print("[Game][info] Event direction left")

        if self.snake.direction() != self.snake.DIRECTION_RIGHT and self.SNAKE_MOVED is True:
            self.snake.set_direction(self.snake.DIRECTION_LEFT)
            self.SNAKE_MOVED = False

    def __direction_right(self):
        #print("[Game][info] Event direction right")

        if self.snake.direction() != self.snake.DIRECTION_LEFT and self.SNAKE_MOVED is True:
            self.snake.set_direction(self.snake.DIRECTION_RIGHT)
            self.SNAKE_MOVED = False

    def toggle_pause(self):
        #print("[Game][info] Toggling paused state")

        self.PAUSED = not self.PAUSED

    def get_score(self):
        #print("[Game][info] Calculating score")

        return self.SCORE

    def print_score(self, high_score=False):
        #print("[Game][info] Printing score")

        score = self.get_score()

        try:
            self.sensehat.clear()
            self.pygame_screen.fill(self.COLORS[0])

            if high_score:
                self.__display_message("Game Over!\n\nHigh score: %d" % score)
                self.pygame.display.update()
            else:
                self.__display_message("Game Over!\n\nScore: %d!" % self.get_score())
                self.pygame.display.update()

            # self.pygame.time.wait(3000)
        except AttributeError:
            print("[Game][error] An error occurred printing score")

    def finish(self):
        #print("[Game][info] Finishing game")

        score = self.get_score()

        self.pygame.display.update()

        if self.db.contains(Query().score >= score):
            self.print_score()
        else:
            self.print_score(True)

        self.db.insert({'score': score})
        self.reset()

    def quit(self):
        #print("[Game][info] Quitting game")

        self.pygame_screen.fill(self.COLORS[0])
        self.sensehat.clear()
        self.__display_message("Exiting...")
        self.pygame.display.update()
        sys.exit()
    def reset(self):
        #print("[Game][info] Resetting game")

        self.PAUSED = False
        self.GAMEOVER = False
        self.SCORE = 0
        self.APPLES = 0
        self.LEVEL = 1
        self.SNAKE_MOVED = True

        self.board = Board(self.COLUMNS, self.ROWS)
        self.snake = None
        self.apple = None
        self.__generate_snake()
        self.__generate_apple()

        self.sensehat.clear()
        self.pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        self.pygame.display.update()

    def cleanup(self):
        #print("[Game][info] Game clean up")

        try:
            self.sensehat.clear()
            self.pygame_screen.fill(self.COLORS[0])
            self.pygame.display.update()
            self.pygame.quit()
        except AttributeError:
            print("[Game][error] An error occurred cleaning up")

    def __exit__(self):
        #print("[Game][info] Game exit")
        print("in exit")
        self.cleanup()
