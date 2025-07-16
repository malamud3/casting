#!/usr/bin/env python3
"""
Quest Casting GUI Demonstration
A comprehensive showcase of the GUI features and visual elements
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import platform

class DeviceState(Enum):
    UNKNOWN = ""
    DEVICE = "device"
    UNAUTHORIZED = "unauthorized"
    OFFLINE = "offline"

class Transport(Enum):
    USB = "usb"
    WIFI = "wifi"
    UNKNOWN = "unknown"

@dataclass
class MockDevice:
    transport: Transport
    state: DeviceState
    serial: Optional[str] = None
    
    @property
    def is_wifi(self) -> bool:
        return self.transport == Transport.WIFI
    
    @property
    def is_usb(self) -> bool:
        return self.transport == Transport.USB
    
    @property
    def is_authorized(self) -> bool:
        return self.state == DeviceState.DEVICE

class GUIDemo:
    """Comprehensive GUI demonstration with all features."""
    
    def __init__(self):
        self.current_device = MockDevice(Transport.UNKNOWN, DeviceState.UNKNOWN)
        self.demo_mode = "disconnected"  # disconnected, unauthorized, usb_connected, wifi_connected
        self.auto_demo = False
        
        self.setup_window()
        self.setup_demo_controls()
        self.setup_main_interface()
        self.setup_status_simulation()
        
    def setup_window(self):
        """Setup the main window with professional styling."""
        self.root = tk.Tk()
        self.root.title("🎮 Quest Casting Pro - GUI Demo")
        self.root.geometry("500x600")
        self.root.configure(bg='#F2F2F7' if platform.system() == 'Darwin' else '#FFFFFF')
        
        # Prevent resizing for consistent demo
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_demo_controls(self):
        """Setup demo control panel."""
        demo_frame = tk.Frame(self.root, bg=self.root.cget('bg'), relief='ridge', bd=2)
        demo_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            demo_frame, 
            text="🎬 GUI Demo Controls", 
            font=('San Francisco', 14, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 12, 'bold'),
            bg=demo_frame.cget('bg')
        ).pack(pady=5)
        
        # Demo state buttons
        button_frame = tk.Frame(demo_frame, bg=demo_frame.cget('bg'))
        button_frame.pack(pady=5)
        
        self.demo_buttons = {}
        states = [
            ("🔴 Disconnected", "disconnected"),
            ("🟡 Unauthorized", "unauthorized"),
            ("🟢 USB Connected", "usb_connected"),
            ("📡 WiFi Connected", "wifi_connected")
        ]
        
        for i, (text, state) in enumerate(states):
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda s=state: self.set_demo_state(s),
                font=('San Francisco', 10) if platform.system() == 'Darwin' else ('Segoe UI', 9),
                width=15,
                relief='raised',
                bd=1
            )
            btn.grid(row=i//2, column=i%2, padx=3, pady=2)
            self.demo_buttons[state] = btn
            
        # Auto demo toggle
        auto_frame = tk.Frame(demo_frame, bg=demo_frame.cget('bg'))
        auto_frame.pack(pady=5)
        
        self.auto_var = tk.BooleanVar()
        auto_check = tk.Checkbutton(
            auto_frame,
            text="🔄 Auto Demo (cycles through states)",
            variable=self.auto_var,
            command=self.toggle_auto_demo,
            bg=auto_frame.cget('bg'),
            font=('San Francisco', 10) if platform.system() == 'Darwin' else ('Segoe UI', 9)
        )
        auto_check.pack()
        
    def setup_main_interface(self):
        """Setup the main casting interface."""
        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)
        
        # Main interface frame
        main_frame = tk.Frame(self.root, bg=self.root.cget('bg'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="קאסטינג LoginVR",
            font=('San Francisco', 18, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 16, 'bold'),
            bg=main_frame.cget('bg'),
            fg='#1D1D1F' if platform.system() == 'Darwin' else '#000000'
        )
        title_label.pack(pady=(0, 20))
        
        # Status indicator container
        status_container = tk.Frame(main_frame, bg=main_frame.cget('bg'))
        status_container.pack(pady=10)
        
        # Status circle (using Canvas for better control)
        self.status_canvas = tk.Canvas(
            status_container, 
            width=50, 
            height=50, 
            bg=status_container.cget('bg'),
            highlightthickness=0
        )
        self.status_canvas.pack()
        
        # Status text
        self.status_text = tk.StringVar(value="מתחבר למכשיר...")
        self.status_label = tk.Label(
            main_frame,
            textvariable=self.status_text,
            font=('San Francisco', 12) if platform.system() == 'Darwin' else ('Segoe UI', 11),
            bg=main_frame.cget('bg'),
            fg='#8E8E93' if platform.system() == 'Darwin' else '#666666',
            wraplength=350,
            justify='center'
        )
        self.status_label.pack(pady=10)
        
        # Main buttons
        self.setup_buttons(main_frame)
        
        # Menu bar
        self.setup_menu()
        
    def setup_buttons(self, parent):
        """Setup the main action buttons."""
        # Cast button
        self.cast_btn = tk.Button(
            parent,
            text="📺 הצג מסך",
            font=('San Francisco', 14, 'bold') if platform.system() == 'Darwin' else ('Segoe UI', 12, 'bold'),
            bg='#007AFF' if platform.system() == 'Darwin' else '#0078D4',
            fg='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            state='disabled',
            command=self.on_cast_clicked
        )
        self.cast_btn.pack(pady=10)
        
        # Wireless button
        self.wireless_btn = tk.Button(
            parent,
            text="📡 חיבור אלחוטי",
            font=('San Francisco', 12) if platform.system() == 'Darwin' else ('Segoe UI', 10),
            bg='#F2F2F7' if platform.system() == 'Darwin' else '#F0F0F0',
            fg='#007AFF' if platform.system() == 'Darwin' else '#0078D4',
            relief='flat',
            bd=1,
            padx=25,
            pady=8,
            state='disabled',
            command=self.on_wireless_clicked
        )
        self.wireless_btn.pack(pady=5)
        
    def setup_menu(self):
        """Setup the menu bar."""
        menubar = tk.Menu(self.root)
        menubar.add_command(label="הוראות", command=self.show_instructions)
        menubar.add_command(label="אודות", command=self.show_about)
        menubar.add_command(label="עזרה", command=self.show_help)
        self.root.config(menu=menubar)
        
    def setup_status_simulation(self):
        """Setup automatic status simulation."""
        self.update_interface()
        
    def set_demo_state(self, state):
        """Set the demo to a specific state."""
        self.demo_mode = state
        self.auto_demo = False
        self.auto_var.set(False)
        
        # Update button styling
        for btn_state, btn in self.demo_buttons.items():
            if btn_state == state:
                btn.configure(relief='sunken', bg='#007AFF', fg='white')
            else:
                btn.configure(relief='raised', bg='SystemButtonFace', fg='black')
                
        # Update device state
        if state == "disconnected":
            self.current_device = MockDevice(Transport.UNKNOWN, DeviceState.UNKNOWN)
        elif state == "unauthorized":
            self.current_device = MockDevice(Transport.USB, DeviceState.UNAUTHORIZED, "12345USB")
        elif state == "usb_connected":
            self.current_device = MockDevice(Transport.USB, DeviceState.DEVICE, "12345USB")
        elif state == "wifi_connected":
            self.current_device = MockDevice(Transport.WIFI, DeviceState.DEVICE, "192.168.1.100:5555")
            
        self.update_interface()
        
    def toggle_auto_demo(self):
        """Toggle automatic demo mode."""
        self.auto_demo = self.auto_var.get()
        if self.auto_demo:
            self.run_auto_demo()
            
    def run_auto_demo(self):
        """Run automatic demo cycle."""
        if not self.auto_demo:
            return
            
        states = ["disconnected", "unauthorized", "usb_connected", "wifi_connected"]
        current_index = states.index(self.demo_mode) if self.demo_mode in states else 0
        next_index = (current_index + 1) % len(states)
        
        self.set_demo_state(states[next_index])
        
        # Schedule next state change
        self.root.after(3000, self.run_auto_demo)  # Change every 3 seconds
        
    def update_interface(self):
        """Update the interface based on current device state."""
        # Update status circle
        self.update_status_circle()
        
        # Update status text and buttons
        if self.current_device.is_wifi and self.current_device.is_authorized:
            self.status_text.set("🎉 מכשיר מחובר אלחוטית")
            self.wireless_btn.config(
                text="🔌 נתק אלחוטית", 
                state="normal",
                bg='#FF3B30' if platform.system() == 'Darwin' else '#D13438',
                fg='white'
            )
            self.cast_btn.config(state="normal", bg='#34C759' if platform.system() == 'Darwin' else '#107C10')
        elif self.current_device.is_authorized:
            self.status_text.set("✅ מכשיר מחובר - מוכן לשידור")
            self.wireless_btn.config(
                text="📡 חיבור אלחוטי",
                state="normal" if self.current_device.is_usb else "disabled",
                bg='#F2F2F7' if platform.system() == 'Darwin' else '#F0F0F0',
                fg='#007AFF' if platform.system() == 'Darwin' else '#0078D4'
            )
            self.cast_btn.config(state="normal", bg='#007AFF' if platform.system() == 'Darwin' else '#0078D4')
        elif self.current_device.state == DeviceState.UNAUTHORIZED:
            self.status_text.set("⚠️ אשר גישה במכשיר (Always Allow)")
            self.wireless_btn.config(
                text="📡 חיבור אלחוטי", 
                state="disabled",
                bg='#F2F2F7' if platform.system() == 'Darwin' else '#F0F0F0',
                fg='#8E8E93' if platform.system() == 'Darwin' else '#666666'
            )
            self.cast_btn.config(
                state="disabled", 
                bg='#F2F2F7' if platform.system() == 'Darwin' else '#F0F0F0',
                fg='#8E8E93' if platform.system() == 'Darwin' else '#666666'
            )
        else:
            self.status_text.set("🔍 וודא שהקווסט דלוק ומחובר למחשב")
            self.wireless_btn.config(
                text="📡 חיבור אלחוטי", 
                state="disabled",
                bg='#F2F2F7' if platform.system() == 'Darwin' else '#F0F0F0',
                fg='#8E8E93' if platform.system() == 'Darwin' else '#666666'
            )
            self.cast_btn.config(
                state="disabled",
                bg='#F2F2F7' if platform.system() == 'Darwin' else '#F0F0F0',
                fg='#8E8E93' if platform.system() == 'Darwin' else '#666666'
            )
            
    def update_status_circle(self):
        """Update the status indicator circle."""
        self.status_canvas.delete("all")
        
        # Determine color based on device state
        if self.current_device.is_wifi and self.current_device.is_authorized:
            color = "#34C759"  # Green for WiFi
            shadow_color = "#28A745"
        elif self.current_device.is_authorized:
            color = "#34C759"  # Green for connected
            shadow_color = "#28A745"
        elif self.current_device.state == DeviceState.UNAUTHORIZED:
            color = "#FF9500"  # Orange for unauthorized
            shadow_color = "#E8860A"
        else:
            color = "#FF3B30"  # Red for disconnected
            shadow_color = "#D32F2F"
            
        # Draw shadow
        self.status_canvas.create_oval(2, 2, 48, 48, fill=shadow_color, outline="")
        
        # Draw main circle
        self.status_canvas.create_oval(0, 0, 46, 46, fill=color, outline="white", width=2)
        
        # Add WiFi indicator if applicable
        if self.current_device.is_wifi:
            # Draw WiFi symbol
            self.status_canvas.create_text(23, 23, text="📡", font=("Arial", 16))
            
    def on_cast_clicked(self):
        """Handle cast button click."""
        if self.current_device.is_authorized:
            messagebox.showinfo(
                "השידור החל",
                f"השידור החל בהצלחה!\n"
                f"מכשיר: {self.current_device.serial}\n"
                f"סוג חיבור: {'אלחוטי' if self.current_device.is_wifi else 'USB'}"
            )
        else:
            messagebox.showwarning("שגיאה", "המכשיר אינו מחובר או לא מאושר")
            
    def on_wireless_clicked(self):
        """Handle wireless button click."""
        if self.current_device.is_wifi:
            # Disconnect from wireless
            self.set_demo_state("usb_connected")
            messagebox.showinfo("נותק", "החיבור האלחוטי נותק בהצלחה")
        elif self.current_device.is_authorized and self.current_device.is_usb:
            # Connect to wireless
            messagebox.showinfo("מתחבר", "מתחבר למצב אלחוטי...")
            self.root.after(2000, lambda: self.set_demo_state("wifi_connected"))
        else:
            messagebox.showwarning("שגיאה", "לא ניתן להתחבר למצב אלחוטי")
            
    def show_instructions(self):
        """Show instructions dialog."""
        instructions = (
            "🔧 הוראות הפעלה:\n\n"
            "1. הדלק את הקווסט והפעל אפליקציה לשידור\n"
            "2. חבר את הקווסט למחשב באמצעות כבל USB\n"
            "3. אשר את הגישה דרך המכשיר (Always Allow)\n"
            "4. לחץ 'הצג מסך' להתחלת השידור\n"
            "5. לחיבור אלחוטי - לחץ 'חיבור אלחוטי' לאחר החיבור"
        )
        messagebox.showinfo("הוראות", instructions)
        
    def show_about(self):
        """Show about dialog."""
        about_text = (
            "Quest Casting Pro - GUI Demo\n\n"
            "⚡ Professional Quest casting application\n"
            "🎮 Support for Meta Quest 2/3/Pro\n"
            "📱 USB and WiFi connectivity\n"
            "🌍 Hebrew RTL interface\n"
            "🍎 macOS native styling\n\n"
            "Created by LoginVR · 2025 · v2.1.0"
        )
        messagebox.showinfo("About", about_text)
        
    def show_help(self):
        """Show help dialog."""
        help_text = (
            "🆘 עזרה ותמיכה:\n\n"
            "📧 אימייל: info@loginvr.co.il\n"
            "🌐 אתר: www.loginvr.co.il\n"
            "📹 מדריך וידאו: זמין בתפריט\n\n"
            "💡 טיפים:\n"
            "• ודא שמצב מפתח פעיל\n"
            "• השתמש בכבל USB איכותי\n"
            "• בדוק חיבור רשת לאלחוטי"
        )
        messagebox.showinfo("עזרה", help_text)
        
    def run(self):
        """Run the GUI demo."""
        # Set initial state
        self.set_demo_state("disconnected")
        
        # Add welcome message
        self.root.after(1000, lambda: messagebox.showinfo(
            "🎬 GUI Demo",
            "ברוכים הבאים להדגמת הממשק!\n\n"
            "השתמשו בכפתורי הבקרה למעלה\n"
            "כדי לראות את המצבים השונים של הממשק.\n\n"
            "אפשר גם להפעיל הדגמה אוטומטית! 🔄"
        ))
        
        # Start the main loop
        self.root.mainloop()


def main():
    """Run the GUI demonstration."""
    print("🎮 Starting Quest Casting GUI Demo...")
    print("📱 This demo showcases all GUI features and states")
    print("🔄 Use the demo controls to see different device states")
    print("✨ Enjoy the professional interface!")
    
    demo = GUIDemo()
    demo.run()


if __name__ == "__main__":
    main()
