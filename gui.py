"""GUI components and dialogs for the casting application."""

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
import platform

from models import QuestDevice, AppState, DeviceState
from utils import open_email_client, open_url
from macos_ui import (
    MacOSStyle, ModernStatusIndicator, ModernLabel, 
    ModernButton, EnhancedRTLDialog
)


logger = logging.getLogger(__name__)


class RTLDialog:
    """Helper for creating RTL (Right-to-Left) dialogs."""
    
    @staticmethod
    def show_info(parent: tk.Tk, title: str, message: str, ok_text: str = "אישור"):
        """Show an RTL information dialog."""
        # Use the enhanced dialog from macos_ui
        EnhancedRTLDialog.show_info(parent, title, message, ok_text)


class InstructionsDialog:
    """Instructions dialog for the application."""
    
    def __init__(self, parent: tk.Tk):
        self.parent = parent
    
    def show(self):
        """Display the instructions dialog."""
        message = (
            "\u202B1. הדלק את הקווסט והפעל אפליקציה לשידור\u202C\n"
            "\u202B2. חבר את הקווסט למחשב באמצעות כבל\u202C\n" 
            "\u202B3. אשר את הגישה דרך המכשיר\u202C\n"
            "\u202B4. לחץ \"הצג מסך\"\u202C"
        )
        RTLDialog.show_info(self.parent, "הוראות", message)


class AboutDialog:
    """About dialog for the application."""
    
    def __init__(self, parent: tk.Tk):
        self.parent = parent
    
    def show(self):
        """Display the about dialog."""
        messagebox.showinfo(
            "About",
            "All rights reserved to LoginVR – internal use only\n"
            "Created by Avi Kohen · 2025 · v2.1.0\n"
            "Refactored for better maintainability"
        )


class FAQDialog:
    """FAQ/Help dialog for the application."""
    
    def __init__(self, parent: tk.Tk):
        self.parent = parent
    
    def show(self):
        """Display the FAQ dialog."""
        faq = tk.Toplevel(self.parent)
        faq.title("FAQ / Help")
        faq.resizable(False, False)
        faq.geometry("400x200")
        
        # Center on parent
        self.parent.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 100
        faq.geometry(f"400x200+{x}+{y}")
        
        # Developer mode video link
        tk.Label(
            faq, 
            text="הפעלת מצב מפתח (סרטון בגוגל דרייב)", 
            justify="right"
        ).pack(padx=10, pady=(10, 5))
        
        video_link = tk.Label(
            faq, 
            text="לחץ כאן", 
            fg="blue", 
            cursor="hand2", 
            underline=True
        )
        video_link.pack()
        video_link.bind("<Button-1>", self._open_video_link)
        
        # Support email
        tk.Label(
            faq, 
            text="לשאלות נוספות / בעיות", 
            justify="right"
        ).pack(pady=(10, 5))
        
        email_label = tk.Label(
            faq, 
            text="info@loginvr.co.il", 
            fg="blue",
            cursor="hand2", 
            underline=True
        )
        email_label.pack(pady=(0, 10))
        email_label.bind("<Button-1>", self._open_email)
    
    def _open_video_link(self, event=None):
        """Open the developer mode video link."""
        url = "https://drive.google.com/file/d/1hYf4B3nKVmHpBGViHWfdY_qgfD-LOKPg/view?usp=drive_link"
        open_url(url)
    
    def _open_email(self, event=None):
        """Open email client for support."""
        open_email_client(
            "info@loginvr.co.il",
            "אפליקציית קאסטינג", 
            "הי,\n\nאני צריך עזרה עם…"
        )


class StatusIndicator:
    """Visual status indicator with color-coded circle."""
    
    def __init__(self, parent: tk.Widget, colors: dict):
        # Use enhanced colors for better platform integration
        enhanced_colors = MacOSStyle.get_status_colors()
        self.colors = {**colors, **enhanced_colors}  # Merge with enhanced colors
        
        # Use the modern status indicator
        self.indicator = ModernStatusIndicator(parent, self.colors)
    
    def update_status(self, device: QuestDevice):
        """Update the status indicator based on device state."""
        self.indicator.update_status(device)


