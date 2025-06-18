import subprocess
import os
import sys
import tkinter as tk
from tkinter import messagebox, Canvas

def is_quest_connected():
    try:
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        adb_path = os.path.join(base_dir, "adb.exe")
        result = subprocess.run([adb_path, "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")
        return any("device" in line and not line.startswith("List") for line in lines)
    except Exception:
        return False

def refresh_status():
    global status_circle
    connected = is_quest_connected()
    canvas.itemconfig(status_circle, fill="green" if connected else "red")
    status_text.set("Meta Quest 2 מחובר" if connected else "לא מחובר")

def cast_screen():
    if not is_quest_connected():
        messagebox.showwarning("המכשיר אינו מחובר", "אנא חבר את המכשיר מראש")
        return
    try:
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        bat_path = os.path.join(base_dir, "cast.bat")
        subprocess.Popen(["cmd.exe", "/c", bat_path])
    except Exception as e:
        messagebox.showerror("תקלה", f"לא הצליח להריץ cast.bat:\n{e}")

# --- GUI ---
window = tk.Tk()
window.title("מציג מסך קאסטינג LoginVR")
window.geometry("350x220")
window.resizable(False, False)

status_text = tk.StringVar()
status_text.set("Status: Unknown")

canvas = Canvas(window, width=30, height=30)
canvas.pack(pady=(20, 0))
status_circle = canvas.create_oval(5, 5, 25, 25, fill="red")

status_label = tk.Label(window, textvariable=status_text, font=("Arial", 12))
status_label.pack(pady=5)

refresh_btn = tk.Button(window, text="🔄 רענן חיבור", font=("Arial", 12), command=refresh_status)
refresh_btn.pack(pady=5)

cast_btn = tk.Button(window, text="📺 הצג מסך", font=("Arial", 12), command=cast_screen)
cast_btn.pack(pady=15)

# Auto-refresh once on load
refresh_status()

window.mainloop()
