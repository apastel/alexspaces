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
]

def show_joke(sense, marquee_proc):
    sense.show_message("Joke Time!", 0.06, [255,255,0])
    joke = random.choice(jokes)
    sense.show_message(joke, 0.06,[255,255,0])
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
