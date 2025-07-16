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
from models import AppState, QuestDevice, Transport, DeviceState
from adb_manager import ADBManager
from cast_manager import CastManager
from beautiful_gui import CastingGUI
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
                    if current_device.state == DeviceState.UNAUTHORIZED:
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
                Transport.UNKNOWN,
                DeviceState.UNKNOWN, 
                None
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
