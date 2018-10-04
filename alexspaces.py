import atexit
import os
import subprocess
import threading
import time
import psutil
import rainbow
import joke
import snake.src.main as Snake
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

def auto_marquee():
    try:
        while True:
            sense.show_message("Welcome to AlexSpaces at Molly Hearts!", 0.07)
            sense.show_message("The current temp is " + get_normalized_temp(), 0.07)
    finally:
        clear_on_shutdown()

def pause_marquee():
    psutil.Process(marquee_proc.pid).suspend()

def resume_marquee():
    psutil.Process(marquee_proc.pid).resume()

def accept_input():
    try:
        rainbow_proc = Process(name='show_rainbow', target=rainbow.show_rainbow, args=())
        joke_proc = Process(name='show_joke', target=joke.show_joke, args=(sense,marquee_proc))
        snake_proc = Process(name='snake', target=Snake.main, args=(sense,))
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'BTN_BASE' and event.state == 1:
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
                if event.code == 'BTN_BASE3' and event.state == 1:
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
                if event.code == 'BTN_TOP' and event.state == 1:
                    pause_marquee()
                    if joke_proc.pid is not None:
                        joke_proc.terminate()
                    if snake_proc.pid is not None:
                        psutil.Process(snake_proc.pid).suspend()
                    if rainbow_proc.pid is None:
                        rainbow_proc.start()
                    elif psutil.Process(rainbow_proc.pid).status() == psutil.STATUS_STOPPED or psutil.Process(rainbow_proc.pid).status() == psutil.STATUS_SLEEPING:
                        psutil.Process(rainbow_proc.pid).resume()

    finally:
        clear_on_shutdown()

sense.set_rotation(180)
sense.load_image("heart.png")
time.sleep(3)

marquee_proc = Process(name='auto_marquee', target=auto_marquee, args=())
input_proc = Process(name='accept_intput', target=accept_input, args=())
marquee_proc.start()
input_proc.start()

