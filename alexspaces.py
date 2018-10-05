import atexit
import os
import subprocess
import random
import time
import psutil
import rainbow
import joke
import datetime
import snake.src.main as Snake
from sense_hat import SenseHat
from inputs import get_gamepad
from multiprocessing import Process, Event
from time import localtime, strftime

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

messages = [
    "The current temp is " + get_normalized_temp() +".",
    "AlexSpaces is not responsible for seizures, hallucinations, or motion sickness experienced while viewing AlexSpaces.",
    "Bored? Why not read the AlexSpaces binder!",
    "If you can read this, you don't need glasses.",
    "Yoga is on Sunday morning with Justice Klein. Namaste.",
    "Molly Hearts lineup features Arielle Z, Artifax, Chrysocolla, Drummer John, Eric Medina b2b JNAV, Miguel Rios, MRNG, Sparrow, The Potted Plants, and Metallica",
    "Bored? Check out Kirsten's fantastic rack!",
    "Why are you still reading this? Go party!",
    "What is AlexSpaces anyway? Hell if I know...",
    "How do you turn this thing off? It's too bright.",
    "Please kill me, Alex only programmed me to feel pain and nothing else.",
    "Ready for the Saturday hike? Oh shit it happened already? Fuck.",
    "Remember to stake down your tent when it gets windy or you're totally fucked!",
    "Our current GPS coordinates are...just kidding I have no fucking clue.",
    "The current time is " + strftime("%I:%M%P", localtime()),
    "Press Left C to go on a mushroom trip!",
    "Press A to hear a bad joke!",
    "Press B to play Snake!",
    "Press Z and absolutely nothing will happen!"
]

colors = [
    [255, 255, 255], # white
    [255, 0, 0],  # red
    [0, 255, 0],  # green
    [0, 0, 255]  # blue
]

def show_marquee():
    sense.show_message("Welcome to AlexSpaces at Molly Hearts!", 0.05)
    while True:
        message = random.choice(messages)
        sense.show_message(message, 0.05, random.choice(colors))

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
                if event.code == 'BTN_BASE' and event.state == 1 and not playing_snake:
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
                    else:
                        playing_snake = False
                        psutil.Process(snake_proc.pid).suspend()
                        resume_marquee()
                if event.code == 'BTN_TOP' and event.state == 1 and not playing_snake:
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

marquee_proc = Process(name='auto_marquee', target=show_marquee, args=())
input_proc = Process(name='accept_intput', target=accept_input, args=())
marquee_proc.start()
input_proc.start()

