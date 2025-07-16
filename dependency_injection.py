"""Dependency injection container for better testability and modularity."""

from typing import Dict, Any, Type, TypeVar, Optional, Callable
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod

T = TypeVar('T')


class Container:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
    
    def register_singleton(self, interface: Type[T], implementation: T) -> None:
        """Register a singleton service."""
        key = interface.__name__
        self._singletons[key] = implementation
        self.logger.debug(f"Registered singleton: {key}")
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Register a factory function for creating instances."""
        key = interface.__name__
        self._factories[key] = factory
        self.logger.debug(f"Registered factory: {key}")
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a specific instance."""
        key = interface.__name__
        self._services[key] = instance
        self.logger.debug(f"Registered instance: {key}")
    
    def get(self, interface: Type[T]) -> T:
        """Get service instance."""
        key = interface.__name__
        
        # Check singletons first
        if key in self._singletons:
            return self._singletons[key]
        
        # Check registered instances
        if key in self._services:
            return self._services[key]
        
        # Check factories
        if key in self._factories:
            instance = self._factories[key]()
            self._singletons[key] = instance  # Cache as singleton
            return instance
        
        raise ValueError(f"Service not registered: {key}")
    
    def has(self, interface: Type[T]) -> bool:
        """Check if service is registered."""
        key = interface.__name__
        return key in self._services or key in self._factories or key in self._singletons


@dataclass
class ServiceConfiguration:
    """Configuration for service registration."""
    log_level: str = "INFO"
    config_path: Optional[str] = None
    src_dir: str = "src"
    icon_path: Optional[str] = None


class ServiceRegistry:
    """Service registry with automatic dependency resolution."""
    
    def __init__(self, config: ServiceConfiguration):
        self.config = config
        self.container = Container()
        self._setup_logging()
        self._register_core_services()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _register_core_services(self):
        """Register all core services with proper dependencies."""
        from enhanced_config import ConfigManager
        from error_handling import ErrorHandler
        from platform_detector import PlatformDetector
        from service_factory import ServiceFactory
        
        # Core services
        self.container.register_factory(
            ConfigManager,
            lambda: ConfigManager(self.config.config_path)
        )
        
        self.container.register_factory(
            ErrorHandler,
            lambda: ErrorHandler(logging.getLogger("error_handler"))
        )
        
        self.container.register_singleton(
            PlatformDetector,
            PlatformDetector()
        )
        
        # Platform service
        self.container.register_factory(
            'PlatformService',
            ServiceFactory.create_platform_service
        )
    
    def register_application_services(self):
        """Register application-specific services."""
        from adb_manager import ADBManager
        from cast_manager import CastManager
        from async_operations import AsyncDeviceManager
        
        config_manager = self.container.get(ConfigManager)
        error_handler = self.container.get(ErrorHandler)
        app_config = config_manager.load_config()
        
        # ADB Manager
        self.container.register_factory(
            ADBManager,
            lambda: ADBManager(app_config, self.config.src_dir)
        )
        
        # Cast Manager
        self.container.register_factory(
            CastManager,
            lambda: CastManager(app_config, self.config.src_dir)
        )
        
        # Async Device Manager
        self.container.register_factory(
            AsyncDeviceManager,
            lambda: AsyncDeviceManager(
                self.container.get(ADBManager),
                error_handler
            )
        )
    
    def get_service(self, service_type: Type[T]) -> T:
        """Get a service instance."""
        return self.container.get(service_type)
    
    def create_application(self):
        """Create the main application with all dependencies injected."""
        from enhanced_application import EnhancedCastingApplication
        
        return EnhancedCastingApplication(
            config_manager=self.container.get(ConfigManager),
            error_handler=self.container.get(ErrorHandler),
            adb_manager=self.container.get(ADBManager),
            cast_manager=self.container.get(CastManager),
            async_device_manager=self.container.get(AsyncDeviceManager),
            platform_service=self.container.get('PlatformService'),
            icon_path=self.config.icon_path or "temp.ico"
        )