class CastingGUI:
    """Main GUI application for the casting tool."""
    
    def __init__(self, config, icon_path: str):
        self.config = config
        self.state = AppState()
        
        # Callbacks to be set by main application
        self.on_cast_requested: Optional[Callable] = None
        self.on_wireless_toggle: Optional[Callable] = None
        
        # Create main window
        self.window = tk.Tk()
        self.window.iconbitmap(icon_path)
        self.window.title("קאסטינג LoginVR")
        self.window.geometry("370x280")
        self.window.resizable(False, False)
        
        # Create dialogs
        self.instructions_dialog = InstructionsDialog(self.window)
        self.about_dialog = AboutDialog(self.window)
        self.faq_dialog = FAQDialog(self.window)
        
        self._setup_menu()
        self._setup_widgets()
        
        logger.info("GUI initialized")
    
    def _setup_menu(self):
        """Set up the menu bar."""
        menubar = tk.Menu(self.window)
        menubar.add_command(label="הוראות", command=self.instructions_dialog.show)
        menubar.add_command(label="אודות", command=self.about_dialog.show)
        menubar.add_command(label="עזרה", command=self.faq_dialog.show)
        self.window.config(menu=menubar)
    
    def _setup_widgets(self):
        """Set up the main widgets."""
        # Status indicator
        self.status_indicator = StatusIndicator(self.window, self.config.colors)
        
        # Status text
        self.status_text = tk.StringVar(value="מתחבר למכשיר...")
        tk.Label(
            self.window, 
            textvariable=self.status_text, 
            font=("Arial", 12)
        ).pack(pady=5)
        
        # Cast button
        self.cast_btn = tk.Button(
            self.window, 
            text="📺 הצג מסך", 
            font=("Arial", 12),
            command=self._on_cast_clicked,
            state="disabled"
        )
        self.cast_btn.pack(pady=15)
        
        # Wireless button
        self.wireless_btn = tk.Button(
            self.window, 
            text="📡 חיבור אלחוטי", 
            font=("Arial", 12),
            command=self._on_wireless_clicked,
            state="disabled"
        )
        self.wireless_btn.pack(pady=5)
    
    def _on_cast_clicked(self):
        """Handle cast button click."""
        if self.on_cast_requested:
            self.on_cast_requested()
    
    def _on_wireless_clicked(self):
        """Handle wireless button click."""
        if self.on_wireless_toggle:
            self.on_wireless_toggle()
    
    def update_device_status(self, device: QuestDevice):
        """Update the GUI based on device status."""
        self.state.update_device(device)
        
        # Update status indicator
        self.status_indicator.update_status(device)
        
        # Update status text and button states
        if device.is_wifi and device.is_authorized:
            self.status_text.set("מכשיר מחובר אלחוטית")
            self.wireless_btn.config(text="🔌 נתק אלחוטית", state="normal")
            self.cast_btn.config(state="normal")
        elif device.is_authorized:
            self.status_text.set("מכשיר מחובר")
            self.wireless_btn.config(
                text="📡 חיבור אלחוטי",
                state="normal" if device.is_usb else "disabled"
            )
            self.cast_btn.config(state="normal")
        elif device.state == DeviceState.UNAUTHORIZED:
            self.status_text.set("אשר גישה במכשיר (Always Allow)")
            self.wireless_btn.config(text="📡 חיבור אלחוטי", state="disabled")
            self.cast_btn.config(state="disabled")
        else:
            self.status_text.set("וודא שהקווסט דלוק ומחובר למחשב")
            self.wireless_btn.config(text="📡 חיבור אלחוטי", state="disabled")
            self.cast_btn.config(state="disabled")
    
    def show_error(self, title: str, message: str):
        """Show an error message dialog."""
        messagebox.showerror(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show a warning message dialog."""
        messagebox.showwarning(title, message)
    
    def show_info(self, title: str, message: str):
        """Show an info message dialog."""
        messagebox.showinfo(title, message)
    
    def show_rtl_info(self, title: str, message: str):
        """Show an RTL info dialog."""
        RTLDialog.show_info(self.window, title, message)
    
    def run(self):
        """Start the GUI main loop."""
        logger.info("Starting GUI main loop")
        self.window.mainloop()
    
    def schedule_callback(self, callback: Callable, delay_ms: int):
        """Schedule a callback to run after a delay."""
        self.window.after(delay_ms, callback)
