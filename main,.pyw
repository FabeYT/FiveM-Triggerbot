import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput.mouse import Controller, Button
from pynput import keyboard
from PIL import Image
import threading
import time
import ctypes

mouse = Controller()
monitoring_active = False
hidden = False
listener = None

def is_red_color(rgb):
    r, g, b = rgb
    return r > 150 and g < 80 and b < 80 and abs(r - max(g, b)) > 80

def is_white_color(rgb):
    r, g, b = rgb
    return r >= 220 and g >= 220 and b >= 220

def get_center_screen_color():
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2
    screenshot = pyautogui.screenshot(region=(center_x, center_y, 1, 1))
    return screenshot.getpixel((0, 0))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def monitor():
    global monitoring_active
    in_trigger_mode = False
    trigger_start_time = None

    while True:
        if monitoring_active:
            rgb = get_center_screen_color()
            color_hex = rgb_to_hex(rgb)
            current_time = time.time()
            message = f"Farbe (RGB): {rgb}\nHEX: {color_hex.upper()}"

            if not hidden:
                color_preview.config(bg=color_hex)

            if not in_trigger_mode:
                if is_white_color(rgb):
                    in_trigger_mode = True
                    trigger_start_time = current_time
                    message += "\n→ Weiß erkannt: Trigger-Modus AKTIV"
            else:
                if is_red_color(rgb):
                    message += "\n→ ROT erkannt! → MAUSKLICK"
                    mouse.press(Button.left)
                    time.sleep(0.01)
                    mouse.release(Button.left)
                    in_trigger_mode = False
                elif current_time - trigger_start_time > 20:
                    message += "\n→ Zeit abgelaufen (20s) – Trigger-Modus ZURÜCKGESETZT"
                    in_trigger_mode = False

            if not hidden:
                log_text.set(message)
        time.sleep(0.005)

def toggle_monitoring():
    global monitoring_active
    monitoring_active = not monitoring_active
    if monitoring_active:
        status_label.config(text="Status: LÄUFT", foreground="#2ecc71")
        toggle_button.config(text="Stoppen")
    else:
        status_label.config(text="Status: GESTOPPT", foreground="#e74c3c")
        toggle_button.config(text="Starten")

def hide_from_taskbar():
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x80 | 0x08)
    ctypes.windll.user32.ShowWindow(hwnd, 0)

def show_to_taskbar():
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, 0x80 | 0x08)
    ctypes.windll.user32.ShowWindow(hwnd, 5)

def toggle_visibility():
    global hidden
    if hidden:
        root.deiconify()
        show_to_taskbar()
        hidden = False
        hide_button.config(text="Verstecken")
    else:
        root.withdraw()
        hide_from_taskbar()
        hidden = True

# GUI-Aufbau
root = tk.Tk()
root.title("FiveM Trigger Assistant")
root.geometry("380x340")  # Höhe erhöht für den Credit-Hinweis
root.resizable(False, False)
root.configure(bg="#f5f6fa")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 9))

main_frame = ttk.Frame(root, padding=(20, 15))
main_frame.pack(fill=tk.BOTH, expand=True)

preview_frame = ttk.Frame(main_frame)
preview_frame.pack(pady=(0, 15))

color_preview = tk.Label(preview_frame, bg="#000000", width=25, height=3,
                         relief="flat", bd=0, highlightbackground="#dcdde1", highlightthickness=1)
color_preview.pack()

log_frame = ttk.Frame(main_frame)
log_frame.pack(fill=tk.X, pady=(0, 15))

log_text = tk.StringVar(value="Bereit zur Überwachung...")
log_label = ttk.Label(log_frame, textvariable=log_text, wraplength=340)
log_label.pack(fill=tk.X)
log_label.configure(background="#ecf0f1", padding=(10, 8))

status_frame = ttk.Frame(main_frame)
status_frame.pack(fill=tk.X, pady=(0, 15))

status_label = ttk.Label(status_frame, text="Status: GESTOPPT", foreground="#e74c3c", font=("Segoe UI", 10, "bold"))
status_label.pack(side=tk.LEFT)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X)

toggle_button = ttk.Button(button_frame, text="Starten", command=toggle_monitoring)
toggle_button.pack(side=tk.LEFT, padx=(0, 10))

hide_button = ttk.Button(button_frame, text="Verstecken", command=toggle_visibility)
hide_button.pack(side=tk.LEFT)

# Credit-Hinweis hinzugefügt
credit_frame = ttk.Frame(main_frame)
credit_frame.pack(fill=tk.X, pady=(5, 0))
credit_label = ttk.Label(credit_frame, text="Made by dasofabe", foreground="#7f8c8d", font=("Segoe UI", 8, "italic"))
credit_label.pack(side=tk.RIGHT)

hotkey_frame = ttk.Frame(main_frame)
hotkey_frame.pack(fill=tk.X, pady=(5, 0))  # Pady angepasst

ttk.Label(hotkey_frame,
          text="Hotkeys: F1 = Start/Stop, F2 = Verstecken/Anzeigen",
          foreground="#7f8c8d", font=("Segoe UI", 8)).pack()

def start_listener():
    global listener
    listener = keyboard.GlobalHotKeys({
        '<f1>': toggle_monitoring,
        '<f2>': toggle_visibility
    })
    listener.start()

threading.Thread(target=start_listener, daemon=True).start()
threading.Thread(target=monitor, daemon=True).start()

root.mainloop()
