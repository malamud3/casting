"""ADB utility functions and device management."""

import logging
import re
import subprocess
from subprocess import PIPE, STDOUT
from typing import Optional, List

from config import AppConfig
from models import QuestDevice, Transport, DeviceState
from platform_utils import platform_manager


logger = logging.getLogger(__name__)


class ADBManager:
    """Manages ADB operations and device detection."""
    
    def __init__(self, config: AppConfig, src_dir: str):
        self.config = config
        self.src_dir = src_dir
        self.adb_path = platform_manager.get_adb_executable(src_dir)
    
    def run_adb_command(self, args: List[str], **kwargs) -> subprocess.CompletedProcess:
        """Run an ADB command with standard configuration."""
        cmd = [self.adb_path] + args
        
        # Set default subprocess options
        kwargs.setdefault("check", False)
        kwargs.setdefault("stdout", PIPE)
        kwargs.setdefault("stderr", STDOUT)
        kwargs.setdefault("text", True)
        kwargs.setdefault("timeout", self.config.adb_timeout_ms / 1000)
        
        # Add platform-specific flags
        subprocess_flags = platform_manager.get_subprocess_flags()
        kwargs.update(subprocess_flags)
        
        logger.debug(f"Running ADB command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, **kwargs)
            logger.debug(f"ADB command result: {result.returncode}, output: {result.stdout}")
            return result
        except subprocess.TimeoutExpired as e:
            logger.error(f"ADB command timed out: {e}")
            raise
        except Exception as e:
            logger.error(f"ADB command failed: {e}")
            raise
    
    def get_devices_output(self) -> str:
        """Get the output of 'adb devices -l' command."""
        result = self.run_adb_command(["devices", "-l"])
        return result.stdout or ""
    
    def detect_quest_device(self) -> QuestDevice:
        """
        Detect and return the current Quest device state.
        
        Returns:
            QuestDevice with current connection state
        """
        wifi_device: Optional[QuestDevice] = None
        usb_device: Optional[QuestDevice] = None
        
        devices_output = self.get_devices_output()
        logger.debug(f"ADB devices output: {devices_output}")
        
        for line in devices_output.splitlines()[1:]:  # Skip header
            parts = line.split()
            if len(parts) < 2:
                continue
                
            serial, state_str = parts[0], parts[1]
            
            # Parse device state
            try:
                state = DeviceState(state_str)
            except ValueError:
                state = DeviceState.UNKNOWN
            
            # Determine transport type
            if ":" in serial:  # Wi-Fi connection (IP:port format)
                transport = Transport.WIFI
                if wifi_device is None:  # Keep first Wi-Fi device only
                    wifi_device = QuestDevice(transport, state, serial)
            else:  # USB connection
                transport = Transport.USB
                if usb_device is None:  # Keep first USB device only
                    usb_device = QuestDevice(transport, state, serial)
        
        # Prefer Wi-Fi over USB
        detected_device = wifi_device or usb_device
        
        if detected_device is None:
            # No devices found
            detected_device = QuestDevice(
                Transport.UNKNOWN, 
                DeviceState.UNKNOWN, 
                None
            )
        
        logger.info(f"Detected device: {detected_device}")
        return detected_device
    
    def get_wifi_ip(self) -> Optional[str]:
        """
        Get the Wi-Fi IP address of the connected Quest device.
        
        Returns:
            IP address string or None if not found
        """
        try:
            result = self.run_adb_command([
                "shell", "ip", "-f", "inet", "addr", "show", "wlan0"
            ])
            
            if result.returncode == 0 and result.stdout:
                match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", result.stdout)
                if match:
                    ip = match.group(1)
                    logger.info(f"Found Wi-Fi IP: {ip}")
                    return ip
            
            logger.warning("Could not extract Wi-Fi IP from device")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get Wi-Fi IP: {e}")
            return None
    
    def enable_wireless_adb(self) -> bool:
        """
        Enable ADB over TCP/IP on the wireless port.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Enable TCP/IP mode
            result = self.run_adb_command(["tcpip", self.config.wireless_port])
            if result.returncode != 0:
                logger.error(f"Failed to enable tcpip mode: {result.stdout}")
                return False
            
            logger.info("Successfully enabled ADB over TCP/IP")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable wireless ADB: {e}")
            return False
    
    def connect_wireless(self, ip: str) -> tuple[bool, str]:
        """
        Connect to device over Wi-Fi.
        
        Args:
            ip: IP address of the device
            
        Returns:
            Tuple of (success, message)
        """
        wifi_address = f"{ip}:{self.config.wireless_port}"
        
        try:
            result = self.run_adb_command(["connect", wifi_address])
            output = result.stdout.strip()
            
            success = "connected" in output.lower() or "already connected" in output.lower()
            
            if success:
                logger.info(f"Successfully connected to {wifi_address}")
            else:
                logger.warning(f"Failed to connect to {wifi_address}: {output}")
            
            return success, output
            
        except Exception as e:
            error_msg = f"Connection failed: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def disconnect_wireless(self, address: Optional[str] = None) -> bool:
        """
        Disconnect from wireless ADB and switch back to USB.
        
        Args:
            address: Specific address to disconnect (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if address:
                result = self.run_adb_command(["disconnect", address])
                logger.info(f"Disconnected from {address}: {result.stdout}")
            
            # Switch back to USB mode
            result = self.run_adb_command(["usb"])
            logger.info("Switched back to USB mode")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disconnect wireless: {e}")
            return False
    
    def find_wifi_serial(self) -> Optional[str]:
        """
        Find the first Wi-Fi serial (IP:port) in ADB devices list.
        
        Returns:
            Wi-Fi serial string or None if not found
        """
        devices_output = self.get_devices_output()
        
        for line in devices_output.splitlines()[1:]:
            parts = line.split()
            if parts and ":" in parts[0]:
                logger.debug(f"Found Wi-Fi serial: {parts[0]}")
                return parts[0]
        
        logger.debug("No Wi-Fi serial found in devices list")
        return None
