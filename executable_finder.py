"""Executable finder service for locating platform-specific binaries."""

import os
import subprocess
from typing import Optional
from interfaces import IExecutableFinder, IPlatformDetector


class ExecutableFinder(IExecutableFinder):
    """Concrete implementation for finding executables."""
    
    def __init__(self, platform_detector: IPlatformDetector):
        self.platform_detector = platform_detector
    
    def find_adb_executable(self, src_dir: str) -> str:
        """Find the ADB executable for the current platform."""
        if self.platform_detector.is_windows():
            return os.path.join(src_dir, "adb.exe")
        else:
            # Try system ADB first, then bundled version
            system_adb = self.find_system_executable("adb")
            if system_adb:
                return system_adb
            return os.path.join(src_dir, "adb")
    
    def find_scrcpy_executable(self, src_dir: str) -> str:
        """Find the scrcpy executable for the current platform."""
        if self.platform_detector.is_windows():
            return os.path.join(src_dir, "scrcpy.exe")
        else:
            # Try system scrcpy first, then bundled version
            system_scrcpy = self.find_system_executable("scrcpy")
            if system_scrcpy:
                return system_scrcpy
            return os.path.join(src_dir, "scrcpy")
    
    def find_system_executable(self, name: str) -> Optional[str]:
        """Find an executable in the system PATH."""
        try:
            command = ["where", name] if self.platform_detector.is_windows() else ["which", name]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')[0] if result.stdout else None
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
