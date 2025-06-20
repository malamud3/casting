import subprocess
import os
import sys
import tkinter as tk
from tkinter import messagebox, Canvas
from subprocess import run, PIPE
import webbrowser
from urllib.parse import quote

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")

# --- constants ---
REFRESH_INTERVAL_MS = 5000          # 5 seconds
COLORS = {
    "device":       "green",
    "unauthorized": "yellow",
    "offline":      "red",
    "":             "red",
}
def quest_state():
    adb = os.path.join(BASE_PATH, "adb.exe")
    out = run([adb, "devices"], stdout=PIPE, text=True, timeout=1).stdout
    for line in out.splitlines()[1:]:          # skip header
        parts = line.split()
        if len(parts) >= 2:
            return parts[1]                    # "device", "unauthorized", ...
    return ""                                  # nothing connected

# --- refresh logic ---
def refresh_status(auto=True):
    state = quest_state()
    print("something")
    print(state)
    canvas.itemconfig(status_circle, fill=COLORS.get(state, "red"))

    if state == "device":
        status_text.set("Meta Quest מחובר")
    elif state == "unauthorized":
        status_text.set('אשר גישה במכשיר על ידי לחיצה על\n Always allow')
    else:
        status_text.set("וודא כי הקווסט דלוק ומחובר למחשב")

    # Automatically schedule the next check
    if auto:
        window.after(REFRESH_INTERVAL_MS, refresh_status)

def is_quest_connected():
    try:
        adb_path = os.path.join(BASE_PATH, "adb.exe")
        result = subprocess.run([adb_path, "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split("\n")
        return any("device" in line and not line.startswith("List") for line in lines)
    except Exception as e:
        print("ADB error:", e)
        return False

def cast_screen():
    state = quest_state()
    if state == "unauthorized":
        messagebox.showwarning("אין גישה",
            "המכשיר זוהה אך לא אושרה הגישה.\n"
            "שים את המשקפת על הראש ובחר ב- **Always Allow**.")
        return
    if state != "device":
        messagebox.showwarning("המכשיר אינו מחובר",
            "אנא וודא שהמכשיר מחובר למחשב עם כבל תקני ושהנך במצב מפתח")
        return
    try:
        bat_path = os.path.join(BASE_PATH, "cast.bat")
        subprocess.Popen(["cmd.exe", "/c", bat_path], cwd=BASE_PATH)
    except Exception as e:
        messagebox.showerror("תקלה", f"לא הצליח להריץ cast.bat:\n{e}")

def show_instructions():
    messagebox.showinfo("הוראות",
        "1. הדלק את הקווסט והפעל אפליקציה לשידור\n"
        "2. חבר את הקווסט למחשב באצעות כבל\n"
        "3. אשר את הגישה דרך המכשיר\n"
        '4. לחץ "הצג מסך"')

def show_about():
    messagebox.showinfo("About",
        "All rights reserved to LoginVR not for sale or distribution - Internal use only\n"
        "Created by Avi Kohen\n"
        "2025\n"
        "V0.1")

def show_faq():
    win = tk.Toplevel(window)
    win.title("FAQ/Help")
    win.resizable(False, False)

    tk.Label(
        win,
        text="הפעלת מצב מפתח (לינק לסרטון בגוגל דרייב)",
        justify="right"
    ).pack(padx=10, pady=(10,5))

    def open_link(_=None):
        webbrowser.open_new("https://drive.google.com/file/d/1hYf4B3nKVmHpBGViHWfdY_qgfD-LOKPg/view?usp=drive_link")

    link = tk.Label(
        win,
        text="לחץ כאן",
        fg="blue", cursor="hand2", underline=True
    )
    link.pack(pady=(0,10))
    link.bind("<Button-1>", open_link)

    tk.Label(
        win,
        text="לשאלות נוספות\בעיות",
        justify="right"
    ).pack(padx=10, pady=(10,5))



    email = "info@loginvr.co.il"
    subject = "אפליקציית קאסטינג"
    body = "הי,\n\nאני צריך עזרה עם…"

    def mailto(_=None):
        uri = (
            f"mailto:{email}"
            f"?subject={quote(subject)}"
            f"&body={quote(body)}"
        )
        webbrowser.open_new(uri)

    link = tk.Label(
        win,
        text=email,
        fg="blue", cursor="hand2", underline=True
    )
    link.pack(pady=(0, 10))
    link.bind("<Button-1>", mailto)

# --- GUI ---
window = tk.Tk()
window.title("קאסטינג LoginVR")
window.geometry("350x220")
window.resizable(False, False)

icon_path = os.path.join(BASE_PATH, "temp.ico")
if os.path.exists(icon_path):
    window.iconbitmap(icon_path)

# --- Menu Bar ---
menubar = tk.Menu(window)
menubar.add_cascade(label="Instructions", command=show_instructions)
menubar.add_cascade(label="About", command=show_about)
menubar.add_cascade(label="FAQ/Help", command=show_faq)
window.config(menu=menubar)

status_text = tk.StringVar()
status_text.set("Status: Unknown")

canvas = Canvas(window, width=30, height=30)
canvas.pack(pady=(20, 0))
status_circle = canvas.create_oval(5, 5, 25, 25, fill="red")

status_label = tk.Label(window, textvariable=status_text, font=("Arial", 12))
status_label.pack(pady=5)

# --- GUI buttons ---
refresh_btn = tk.Button(
    window,
    text="🔄 רענן",
    font=("Arial", 12),
    command=lambda: refresh_status(auto=False)
)
refresh_btn.pack(pady=5)

cast_btn = tk.Button(window, text="📺 הצג מסך", font=("Arial", 12), command=cast_screen)
cast_btn.pack(pady=15)

# Auto-refresh once on load
refresh_status()

window.mainloop()
