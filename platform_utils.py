"""DEPRECATED: Legacy platform utilities - Use service_factory.py instead.

This file is kept for backward compatibility. 
New code should use the modular services from service_factory.py
"""

import warnings
from service_factory import ServiceFactory

# Issue deprecation warning
warnings.warn(
    "platform_utils.py is deprecated. Use ServiceFactory.create_platform_service() instead.",
    DeprecationWarning,
    stacklevel=2
)

# Create a singleton instance for backward compatibility
_service = ServiceFactory.create_platform_service()

class PlatformManager:
    """DEPRECATED: Legacy wrapper around the new modular platform service."""
    
    def __init__(self):
        warnings.warn(
            "PlatformManager is deprecated. Use ServiceFactory.create_platform_service() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self.service = _service
    
    @property
    def system(self):
        return self.service.get_platform_name()
    
    @property
    def is_windows(self):
        return self.service.is_windows()
    
    @property
    def is_macos(self):
        return self.service.is_macos()
    
    @property
    def is_linux(self):
        return self.service.is_linux()
    
    def get_adb_executable(self, src_dir: str) -> str:
        return self.service.get_adb_executable(src_dir)
    
    def get_scrcpy_executable(self, src_dir: str) -> str:
        return self.service.get_scrcpy_executable(src_dir)
    
    def get_subprocess_flags(self) -> dict:
        return self.service.get_subprocess_flags()
    
    def run_casting_command(self, scrcpy_path: str, args: list, src_dir: str):
        return self.service.run_casting_command(scrcpy_path, args, src_dir)
    
    def _find_system_executable(self, name: str):
        return self.service.find_system_executable(name)
    
    def get_installation_instructions(self) -> str:
        return self.service.get_installation_instructions()


# Global platform manager instance for backward compatibility
platform_manager = PlatformManager()
