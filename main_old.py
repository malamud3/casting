"""
LoginVR Quest Casting Application

A modern, modular application for casting Meta Quest screens to PC.
Refactored for better maintainability and extensibility.
"""

import logging
import os
import sys
from typing import Optional

# Import our modular components
from config import load_config, AppConfig
from models import AppState, QuestDevice
from adb_manager import ADBManager
from cast_manager import CastManager
from gui import CastingGUI
from utils import resource_path, setup_logging


class CastingApplication:
    """Main application controller."""
    
    def __init__(self):
        # Set up logging first
        setup_logging("INFO")
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = load_config()
        self.logger.info("Application starting...")
        
        # Set up paths
        self.icon_path = resource_path("temp.ico")
        self.adb_path = resource_path("adb.exe")
        self.src_dir = os.path.dirname(self.adb_path)
        
        # Initialize managers
        self.adb_manager = ADBManager(self.config, self.adb_path)
        self.cast_manager = CastManager(self.config, self.src_dir)
        
        # Initialize GUI
        self.gui = CastingGUI(self.config, self.icon_path)
        
        # Connect GUI callbacks
        self.gui.on_cast_requested = self.handle_cast_request
        self.gui.on_wireless_toggle = self.handle_wireless_toggle
        
        # Application state
        self.app_state = AppState()
        
        self.logger.info("Application initialized successfully")
    
    def handle_cast_request(self):
        """Handle request to start casting."""
        try:
            current_device = self.app_state.current_device
            if not current_device:
                self.gui.show_warning(
                    "המכשיר אינו מחובר",
                    "אנא ודא שהקווסט מחובר / במצב מפתח."
                )
                return
            
            # Check for Wi-Fi connection preference
            wifi_serial = self.adb_manager.find_wifi_serial()
            
            # Perform validation only if no Wi-Fi available
            if not wifi_serial:
                if not current_device.is_authorized:
                    if current_device.state.value == "unauthorized":
                        self.gui.show_warning(
                            "אין גישה",
                            "המכשיר זוהה אך לא אושרה הגישה.\n"
                            "שים את המשקפת על הראש ובחר Always Allow."
                        )
                    else:
                        self.gui.show_warning(
                            "המכשיר אינו מחובר",
                            "אנא ודא שהקווסט מחובר / במצב מפתח."
                        )
                    return
            
            # Start casting
            success = self.cast_manager.start_casting(current_device, wifi_serial)
            if not success:
                self.gui.show_error(
                    "תקלה",
                    "לא הצלחנו להתחיל את השידור. בדוק שכל הקבצים קיימים."
                )
            else:
                self.logger.info("Casting started successfully")
                
        except Exception as e:
            self.logger.error(f"Failed to handle cast request: {e}")
            self.gui.show_error("תקלה", f"שגיאה לא צפויה: {e}")
    
    def handle_wireless_toggle(self):
        """Handle wireless connection toggle."""
        try:
            current_device = self.app_state.current_device
            if not current_device:
                return
            
            if current_device.is_wifi:
                # Disconnect from wireless
                self._disconnect_wireless()
            else:
                # Connect to wireless
                self._connect_wireless()
                
        except Exception as e:
            self.logger.error(f"Failed to handle wireless toggle: {e}")
            self.gui.show_error("תקלה", f"שגיאה בחיבור האלחוטי: {e}")
    
    def _connect_wireless(self):
        """Connect to wireless ADB."""
        self.gui.show_rtl_info("חיבור אלחוטי", "חבר את המכשיר בכבל והמתן לזיהוי…")
        
        def _attempt_connection():
            device = self.adb_manager.detect_quest_device()
            
            if not device.is_authorized:
                # Wait for authorization and try again
                self.gui.schedule_callback(_attempt_connection, self.config.refresh_interval_ms)
                return
            
            # Get Wi-Fi IP
            ip = self.adb_manager.get_wifi_ip()
            if not ip:
                self.gui.show_error("תקלה", "לא נמצא ה-אייפי של המכשיר")
                return
            
            # Enable wireless ADB
            if not self.adb_manager.enable_wireless_adb():
                self.gui.show_error("תקלה", "לא הצלחנו להפעיל מצב אלחוטי")
                return
            
            # Connect to device
            success, message = self.adb_manager.connect_wireless(ip)
            if success:
                wifi_address = f"{ip}:{self.config.wireless_port}"
                self.app_state.last_wifi_serial = wifi_address
                self.gui.show_info("Wi-Fi", f"{message}\nכעת ניתן לנתק את הכבל")
                self.refresh_device_status()
            else:
                self.gui.show_error("תקלה", f"החיבור נכשל: {message}")
        
        _attempt_connection()
    
    def _disconnect_wireless(self):
        """Disconnect from wireless ADB."""
        current_device = self.app_state.current_device
        if current_device and current_device.is_wifi:
            self.adb_manager.disconnect_wireless(current_device.serial)
        
        self.app_state.last_wifi_serial = None
        self.refresh_device_status()
    
    def refresh_device_status(self):
        """Refresh the current device status."""
        try:
            device = self.adb_manager.detect_quest_device()
            self.app_state.update_device(device)
            self.gui.update_device_status(device)
            
        except Exception as e:
            self.logger.error(f"Failed to refresh device status: {e}")
            # Create a default "unknown" device state
            unknown_device = QuestDevice(
                transport=None,
                state=None, 
                serial=None
            )
            self.gui.update_device_status(unknown_device)
    
    def start_auto_refresh(self):
        """Start automatic device status refresh."""
        def _refresh():
            self.refresh_device_status()
            self.gui.schedule_callback(_refresh, self.config.refresh_interval_ms)
        
        _refresh()
    
    def run(self):
        """Run the application."""
        try:
            # Initial device status check
            self.refresh_device_status()
            
            # Start auto-refresh
            self.start_auto_refresh()
            
            # Run GUI
            self.gui.run()
            
        except Exception as e:
            self.logger.error(f"Application failed: {e}")
            raise
        finally:
            self.logger.info("Application shutting down")


def main():
    """Application entry point."""
    try:
        app = CastingApplication()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
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
        "Created by Avi Kohen · 2025 · v0.2.0",
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
    showinfo_rtl("חיבור אלחוטי", "חבר את המכשיר בכבל והמתן לזיהוי…")

    def _do():
        transport, state, _ = quest_state()
        if state != "device":                 # wait until authorised via USB
            window.after(REFRESH_INTERVAL_MS, _do)
            return

        ip = _wifi_ip()
        if not ip:
            messagebox.showerror("תקלה", "לא נמצא ה-אייפי של המכשיר")
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
        status_text.set("מכשיר מחובר אלחוטית")
        wireless_btn.config(text="🔌 נתק אלחוטית", state="normal")
    elif state == "device":
        status_text.set("מכשיר מחובר")
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
