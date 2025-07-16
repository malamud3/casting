"""Process management service for platform-specific subprocess operations."""

import subprocess
from typing import Dict, List
from interfaces import IProcessManager, IPlatformDetector


class ProcessManager(IProcessManager):
    """Concrete implementation for process management."""
    
    def __init__(self, platform_detector: IPlatformDetector):
        self.platform_detector = platform_detector
    
    def get_subprocess_flags(self) -> Dict:
        """Get platform-specific subprocess flags."""
        if self.platform_detector.is_windows():
            return {"creationflags": 0x08000000}  # CREATE_NO_WINDOW
        else:
            return {}
    
    def run_casting_command(self, scrcpy_path: str, args: List[str], src_dir: str) -> subprocess.Popen:
        """Run a casting command with platform-specific settings."""
        cmd = [scrcpy_path] + args
        subprocess_flags = self.get_subprocess_flags()
        
        return subprocess.Popen(
            cmd,
            cwd=src_dir,
            **subprocess_flags
        )
