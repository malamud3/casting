"""Platform-specific instruction provider service."""

from interfaces import IInstructionProvider, IPlatformDetector


class InstructionProvider(IInstructionProvider):
    """Concrete implementation for providing platform-specific instructions."""
    
    def __init__(self, platform_detector: IPlatformDetector):
        self.platform_detector = platform_detector
    
    def get_installation_instructions(self) -> str:
        """Get platform-specific installation instructions."""
        if self.platform_detector.is_macos():
            return """
macOS Installation:
1. Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. Install dependencies: brew install scrcpy android-platform-tools
3. Enable developer mode on Quest and connect via USB
            """
        elif self.platform_detector.is_linux():
            return """
Linux Installation:
1. Ubuntu/Debian: sudo apt install scrcpy adb
2. Fedora: sudo dnf install scrcpy android-tools
3. Arch: sudo pacman -S scrcpy android-tools
4. Enable developer mode on Quest and connect via USB
            """
        else:  # Windows
            return """
Windows Installation:
1. Download ADB and scrcpy executables to src/ folder
2. Install Oculus ADB drivers
3. Enable developer mode on Quest and connect via USB
            """
