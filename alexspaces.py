import atexit
import os
import yaml
import subprocess
import random
import time
import psutil
import rainbow
import joke
import datetime
import snake.src.main as Snake
import messages.marquee as marquee
from sense_hat import SenseHat
from inputs import get_gamepad
from multiprocessing import Process, Event

sense = SenseHat()

@atexit.register
def clear_on_shutdown():
    sense.clear()

def get_normalized_temp():
    cpu_temp = int(subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)) / 1000
    average_temp = (sense.get_temperature_from_pressure() + sense.get_temperature_from_humidity()) / 2
    display_temp_celsius = average_temp - (cpu_temp - average_temp)
    display_temp_fahrenheit = display_temp_celsius * 9/5 + 32
    return str(int(round(display_temp_fahrenheit)))

images = {
    "heart": "resources/heart.png"
}

colors = [
    [255, 255, 255], # white
    [255, 0, 0],  # red
    [0, 255, 0],  # green
    [0, 0, 255]  # blue
]

def show_marquee():
    sense.show_message(f"Welcome to AlexSpaces at {config['event_name']}!", config['scroll_speed'])
    messages = marquee.marquee_messages + marquee.couchella_messages
    while True:
        message = random.choice(messages)
        sense.show_message(message, config['scroll_speed'], random.choice(colors))
        time.sleep(0.5)
        sense.load_image(images.get("heart"))
        time.sleep(2)

def pause_marquee():
    psutil.Process(marquee_proc.pid).suspend()

def resume_marquee():
    psutil.Process(marquee_proc.pid).resume()

def accept_input():
    try:
        rainbow_proc = Process(name='show_rainbow', target=rainbow.show_rainbow, args=())
        joke_proc = Process(name='show_joke', target=joke.show_joke, args=(sense,marquee_proc))
        snake_proc = Process(name='snake', target=Snake.main, args=(sense,))
        playing_snake = False
        while True:
            events = get_gamepad()
            for event in events:
                # A button pressed
                if event.code == 'BTN_BASE' and event.state == 1 and not playing_snake:
                    # Show joke
                    pause_marquee()
                    if rainbow_proc.pid is not None:
                        psutil.Process(rainbow_proc.pid).suspend()
                    if snake_proc.pid is not None:
                        psutil.Process(snake_proc.pid).suspend()
                    if joke_proc.pid is None:
                        joke_proc = Process(name='show_joke', target=joke.show_joke, args=(sense,marquee_proc))
                        joke_proc.start()
                    else:
                        joke_proc.terminate()
                        joke_proc = Process(name='show_joke', target=joke.show_joke, args=(sense,marquee_proc))
                        joke_proc.start()
                # B button pressed
                elif event.code == 'BTN_BASE3' and event.state == 1:
                    # Start Snake
                    if not playing_snake:
                        playing_snake = True
                        pause_marquee()
                        if rainbow_proc.pid is not None:
                            psutil.Process(rainbow_proc.pid).suspend()
                        if joke_proc.pid is not None:
                            joke_proc.terminate()
                        if snake_proc.pid is None:
                            snake_proc = Process(name='snake', target=Snake.main, args=(sense,))
                            snake_proc.start()
                        elif psutil.Process(snake_proc.pid).status() == psutil.STATUS_STOPPED or psutil.Process(snake_proc.pid).status() == psutil.STATUS_SLEEPING:
                            psutil.Process(snake_proc.pid).resume()
                    # End snake
                    else:
                        playing_snake = False
                        psutil.Process(snake_proc.pid).suspend()
                        resume_marquee()
                # Left-C pressed
                elif event.code == 'BTN_TOP' and event.state == 1 and not playing_snake:
                    # Show rainbow
                    pause_marquee()
                    if joke_proc.pid is not None:
                        joke_proc.terminate()
                    if snake_proc.pid is not None:
                        psutil.Process(snake_proc.pid).suspend()
                    if rainbow_proc.pid is None:
                        rainbow_proc.start()
                    elif psutil.Process(rainbow_proc.pid).status() == psutil.STATUS_STOPPED or psutil.Process(rainbow_proc.pid).status() == psutil.STATUS_SLEEPING:
                        psutil.Process(rainbow_proc.pid).resume()
                # Up-C pressed
                elif event.code == 'BTN_TRIGGER' and event.state == 1 and not playing_snake:
                    # Show temp
                    pause_marquee()
                    if joke_proc.pid is not None:
                        joke_proc.terminate()
                    if snake_proc.pid is not None:
                        psutil.Process(snake_proc.pid).suspend()
                    if rainbow_proc.pid is not None:
                        psutil.Process(rainbow_proc.pid).suspend()
                    temp = get_normalized_temp()
                    random_color = random.choice(colors)
                    sense.show_message("The current temp is ", config['scroll_speed'], random_color)
                    sense.show_message(temp, config['scroll_speed'], random_color)
                    sense.show_message(temp, config['scroll_speed'], random_color)
                    sense.show_message(temp, config['scroll_speed'], random_color)
                    time.sleep(1)
                    resume_marquee()
                # Z pressed
                elif event.code == "BTN_BASE2" and event.state == 1 and not playing_snake:
                    # Return to marquee
                    if joke_proc.pid is not None:
                        joke_proc.terminate()
                    if rainbow_proc.pid is not None:
                        psutil.Process(rainbow_proc.pid).suspend()
                    if snake_proc.pid is not None:
                        psutil.Process(snake_proc.pid).suspend()
                    resume_marquee()

    finally:
        clear_on_shutdown()

def main():
    global config
    config = yaml.safe_load(open('config.yaml'))
    sense.set_rotation(config['rotation'])
    sense.load_image(images.get("heart"))
    time.sleep(3)

    global marquee_proc
    global input_proc
    marquee_proc = Process(name='auto_marquee', target=show_marquee, args=())
    input_proc = Process(name='accept_intput', target=accept_input, args=())
    marquee_proc.start()
    input_proc.start()

if __name__ == "__main__":
    main()