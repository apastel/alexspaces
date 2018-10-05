# Raspberry Pi Python sense hat snake

A project to create a Snake game on a Raspberry Pi using a Sense Hat.

## Requirements

This package requires the following system packages to be installed:

- python-pip
- python-dev

## Installation

Begin by installing this packages requirements:

    pip install -e .

Finally copy the example configuration file `example.config.py`, and save it as `config.py`

    cp sensehatsnake/example.config.py sensehatsnake/config.py

## Configuration

You can now configure Sense-Hat-Snake in a few simple steps. Open `sensehatsnake/config.py` and update the options as needed.

- `columns` - The number of columns the board has.
- `rows` - The number of rows the board has.
- `fps` - The games frames per second.
- `countdown` - The game countdown in seconds.
- `interval` - The game tick interval in milliseconds.
- `score_increment` - The number to increment score by in game.
- `level_increment` - The score when to increment the level by in game.
- `interval_increment` - The number to reduce the game tick interval by in milliseconds.

## Usage

It's really as simple as running the main file

    sudo python sensehatsnake/main.py

### License

Sense-Hat-Snake is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT)