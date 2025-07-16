"""Comprehensive platform service that aggregates all platform-specific functionality."""

from interfaces import (
    IPlatformDetector, IExecutableFinder, IProcessManager, 
    IUITheme, IInstructionProvider
)


class PlatformService:
    """
    Aggregates platform-specific services following Dependency Inversion Principle.
    High-level modules depend on abstractions, not concretions.
    """
    
    def __init__(
        self,
        platform_detector: IPlatformDetector,
        executable_finder: IExecutableFinder,
        process_manager: IProcessManager,
        ui_theme: IUITheme,
        instruction_provider: IInstructionProvider
    ):
        self.platform_detector = platform_detector
        self.executable_finder = executable_finder
        self.process_manager = process_manager
        self.ui_theme = ui_theme
        self.instruction_provider = instruction_provider
    
    # Platform detection methods
    def get_platform_name(self) -> str:
        """Get the current platform name."""
        return self.platform_detector.get_platform_name()
    
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self.platform_detector.is_windows()
    
    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return self.platform_detector.is_macos()
    
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return self.platform_detector.is_linux()
    
    # Executable finding methods
    def get_adb_executable(self, src_dir: str) -> str:
        """Find the ADB executable for the current platform."""
        return self.executable_finder.find_adb_executable(src_dir)
    
    def get_scrcpy_executable(self, src_dir: str) -> str:
        """Find the scrcpy executable for the current platform."""
        return self.executable_finder.find_scrcpy_executable(src_dir)
    
    def find_system_executable(self, name: str):
        """Find an executable in the system PATH."""
        return self.executable_finder.find_system_executable(name)
    
    # Process management methods
    def get_subprocess_flags(self) -> dict:
        """Get platform-specific subprocess flags."""
        return self.process_manager.get_subprocess_flags()
    
    def run_casting_command(self, scrcpy_path: str, args: list, src_dir: str):
        """Run a casting command with platform-specific settings."""
        return self.process_manager.run_casting_command(scrcpy_path, args, src_dir)
    
    # UI theme methods
    def get_system_font(self):
        """Get the system font for the platform."""
        return self.ui_theme.get_system_font()
    
    def get_primary_button_style(self):
        """Get primary button styling."""
        return self.ui_theme.get_primary_button_style()
    
    def get_secondary_button_style(self):
        """Get secondary button styling."""
        return self.ui_theme.get_secondary_button_style()
    
    def apply_window_styling(self, window):
        """Apply platform-specific window styling."""
        return self.ui_theme.apply_window_styling(window)
    
    # Instruction methods
    def get_installation_instructions(self) -> str:
        """Get platform-specific installation instructions."""
        return self.instruction_provider.get_installation_instructions()
