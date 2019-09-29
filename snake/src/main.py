from __future__ import print_function
from .lib.game import Game
import atexit
from . import config
from sense_hat import SenseHat


def main(sense):
    game = Game(
        config.game['columns'],
        config.game['rows'],
        config.game['fps'],
        config.game['countdown'],
        config.game['interval'],
        config.game['score_increment'],
        config.game['level_increment'],
        config.game['interval_increment'],
        sense
    )

    game.start()

    atexit.register(game.__exit__)


if __name__ == '__main__':
    sense = SenseHat()
    sense.set_rotation(180)
    main(sense)
