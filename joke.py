import random
import psutil
import time
from faces import normal, happy, sad

jokes = [
    "What happens to a frog's car when it breaks down? It gets toad away",
    "Why was six scared of seven? Because seven eight nine",
    "What do you call a bear with no teeth? A gummy bear",
    "How do you count cows? With a cowculator",
    "How do astronomers organize a party? They planet",
    "Why does Humpty Dumpty love autumn? Because Humpty Dumpty had a great fall",
    "I went to the bank the other day and asked the banker to check my balance, so she pushed me!",
    "Can a kangaroo jump higher than the Empire State Building? Of course. The Empire State Building can't jump",
    "Did you hear about the kidnapping at school? It's okay. He woke up",
    "A man got hit in the head with a can of Coke, but he was alright because it was a soft drink",
    "Why was six afraid of seven? Because seven is a convicted rapist",
    "I spent the last two years looking for my ex-girlfriend's killer. *Sigh* But no one will do it"
    "An Irishman walks out of a bar",
    "What's red and smells like blue pain? Red paint.",
    "A dyslexic man walks into a bra",
    "Why was six afraid of seven? It wasn't. Numbers are not sentient and thus incapable of feeling fear",
    "What would George Washington do if he were alive today? Scream and scratch at the top of his coffin",
    "A horse walks into a bar. Several people get up and leave as they spot the potential danger of the situation"
]

colors = [
    [255, 255, 255], # white
    [255, 0, 0],  # red
    [0, 255, 0],  # green
    [0, 0, 255]  # blue
]

def show_joke(sense, marquee_proc):
    random_color = random.choice(colors)
    sense.show_message("Joke Time!", 0.05, random_color)
    joke = random.choice(jokes)
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
