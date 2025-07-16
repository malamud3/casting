"""Abstract interfaces for the casting application following SOLID principles."""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Optional
import subprocess
import tkinter as tk


class IPlatformDetector(ABC):
    """Interface for platform detection."""
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Get the current platform name."""
        pass
    
    @abstractmethod
    def is_windows(self) -> bool:
        """Check if running on Windows."""
        pass
    
    @abstractmethod
    def is_macos(self) -> bool:
        """Check if running on macOS."""
        pass
    
    @abstractmethod
    def is_linux(self) -> bool:
        """Check if running on Linux."""
        pass


class IExecutableFinder(ABC):
    """Interface for finding platform-specific executables."""
    
    @abstractmethod
    def find_adb_executable(self, src_dir: str) -> str:
        """Find the ADB executable for the current platform."""
        pass
    
    @abstractmethod
    def find_scrcpy_executable(self, src_dir: str) -> str:
        """Find the scrcpy executable for the current platform."""
        pass
    
    @abstractmethod
    def find_system_executable(self, name: str) -> Optional[str]:
        """Find an executable in the system PATH."""
        pass


class IProcessManager(ABC):
    """Interface for managing platform-specific process operations."""
    
    @abstractmethod
    def get_subprocess_flags(self) -> Dict:
        """Get platform-specific subprocess flags."""
        pass
    
    @abstractmethod
    def run_casting_command(self, scrcpy_path: str, args: List[str], src_dir: str) -> subprocess.Popen:
        """Run a casting command with platform-specific settings."""
        pass


class IUITheme(ABC):
    """Interface for UI theming."""
    
    @abstractmethod
    def get_system_font(self) -> Tuple[str, int]:
        """Get the system font for the platform."""
        pass
    
    @abstractmethod
    def get_primary_button_style(self) -> Dict:
        """Get primary button styling."""
        pass
    
    @abstractmethod
    def get_secondary_button_style(self) -> Dict:
        """Get secondary button styling."""
        pass
    
    @abstractmethod
    def apply_window_styling(self, window: tk.Tk) -> None:
        """Apply platform-specific window styling."""
        pass


class IInstructionProvider(ABC):
    """Interface for providing platform-specific instructions."""
    
    @abstractmethod
    def get_installation_instructions(self) -> str:
        """Get platform-specific installation instructions."""
        pass
