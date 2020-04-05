# What is AlexSpaces?

## What if there were not one, but two dimensions?
That’s the question that AlexSpaces attempts to answer.  
Imagine a world where the space you move through has not only width, but also length! Thanks to modern advances in computing, you no longer have to imagine it.

Now, it might hurt your head trying to grasp what a 2D world might look like.  
Trying to simulate a 2D environment on a normal LCD screen would be far too overwhelming to the human eye, so we’ve scaled it down to a tiny 8x8 pixel grid capable of displaying one letter at a time. 
Across these 64 pixels moves the words, shapes, and colors that comprise a 2D universe previously only described in books and audio tape. 

## What is this alien-shaped gamepad connected to it? 

![controller](controller.png)

The AlexSpaces Function Controller™ is a futuristic look into the possible world of 2D gaming.  
The confusing layout of the gamepad buttons reflect the hazy future of a world where things aren’t what they seem.  
Some buttons are big, some are different colors, wait there’s a button on the back? What does all this mean?  
Notice the strange three-prong handles...does this mean humans of the future will have three hands? Probably! 

## What is Snake?
Snake is a brand new 2-dimensional game of the future.  
In it, you control a photorealistic python as it navigates a maze, attempting to eat apples (what?) and avoid walls (why?). 
While playing Snake, it is not uncommon to feel like you may have played this exact game before, and possibly on a better screen.  
These types of hallucinatory déjà vu experiences are normal while experiencing AlexSpaces, and may be a sign that you need to take a short break and lie down. 

## This is really boring, what else does it do? Also it said a curse word at my daughter and now...
Thank you for using AlexSpaces. We hope this has been beneficial to you and--
## But wait...
And now we kindly ask you to--
## ...I want my money back...
Please leave us a review and we thank you again for using AlexSpaces. Goodbye.<sup>1</sup>

<sup>1</sup> AlexSpaces is not responsible for any seizures, hallucinations, delusions, aches, cramps, or diarrheal episodes you might experience. By viewing AlexSpaces you hold harmless AlexSpaces LLC and all incorporated entities against any legal action partaken herein unto whomsoever thus beholden wherein. Children under the age of 25 should not use AlexSpaces. 

# Here’s what people are saying about AlexSpaces: 
*“It changed my life forever. I used to think there was no such thing as a 2nd dimension. I still don’t think there is, but it was cool to look at and there were chicks around.”*  
-Dave E., Columbus, OH 
 
*“I was at this music festival and this little box started talking at me. It was like my thoughts were being projected on this little screen. I made it change colors with my mind. I was really high on acid and ecstasy at the same time.”*  
-Jennifer F., Sacramento, CA  
 
*“It's ok I guess."*  
-Mike A., Dallas TX 
 
*“I’ve never seen so many curse words displayed on a screen so small. This is an all-ages festival you know. Are you in charge of this shit? Who can I talk to about this piece of shit garbage?”*  
-Linda C., (the ‘C’ is for ‘cunt’ apparently) 
 
*“I bought this for my husband to play with while I'm out of town. We recieved it in the mail and when we took it out of the box, we were suprised how big it was. The black outer casing is rather big and bulky, not as discreet as I thought it'd be, but once you screw off the lid and feel the soft textures lips on the top of the toy I think all your bulk issues melt away. My husband tested it out and LOVED IT. We warmed it up first and used a bit of the enclosed lube packet that came with it. My husband was so shocked at how real it felt! He even moaned. ha ha It didn't take long before he exploded. Conveniently the sleeve comes out of the casing and you can wash it for easy clean up. I washed the casing as well. I highly recommend this product to any male or couple who will be apart for any length of time.”*  
-Tina L., (obviously confused and left a review for the wrong product)

# Ok Now the Boring Stuff

Hi, Alex here. I created AlexSpaces as a little art project for a friend of mine that hosts her own music festival every year called Molly Hearts. The name "AlexSpaces" is a play on [Wonderspaces](https://www.wonderspaces.com), an art installation that comes to different cities around the US every year.

It's basically just a Raspberry Pi with a Sense HAT attached to it, displaying some fun text and games on the 8x8 pixel grid. The different modes and the one game are controlled using a USB N64 controller, since everybody loves those. The sample [alexspaces.service](alexspaces.service) file configures the program to run upon startup, so it can be plugged in somewhere where no network connectivity is available.

The code for Snake was lifted from https://github.com/bradcornford/Sense-Hat-Snake  
It uses the MIT license and if I understand that license correctly, it's totally fine that I stole it and repurposed it for my own needs. Yeah...

## How to Run AlexSpaces

This is mostly going to be a reminder for myself.  
The odds are pretty slim of someone out there in the world not only reading this far, but reading this far and then deciding "Yeah, I'd like to take this guy's little inside-joke project that he did for him and his friends and run it on my own hardware. Wow how cool is this! Omg and his jokes are so funny too! How do I get in touch with this brilliant mastermind?" But seriously if you are reading this far and/or you maybe found some code in here you found useful, that's awesome.

Once you have your Raspberry Pi up and running with a Sense HAT attached and a USB controller plugged in (doesn't have to be N64 but the button mapping I used assumes N64), then run the following on your Pi:
```
$ git clone https://github.com/apastel/alexspaces.git
$ cd alexspaces
$ ./run_me.py
```

That's it! The [run_me.py](run_me.py) script will automatically do the following:
1. Download/install all the `apt` requirements (it will ask for `sudo` access).
2. Create and launch a Python virtual environment.
3. Download/install all the `pip` requirements into the virtual environment.
4. Launch Alexspaces.

However, very often something bad will happen during steps 3 or 4 because packages are always changing. I strive to make sure all the correct dependencies are specified and nothing should have to be installed separately, but each time I fire up this app I've noticed I have to tweak the dependencies list.

## Great It's Running. Now What?

Alexspaces (I still haven't decided whether it should be "AlexSpaces" or "Alexspaces") has several different modes, or features (installations?):

1. **Marquee**  
This is the default mode of Alexspaces. Basically, a serious of silly messages will scroll across the grid indefinitely. Exiting one of the othe modes will return to this one.
2. **Jokes** (Press A)  
A random joke will scroll across the grid.
3. **Snake** (Press B)  
Play the game Snake on the grid. (This is really the only interactive/fun thing to do in Alexspaces right now.)
4. **Rainbow** (Press Left-C)  
A wave of rainbow colors will overwhelm your senses. Code taken from the [Astro-Pi Project](https://github.com/astro-pi/python-sense-hat/blob/master/examples/rainbow.py)
5. **Temperature** (Press Up-C)  
Show the current temperature. (Guaranteed to be wrong because of added heat coming off the CPU, but it still attempts to account for that).
6. I thought there was one more but I guess that's it.