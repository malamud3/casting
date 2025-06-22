import os
import sys
import subprocess                      # gives you subprocess.run, .Popen, .CREATE_NO_WINDOW
from subprocess import PIPE, STDOUT, TimeoutExpired
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Canvas
import webbrowser
from urllib.parse import quote          # for mailto links

def resource_path(name):
    """
    Return absolute path to resource, whether running
    - from source (…/src/main.py)   ->  …/src/<name>
    - or from a PyInstaller bundle  ->  …/_MEIxxxx/src/<name>
    """
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # only add 'src' when it isn't already part of the path
    if not base.endswith('src'):
        base = os.path.join(base, 'src')
    return os.path.join(base, name)

ICON_PATH = resource_path('temp.ico')

# --- constants ---
CREATE_NO_WINDOW = 0x08000000
REFRESH_INTERVAL_MS = 2000          # 5 seconds
ADB_TIMEOUT = 4000      # milliseconds (≈4 s)
COLORS = {
    "device":       "green",
    "unauthorized": "yellow",
    "offline":      "red",
    "":             "red",
}

def quest_state():
    adb = resource_path('adb.exe')
    try:
        out = subprocess.run(
            [adb, "devices", "-l"],
            stdout=PIPE, stderr=STDOUT, text=True,
            timeout=ADB_TIMEOUT / 1000,
            creationflags=CREATE_NO_WINDOW             #  ← NEW
        ).stdout
        for line in out.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 2:
                return parts[1]                       # "device", "unauthorized"
        return ""
    except TimeoutExpired:
        # start server silently
        subprocess.run(
            [adb, "start-server"],
            stdout=PIPE, stderr=STDOUT, timeout=5,
            creationflags=CREATE_NO_WINDOW            #  ← NEW
        )
        return ""

# --- refresh logic ---
def refresh_status(auto=True):
    state = quest_state()
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
        adb_path = resource_path('adb.exe')
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
        bat_path = resource_path("cast.bat")
        src_dir  = os.path.dirname(bat_path)        # ← folder that holds cast.bat
        subprocess.Popen(
            ["cmd.exe", "/c", bat_path],
            cwd=src_dir                          # ← use this instead of BASE_PATH
        )
    except Exception as e:
        messagebox.showerror("תקלה", f"לא הצליח להריץ cast.bat:\n{e}")


def showinfo_rtl(title: str, body: str, ok_text: str = "אישור"):
    """
    Replacement for messagebox.showinfo that is right-to-left.
    • Title bar shows your title
    • Text is right-aligned and wraps
    • OK button closes the window
    """
    win = tk.Toplevel(window)           # 'window' == your main Tk instance
    win.title(title)
    win.resizable(False, False)
    win.grab_set()                      # make it modal (blocks parent)

    # Ensure the dialog is centred over the parent
    win.transient(window)

    # Main text label — RTL alignment
    ttk.Label(
        win,
        text=body,
        justify="right",
        anchor="e",     # east
        wraplength=300,
        font=("Segoe UI", 10)
    ).pack(padx=20, pady=(20, 10))

    # OK button
    ttk.Button(
        win,
        text=ok_text,
        command=win.destroy
    ).pack(pady=(0, 15), ipadx=10)

    win.wait_window()  # block until user closes


def show_instructions():

    text = (
        "\u202B1. הדלק את הקווסט והפעל אפליקציה לשידור\u202C\n"
        "\u202B2. חבר את הקווסט למחשב באמצעות כבל\u202C\n"
        "\u202B3. אשר את הגישה דרך המכשיר\u202C\n"
        "\u202B4. לחץ \"הצג מסך\"\u202C"
    )
    showinfo_rtl("הוראות", text)

def show_about():
    messagebox.showinfo("About",
        "All rights reserved to LoginVR not for sale or distribution - Internal use only\n"
        "Created by Avi Kohen\n"
        "2025\n"
        "V0.1.1")

def show_faq():
    win = tk.Toplevel(window)
    win.title("FAQ/Help")
    win.iconbitmap(ICON_PATH)
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
window.iconbitmap(ICON_PATH)
window.title("קאסטינג LoginVR")
window.geometry("370x250")
window.resizable(False, False)

# --- Menu Bar ---
menubar = tk.Menu(window)
menubar.add_cascade(label="הוראות", command=show_instructions)
menubar.add_cascade(label="אודות", command=show_about)
menubar.add_cascade(label="עזרה", command=show_faq)
window.config(menu=menubar)

status_text = tk.StringVar()
status_text.set("Status: Unknown")

canvas = Canvas(window, width=30, height=30)
canvas.pack(pady=(20, 0))
status_circle = canvas.create_oval(5, 5, 25, 25, fill="red")

status_label = tk.Label(window, textvariable=status_text, font=("Arial", 12))
status_label.pack(pady=5)

# --- GUI buttons ---

cast_btn = tk.Button(window, text="📺 הצג מסך", font=("Arial", 12), command=cast_screen)
cast_btn.pack(pady=15)

# Auto-refresh once on load
refresh_status()

window.mainloop()
