#!/usr/bin/env python3
"""
Beautiful GUI Demo - Showcases the improved visual design
"""

import tkinter as tk
from beautiful_gui import BeautifulCastingGUI, ModernColors
from models import QuestDevice, DeviceState, Transport
from config import AppConfig

class MockConfig:
    """Mock configuration for demo."""
    colors = {}

class GUIBeautyDemo:
    """Demo showcasing the beautiful GUI improvements."""
    
    def __init__(self):
        self.demo_states = [
            ("🔴 Disconnected", QuestDevice(Transport.UNKNOWN, DeviceState.UNKNOWN)),
            ("🟡 Unauthorized", QuestDevice(Transport.USB, DeviceState.UNAUTHORIZED, "12345")),
            ("🟢 USB Connected", QuestDevice(Transport.USB, DeviceState.DEVICE, "12345")),
            ("📡 WiFi Connected", QuestDevice(Transport.WIFI, DeviceState.DEVICE, "192.168.1.100:5555"))
        ]
        self.current_state = 0
        
        # Create the beautiful GUI
        self.gui = BeautifulCastingGUI(MockConfig(), "temp.ico")
        
        # Setup demo controls
        self.setup_demo_controls()
        
        # Set initial state
        self.update_demo_state()
        
    def setup_demo_controls(self):
        """Add demo controls to the GUI."""
        # Create demo control frame at the top
        demo_frame = tk.Frame(self.gui.window, bg=ModernColors.BG_SECONDARY, relief='ridge', bd=1)
        demo_frame.pack(fill='x', padx=10, pady=(10, 0), before=self.gui.window.winfo_children()[0])
        
        tk.Label(
            demo_frame,
            text="🎨 Beautiful GUI Demo - Click to cycle through states",
            bg=ModernColors.BG_SECONDARY,
            fg=ModernColors.TEXT_PRIMARY,
            font=('Arial', 11, 'bold'),
            pady=10
        ).pack()
        
        # Add click binding to window for state cycling
        self.gui.window.bind('<Button-1>', self.cycle_demo_state)
        self.gui.window.bind('<space>', self.cycle_demo_state)
        
        # Display current state
        self.state_label = tk.Label(
            demo_frame,
            text=f"Current: {self.demo_states[self.current_state][0]}",
            bg=ModernColors.BG_SECONDARY,
            fg=ModernColors.PRIMARY_BLUE,
            font=('Arial', 9)
        )
        self.state_label.pack(pady=(0, 10))
        
    def cycle_demo_state(self, event=None):
        """Cycle to the next demo state."""
        self.current_state = (self.current_state + 1) % len(self.demo_states)
        self.update_demo_state()
        
    def update_demo_state(self):
        """Update the GUI to show the current demo state."""
        state_name, device = self.demo_states[self.current_state]
        
        # Update the GUI
        self.gui.update_device_status(device)
        
        # Update demo label
        if hasattr(self, 'state_label'):
            self.state_label.config(text=f"Current: {state_name}")
            
        # Show info about current state
        messages = {
            0: "No device detected - buttons disabled",
            1: "Device needs authorization - cast disabled", 
            2: "USB connected - ready to cast and go wireless",
            3: "WiFi connected - wireless casting active"
        }
        
        print(f"Demo State: {state_name}")
        print(f"Info: {messages[self.current_state]}")
        
    def run(self):
        """Run the beautiful GUI demo."""
        print("🎨 Beautiful GUI Demo Starting!")
        print("✨ Click anywhere or press space to cycle through states")
        print("🎯 See how the modern design responds to different device states")
        
        # Setup mock callbacks
        self.gui.on_cast_requested = lambda: print("🎬 Cast button clicked!")
        self.gui.on_wireless_toggle = lambda: print("📡 Wireless button clicked!")
        
        # Start the GUI
        self.gui.run()


if __name__ == "__main__":
    try:
        demo = GUIBeautyDemo()
        demo.run()
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()
