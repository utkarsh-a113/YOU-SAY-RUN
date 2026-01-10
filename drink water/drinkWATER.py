import time
import threading
import winsound
from plyer import notification
import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

running=False
reminder_thread= None
tray_icon= None

def remind(interval):
    global running
    while running:
        winsound.beep(1000,800)
        notification.notify(
        title=" Water Reminder",
        message="Time to drink water !",
        timeout=10
    )
    time.sleep(interval)

def start_reminder():
    

INTERVAL=3600 #1x
while True:
    #beep beep
    winsound.Beep(1000,800) #frequency, duration
    
    #notification
    