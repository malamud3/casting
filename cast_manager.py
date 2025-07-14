"""Screen casting functionality using scrcpy."""

import logging
import os
import subprocess
from typing import Optional

from config import AppConfig
from models import QuestDevice
from platform_utils import platform_manager


logger = logging.getLogger(__name__)


class CastManager:
    """Manages screen casting operations using scrcpy."""
    
    def __init__(self, config: AppConfig, src_dir: str):
        self.config = config
        self.src_dir = src_dir
        self.scrcpy_path = platform_manager.get_scrcpy_executable(src_dir)
    
    def start_casting(self, device: QuestDevice, wifi_serial: Optional[str] = None) -> bool:
        """
        Start screen casting to the specified device.
        
        Args:
            device: The Quest device to cast
            wifi_serial: Optional Wi-Fi serial to prefer over device serial
            
        Returns:
            True if casting started successfully, False otherwise
        """
        # Choose target serial: prefer Wi-Fi, fallback to device serial
        target_serial = wifi_serial or device.serial
        
        try:
            # Generate scrcpy command
            cmd = self.generate_scrcpy_command(target_serial)
            
            logger.info(f"Starting cast with command: {' '.join(cmd)}")
            
            # Use platform manager to run the command
            process = platform_manager.run_casting_command(
                self.scrcpy_path, 
                cmd[1:],  # Remove scrcpy path from args
                self.src_dir
            )
            
            logger.info(f"Cast process started with PID: {process.pid}")
            return True
            
        except FileNotFoundError:
            logger.error(f"scrcpy executable not found at: {self.scrcpy_path}")
            return False
        except Exception as e:
            logger.error(f"Failed to start casting: {e}")
            return False
    
    def generate_scrcpy_command(self, serial: Optional[str] = None) -> list[str]:
        """
        Generate scrcpy command with current configuration.
        
        Args:
            serial: Device serial (optional)
            
        Returns:
            List of command arguments
        """
        cmd = [self.scrcpy_path]
        
        # Add serial if specified
        if serial:
            cmd.extend(["-s", serial])
        
        # Add configuration options
        config = self.config.scrcpy
        cmd.extend([
            "--render-driver", config.render_driver,
            "--crop", config.crop,
            "-b", config.bitrate,
            "--max-size", str(config.max_size),
            "--video-codec", config.video_codec,
            "--video-encoder", config.video_encoder,
        ])
        
        if config.no_audio:
            cmd.append("--no-audio")
        
        if config.no_control:
            cmd.append("-n")
        
        return cmd
    
    def check_dependencies(self) -> tuple[bool, str]:
        """
        Check if required dependencies (scrcpy, adb) are available.
        
        Returns:
            Tuple of (dependencies_available, error_message)
        """
        missing = []
        
        # Check scrcpy
        if not os.path.exists(self.scrcpy_path):
            if not platform_manager._find_system_executable("scrcpy"):
                missing.append("scrcpy")
        
        # Check ADB  
        adb_path = platform_manager.get_adb_executable(self.src_dir)
        if not os.path.exists(adb_path):
            if not platform_manager._find_system_executable("adb"):
                missing.append("adb")
        
        if missing:
            instructions = platform_manager.get_installation_instructions()
            error_msg = f"Missing dependencies: {', '.join(missing)}\n\n{instructions}"
            return False, error_msg
        
        return True, ""
