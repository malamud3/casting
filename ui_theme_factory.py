"""Factory for creating platform-specific UI themes."""

from interfaces import IUITheme, IPlatformDetector
from ui_themes import MacOSUITheme, WindowsUITheme, LinuxUITheme


class UIThemeFactory:
    """Factory for creating platform-appropriate UI themes."""
    
    @staticmethod
    def create_theme(platform_detector: IPlatformDetector) -> IUITheme:
        """Create a UI theme based on the current platform."""
        if platform_detector.is_macos():
            return MacOSUITheme()
        elif platform_detector.is_windows():
            return WindowsUITheme()
        elif platform_detector.is_linux():
            return LinuxUITheme()
        else:
            # Fallback to Linux theme for unknown platforms
            return LinuxUITheme()
