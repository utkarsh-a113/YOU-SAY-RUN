import sys
import time
from time import sleep

def printlyrics():
    # (word, delay) pairs
    lyrics = [
        ("I wanna da-", 0.5),
        ("I wanna dance in the lights", 0.45),
        ("I wanna ro-", 0.55),
        ("I wanna rock your body", 0.6),
        ("I wanna go", 0.6),
        ("I wanna go for a ride", 0.55),
        ("Hop in the music and", 0.55),
        ("ROCK YOUR BODY", 0.65),
        ("ROCK THAT BODY", 0.65),
        ("Come on come on", 0.5),
        ("rock that body", 0.55),
        ("(Rock yo' body)", 0.5),
        ("Rock that body", 0.55)
    ]
    
    for line, delay in lyrics:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        sleep(delay)  # longer delay

# Run it
printlyrics()
