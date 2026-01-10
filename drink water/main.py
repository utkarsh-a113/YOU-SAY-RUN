import time
import winsound
from plyer import notification

# reminder interval (seconds)
# 1 hour = 3600, 2 hours = 7200
INTERVAL = 3600  

while True:
    # Beep sound
    winsound.Beep(1000, 800)  # frequency, duration(ms)

    # Windows notification
    notification.notify(
        title="💧Water Reminder",
        message="Time to drink water!",
        timeout=10
    )

    time.sleep(INTERVAL)
