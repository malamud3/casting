
"""
LoginVR – Meta Quest casting helper
Author  : Avi Kohen
Version : 0.1.1 · 2025
"""

import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from subprocess import PIPE, STDOUT
import webbrowser
from urllib.parse import quote

# ── paths ────────────────────────────────────────────────────────────────────
def resource_path(name: str) -> str:
    """
    Return absolute path to *name*, whether running from source or a PyInstaller
    bundle.
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    if not base.endswith("src"):
        base = os.path.join(base, "src")
    return os.path.join(base, name)


ICON_PATH = resource_path("temp.ico")


# ── constants ────────────────────────────────────────────────────────────────
CREATE_NO_WINDOW   = 0x08000000
REFRESH_INTERVAL_MS = 2000      # GUI auto-refresh
ADB_TIMEOUT        = 4000       # ms
WIRELESS_PORT      = "5555"

COLORS = {                       # dot colour by state / transport
    "wifi":        "green",
    "device":      "green",
    "unauthorized":"yellow",
    "offline":     "red",
    "":            "red",
}

# remember last Wi-Fi serial so we can cast even with cable attached
last_wifi_serial: str | None = None


# ── tiny subprocess wrapper (keeps pylint quiet & code DRY) ──────────────────
def run(cmd, **kw):
    """subprocess.run() with sensible defaults (check=False by default)."""
    kw.setdefault("check", False)
    kw.setdefault("stdout", PIPE)
    kw.setdefault("stderr", STDOUT)
    kw.setdefault("text", True)
    kw.setdefault("timeout", ADB_TIMEOUT / 1000)
    kw.setdefault("creationflags", CREATE_NO_WINDOW)
    return subprocess.run(cmd, **kw)


# ── adb helpers ──────────────────────────────────────────────────────────────
def _adb() -> str:
    return resource_path("adb.exe")


def _devices_output() -> str:
    return run([_adb(), "devices", "-l"]).stdout


def quest_state() -> tuple[str | None, str, str | None]:
    """
    Return (transport, state, serial), preferring Wi-Fi if present.

    transport ∈ {"wifi", "usb", None}
    state     ∈ {"device", "unauthorized", "offline", ""}
    serial    = "192.168…:5555" | "<USB-serial>" | None
    """
    wifi_row: tuple[str, str, str] | None = None
    usb_row:  tuple[str, str, str] | None = None

    for line in _devices_output().splitlines()[1:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        serial, state = parts[0], parts[1]

        if ":" in serial:                  # looks like 192.168.x.x:5555 (TCP/IP)
            if wifi_row is None:           # keep the first Wi-Fi row only
                wifi_row = ("wifi", state, serial)
        else:                              # USB entry
            if usb_row is None:            # keep the first USB row only
                usb_row = ("usb", state, serial)

    return wifi_row or usb_row or (None, "", None)



def _wifi_ip() -> str | None:
    """Return headset Wi-Fi IP (USB must be connected)."""
    out = run([_adb(), "shell", "ip", "-f", "inet", "addr", "show", "wlan0"]).stdout
    m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", out)
    return m.group(1) if m else None


def wifi_serial_from_adb() -> str | None:
    """Return first xxx.xxx.xxx.xxx:5555 found in adb devices output."""
    for line in _devices_output().splitlines()[1:]:
        tok = line.split()
        if tok and ":" in tok[0]:
            return tok[0]
    return None


# ── RTL / helper dialogs ─────────────────────────────────────────────────────
def showinfo_rtl(title: str, body: str, ok_text: str = "אישור"):
    win = tk.Toplevel(window)
    win.title(title)
    win.resizable(False, False)
    win.grab_set()
    win.transient(window)
    ttk.Label(win, text=body, justify="right", anchor="e",
              wraplength=300, font=("Segoe UI", 10)).pack(padx=20, pady=(20, 10))
    ttk.Button(win, text=ok_text, command=win.destroy).pack(pady=(0, 15), ipadx=10)
    win.wait_window()


def show_instructions():
    msg = (
        "\u202B1. הדלק את הקווסט והפעל אפליקציה לשידור\u202C\n"
        "\u202B2. חבר את הקווסט למחשב באמצעות כבל\u202C\n"
        "\u202B3. אשר את הגישה דרך המכשיר\u202C\n"
        "\u202B4. לחץ \"הצג מסך\"\u202C"
    )
    showinfo_rtl("הוראות", msg)


def show_about():
    messagebox.showinfo(
        "About",
        "All rights reserved to LoginVR – internal use only\n"
        "Created by Avi Kohen · 2025 · v0.1.1",
    )


def show_faq():
    faq = tk.Toplevel(window)
    faq.title("FAQ / Help")
    faq.iconbitmap(ICON_PATH)
    faq.resizable(False, False)

    tk.Label(faq, text="הפעלת מצב מפתח (סרטון בגוגל דרייב)", justify="right")\
      .pack(padx=10, pady=(10, 5))

    def open_link(_=None):
        webbrowser.open_new(
            "https://drive.google.com/file/d/1hYf4B3nKVmHpBGViHWfdY_qgfD-LOKPg/view?usp=drive_link"
        )

    link = tk.Label(faq, text="לחץ כאן", fg="blue", cursor="hand2", underline=True)
    link.pack()
    link.bind("<Button-1>", open_link)

    tk.Label(faq, text="לשאלות נוספות / בעיות", justify="right")\
      .pack(pady=(10, 5))

    email = "info@loginvr.co.il"
    subject = "אפליקציית קאסטינג"
    body = "הי,\n\nאני צריך עזרה עם…"

    def mailto(_=None):
        uri = f"mailto:{email}?subject={quote(subject)}&body={quote(body)}"
        webbrowser.open_new(uri)

    email_lbl = tk.Label(faq, text=email, fg="blue",
                         cursor="hand2", underline=True)
    email_lbl.pack(pady=(0, 10))
    email_lbl.bind("<Button-1>", mailto)


# ── connection actions ──────────────────────────────────────────────────────
def wireless_connect():
    """Switch Quest to Wi-Fi ADB."""
    showinfo_rtl("חיבור אלחוטי", "חבר את הקווסט בכבל והמתן לזיהוי…")

    def _do():
        transport, state, _ = quest_state()
        if state != "device":                 # wait until authorised via USB
            window.after(REFRESH_INTERVAL_MS, _do)
            return

        ip = _wifi_ip()
        if not ip:
            messagebox.showerror("תקלה", "לא נמצא IP של הקווסט")
            return

        wifi = f"{ip}:{WIRELESS_PORT}"
        run([_adb(), "tcpip", WIRELESS_PORT])
        out = run([_adb(), "connect", wifi]).stdout

        global last_wifi_serial
        last_wifi_serial = wifi
        messagebox.showinfo("Wi-Fi", out.strip() + "\nכעת ניתן לנתק את הכבל")
        refresh_status(auto=False)

    _do()


def wireless_disconnect():
    """Tear down Wi-Fi ADB and fall back to USB."""
    _, _, serial = quest_state()
    if serial and ":" in serial:              # only when on Wi-Fi
        run([_adb(), "disconnect", serial])
    run([_adb(), "usb"])

    global last_wifi_serial
    last_wifi_serial = None
    refresh_status(auto=False)


def toggle_wireless():
    if wireless_btn.cget("text").startswith("📡"):
        wireless_connect()
    else:
        wireless_disconnect()


def cast_screen():
    """
    Launch scrcpy, preferring the Wi-Fi serial if one is in the adb list.

    • If a Wi-Fi row is in `adb devices` → scrcpy -s <wifi:5555>
    • Else fall back to whatever serial `quest_state()` returned.
    • The usual “unauthorized / no-device” checks only block when *no* Wi-Fi
      row is available.
    """
    transport, state, serial = quest_state()
    wifi = wifi_serial_from_adb()        # returns e.g. 192.168.0.15:5555 or None

    # -- sanity checks (skip them when we have a Wi-Fi target anyway) --
    if not wifi and state == "unauthorized":
        messagebox.showwarning(
            "אין גישה",
            "המכשיר זוהה אך לא אושרה הגישה.\n"
            "שים את המשקפת על הראש ובחר Always Allow."
        )
        return

    if not wifi and state != "device":
        messagebox.showwarning(
            "המכשיר אינו מחובר",
            "אנא ודא שהקווסט מחובר / במצב מפתח."
        )
        return

    # choose the target serial: Wi-Fi first, fallback = whatever we saw
    target = wifi or serial

    bat = resource_path("cast.bat")
    cwd = os.path.dirname(bat)

    try:
        if target:
            subprocess.Popen(
                ["cmd.exe", "/c", bat, target],
                cwd=cwd,
                creationflags=CREATE_NO_WINDOW,
            )
        else:                            # extremely rare: no serial at all
            subprocess.Popen(
                ["cmd.exe", "/c", bat],
                cwd=cwd,
                creationflags=CREATE_NO_WINDOW,
            )
    except Exception as exc:
        messagebox.showerror("תקלה", f"cast.bat נכשל:\n{exc}")



# ── GUI refresh ─────────────────────────────────────────────────────────────
def refresh_status(auto: bool = True):
    transport, state, _ = quest_state()
    key = transport if transport == "wifi" else state
    canvas.itemconfig(status_circle, fill=COLORS.get(key, "red"))

    if transport == "wifi" and state == "device":
        status_text.set("Meta Quest מחובר אלחוטית")
        wireless_btn.config(text="🔌 נתק אלחוטית", state="normal")
    elif state == "device":
        status_text.set("Meta Quest מחובר")
        wireless_btn.config(
            text="📡 חיבור אלחוטי",
            state="normal" if transport == "usb" else "disabled"
        )
    elif state == "unauthorized":
        status_text.set("אשר גישה במכשיר (Always Allow)")
        wireless_btn.config(text="📡 חיבור אלחוטי", state="disabled")
    else:
        status_text.set("וודא שהקווסט דלוק ומחובר למחשב")
        wireless_btn.config(text="📡 חיבור אלחוטי", state="disabled")

    if auto:
        window.after(REFRESH_INTERVAL_MS, refresh_status)


# ── GUI root window ─────────────────────────────────────────────────────────
window = tk.Tk()
window.iconbitmap(ICON_PATH)
window.title("קאסטינג LoginVR")
window.geometry("370x250")
window.resizable(False, False)

# Menu bar (RTL order – rightmost first)
menubar = tk.Menu(window)
menubar.add_command(label="הוראות", command=show_instructions)
menubar.add_command(label="אודות",  command=show_about)
menubar.add_command(label="עזרה",   command=show_faq)
window.config(menu=menubar)

status_text = tk.StringVar(value="Status: Unknown")

canvas = Canvas(window, width=30, height=30)
canvas.pack(pady=(20, 0))
status_circle = canvas.create_oval(5, 5, 25, 25, fill="red")

tk.Label(window, textvariable=status_text, font=("Arial", 12)).pack(pady=5)

cast_btn = tk.Button(window, text="📺 הצג מסך", font=("Arial", 12),
                     command=cast_screen)
cast_btn.pack(pady=15)

wireless_btn = tk.Button(window, text="📡 חיבור אלחוטי", font=("Arial", 12),
                         command=toggle_wireless, state="disabled")
wireless_btn.pack(pady=5)

# initial status poll
refresh_status()

window.mainloop()
