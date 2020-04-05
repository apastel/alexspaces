import random
import psutil
import time
from messages import jokes
from faces import normal, happy, sad

colors = [
    [255, 255, 255], # white
    [255, 0, 0],  # red
    [0, 255, 0],  # green
    [0, 0, 255]  # blue
]

def show_joke(sense, marquee_proc):
    random_color = random.choice(colors)
    sense.show_message("Joke Time!", 0.05, random_color)
    joke = random.choice(jokes.joke_list)
    sense.show_message(joke, 0.05, random_color)
    sense.set_pixels(happy)
    time.sleep(0.5)
    sense.clear()
    time.sleep(0.5)
    sense.set_pixels(happy)
    time.sleep(0.5)
    sense.clear()
    time.sleep(0.5)
    sense.set_pixels(happy)
    time.sleep(1)
    sense.clear()
    psutil.Process(marquee_proc.pid).resume()
