"""Platform detection service following Single Responsibility Principle."""

import platform
from interfaces import IPlatformDetector


class PlatformDetector(IPlatformDetector):
    """Concrete implementation of platform detection."""
    
    def __init__(self):
        self._platform_name = platform.system().lower()
    
    def get_platform_name(self) -> str:
        """Get the current platform name."""
        return self._platform_name
    
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self._platform_name == "windows"
    
    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return self._platform_name == "darwin"
    
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return self._platform_name == "linux"
