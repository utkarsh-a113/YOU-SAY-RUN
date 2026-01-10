import time
import winsound
from plyer import notification
INTERVAL=3600 #1x
while True:
    #beep beep
    winsound.Beep(1000,800) #frequency, duration
    
    #notification
    notification.notify(
        title=" Water Reminder",
        message="Time to drink water !",
        timeout=10
    )
    time.sleep(INTERVAL)