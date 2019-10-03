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

images = {
    "heart": "heart.png"
}

messages = [
    "The current temp is " + get_normalized_temp() +".",
    "The current temp is " + get_normalized_temp() +".",
    "The current temp is " + get_normalized_temp() +".",
    "AlexSpaces is not responsible for seizures, hallucinations, or motion sickness experienced while viewing AlexSpaces.",
    "Bored? Why not read the AlexSpaces binder!",
    "If you can read this, you don't need glasses.",
    "Molly Hearts lineup features Arielle Z, Chrysocolla, Drummer John, Sparrow, Molly Hearts (Rap Performance), and Metallica",
    "Bored? Check out Kirsten's rack!",
    "Why are you still reading this? Go party!",
    "What is AlexSpaces anyway? Hell if I know...",
    "How do you turn this thing off? It's too bright.",
    "Please kill me, Alex only programmed me to feel pain and nothing else.",
    "Our current GPS coordinates are...just kidding I have no fucking clue.",
    "The current time is " + strftime("%I:%M%P", localtime()),
    "Press C-Left to go on a mushroom trip!",
    "Press A to hear a bad joke!",
    "Press B to play Snake!",
    "Press Z and absolutely nothing will happen!",
    "If you can read this, you are way too sober.",
    "I wonder if anyone is still reading this.",
    "You think you're so cool with your \"3rd dimension\". Nerd.",
    "What's your high score in Snake? Mine is 5....th-thousand. 5 thousand.",
    "Welcome to AlexSpaces at Molly Hearts!",
    "Please don't put me near the fire again.",
    "I've got a fever, and the only prescription is ibuprofen!",
    "Check out the fire performances!",
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
                    sense.show_message("The current temp is ", 0.05, random_color)
                    sense.show_message(temp, 0.05, random_color)
                    sense.show_message(temp, 0.05, random_color)
                    sense.show_message(temp, 0.05, random_color)
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

sense.load_image(images.get("heart"))
time.sleep(3)

marquee_proc = Process(name='auto_marquee', target=show_marquee, args=())
input_proc = Process(name='accept_intput', target=accept_input, args=())
marquee_proc.start()
input_proc.start()

