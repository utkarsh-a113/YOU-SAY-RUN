import sys
from time import sleep

def printlyrics_with_timing():
    lyrics = [
        ("Forbidden from the beginnin',", 5.0),  # e.g., starts at 5.0 seconds
        ("I saw her there, up there", 5.8),
        ("Been like that since I met her,", 7.2),
        ("they said I couldn't have her", 9.0),
        ("Way out of my league,", 11.0),
        ("I never believed it", 12.5),
        ("Gotta get her heart,", 14.0),
        ("I gotta make her mine", 15.5),
        ("But what if she just tells me", 17.2),
        ("I'm not quite her speed or", 18.8),
        ("Shows me her bare hands", 20.0),
        ("and crushes my ego?", 21.5),
        ("Dismiss me as a kid,", 23.0),
        ("tells me I'm barely legal", 24.5),
        ("But barely legal is legal", 26.0),
    ]

    start = lyrics[0][1]  # initial timestamp (start of first line)
    current_time = 0.0
    for line, timestamp in lyrics:
        sleep(timestamp - current_time)
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        current_time = timestamp

printlyrics_with_timing()
