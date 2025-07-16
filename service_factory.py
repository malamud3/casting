"""Service factory for creating and configuring platform services with dependency injection."""

from platform_detector import PlatformDetector
from executable_finder import ExecutableFinder
from process_manager import ProcessManager
from instruction_provider import InstructionProvider
from ui_theme_factory import UIThemeFactory
from platform_service import PlatformService


class ServiceFactory:
    """
    Factory for creating configured platform services.
    Implements dependency injection pattern.
    """
    
    @staticmethod
    def create_platform_service() -> PlatformService:
        """
        Create a fully configured platform service with all dependencies injected.
        
        Returns:
            PlatformService: Configured service with all platform-specific implementations
        """
        # Create platform detector (foundation service)
        platform_detector = PlatformDetector()
        
        # Create dependent services using dependency injection
        executable_finder = ExecutableFinder(platform_detector)
        process_manager = ProcessManager(platform_detector)
        instruction_provider = InstructionProvider(platform_detector)
        
        # Create UI theme using factory pattern
        ui_theme = UIThemeFactory.create_theme(platform_detector)
        
        # Inject all dependencies into the main service
        return PlatformService(
            platform_detector=platform_detector,
            executable_finder=executable_finder,
            process_manager=process_manager,
            ui_theme=ui_theme,
            instruction_provider=instruction_provider
        )
