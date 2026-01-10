import time
import threading
import winsound
from plyer import notification
import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

running = False
reminder_thread = None
tray_icon = None

def remind(interval):
    global running
    while running:
        winsound.Beep(1000, 800)
        notification.notify(
            title="💧 Water Reminder",
            message="Time to drink water!",
            timeout=10
        )
        time.sleep(interval)

def start_reminder():
    global running, reminder_thread
    if running:
        messagebox.showinfo("Info", "Reminder already running!")
        return

    try:
        interval = int(interval_entry.get()) * 60
    except:
        messagebox.showerror("Error", "Enter a valid number")
        return

    running = True
    reminder_thread = threading.Thread(target=remind, args=(interval,), daemon=True)
    reminder_thread.start()
    status_label.config(text="Status: Running")

def stop_reminder():
    global running
    running = False
    status_label.config(text="Status: Stopped")

def create_image():
    image = Image.new('RGB', (64, 64), color='blue')
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 10, 44, 54), fill="white")
    return image

def on_quit(icon, item):
    stop_reminder()
    icon.stop()
    root.destroy()

def minimize_to_tray():
    global tray_icon
    root.withdraw()
    image = create_image()
    tray_icon = pystray.Icon(
        "Water Reminder",
        image,
        "Water Reminder",
        menu=pystray.Menu(
            item("Open", restore_window),
            item("Quit", on_quit)
        )
    )
    tray_icon.run()

def restore_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

#-----------------------------------GUI--------------------------------#
root = tk.Tk()
root.title("Water Reminder")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW", minimize_to_tray)

tk.Label(root, text="Interval (minutes):").pack(pady=5)
interval_entry = tk.Entry(root)
interval_entry.insert(0, "60")
interval_entry.pack()

tk.Button(root, text="Start", command=start_reminder).pack(pady=5)
tk.Button(root, text="Stop", command=stop_reminder).pack(pady=5)

status_label = tk.Label(root, text="Status: Stopped")
status_label.pack(pady=10)

root.mainloop()