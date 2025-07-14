"""Cross-platform utilities for the casting application."""

import os
import platform
import subprocess
from typing import List, Optional


class PlatformManager:
    """Manages platform-specific operations and file paths."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_macos = self.system == "darwin"
        self.is_linux = self.system == "linux"
    
    def get_adb_executable(self, src_dir: str) -> str:
        """Get the appropriate ADB executable for the current platform."""
        if self.is_windows:
            return os.path.join(src_dir, "adb.exe")
        else:
            # On macOS/Linux, try system ADB first, then bundled version
            system_adb = self._find_system_executable("adb")
            if system_adb:
                return system_adb
            return os.path.join(src_dir, "adb")
    
    def get_scrcpy_executable(self, src_dir: str) -> str:
        """Get the appropriate scrcpy executable for the current platform."""
        if self.is_windows:
            return os.path.join(src_dir, "scrcpy.exe")
        else:
            # On macOS/Linux, try system scrcpy first, then bundled version
            system_scrcpy = self._find_system_executable("scrcpy")
            if system_scrcpy:
                return system_scrcpy
            return os.path.join(src_dir, "scrcpy")
    
    def get_subprocess_flags(self) -> dict:
        """Get platform-appropriate subprocess flags."""
        if self.is_windows:
            return {"creationflags": 0x08000000}  # CREATE_NO_WINDOW
        else:
            return {}
    
    def run_casting_command(self, scrcpy_path: str, args: List[str], src_dir: str) -> subprocess.Popen:
        """Run the casting command with platform-appropriate method."""
        cmd = [scrcpy_path] + args
        
        subprocess_flags = self.get_subprocess_flags()
        
        return subprocess.Popen(
            cmd,
            cwd=src_dir,
            **subprocess_flags
        )
    
    def _find_system_executable(self, name: str) -> Optional[str]:
        """Find an executable in the system PATH."""
        try:
            result = subprocess.run(
                ["which", name] if not self.is_windows else ["where", name],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')[0] if result.stdout else None
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def get_installation_instructions(self) -> str:
        """Get platform-specific installation instructions for missing dependencies."""
        if self.is_macos:
            return """
macOS Installation:
1. Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. Install dependencies: brew install scrcpy android-platform-tools
3. Enable developer mode on Quest and connect via USB
            """
        elif self.is_linux:
            return """
Linux Installation:
1. Ubuntu/Debian: sudo apt install scrcpy adb
2. Fedora: sudo dnf install scrcpy android-tools
3. Arch: sudo pacman -S scrcpy android-tools
4. Enable developer mode on Quest and connect via USB
            """
        else:
            return """
Windows Installation:
1. Download ADB and scrcpy executables to src/ folder
2. Install Oculus ADB drivers
3. Enable developer mode on Quest and connect via USB
            """


# Global platform manager instance
platform_manager = PlatformManager()
