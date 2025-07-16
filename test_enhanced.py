"""Professional test suite for Quest Casting Application."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import tempfile
import shutil

from error_handling import ErrorHandler, ApplicationError, ErrorSeverity
from async_operations import AsyncDeviceManager
from enhanced_config import ConfigManager
from dependency_injection import Container, ServiceRegistry, ServiceConfiguration


class TestErrorHandling:
    """Test error handling system."""
    
    def setup_method(self):
        self.error_handler = ErrorHandler()
    
    def test_create_application_error(self):
        """Test ApplicationError creation."""
        error = self.error_handler.create_error(
            "TEST_001",
            "Test error message",
            ErrorSeverity.ERROR
        )
        
        assert isinstance(error, ApplicationError)
        assert error.code == "TEST_001"
        assert error.message == "Test error message"
        assert error.severity == ErrorSeverity.ERROR
    
    def test_hebrew_translation(self):
        """Test Hebrew error translation."""
        error = self.error_handler.create_error(
            "DEVICE_NOT_FOUND",
            "Device not found",
            ErrorSeverity.WARNING
        )
        
        hebrew_msg = self.error_handler.get_user_message(error)
        assert hebrew_msg  # Should have Hebrew translation
        assert hebrew_msg != error.message  # Should be different from English
    
    def test_error_context(self):
        """Test error context handling."""
        with pytest.raises(ApplicationError) as exc_info:
            self.error_handler.handle_error(
                Exception("Test exception"),
                "TEST_CONTEXT",
                {"device_id": "12345"}
            )
        
        error = exc_info.value
        assert error.context == {"device_id": "12345"}


class TestAsyncOperations:
    """Test async device operations."""
    
    def setup_method(self):
        self.manager = AsyncDeviceManager()
    
    @pytest.mark.asyncio
    async def test_async_device_scan(self):
        """Test async device scanning."""
        progress_updates = []
        
        def progress_callback(progress: float, status: str):
            progress_updates.append((progress, status))
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "device1\tdevice\ndevice2\tdevice\n"
            mock_run.return_value.returncode = 0
            
            devices = await self.manager.scan_devices(progress_callback)
            
            assert len(devices) == 2
            assert len(progress_updates) > 0
            assert progress_updates[-1][0] == 1.0  # Should reach 100%
    
    @pytest.mark.asyncio
    async def test_async_connection(self):
        """Test async device connection."""
        with patch.object(self.manager, '_run_command') as mock_command:
            mock_command.return_value = (0, "connected", "")
            
            result = await self.manager.connect_device("192.168.1.100")
            assert result is True
    
    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """Test connection timeout handling."""
        with patch.object(self.manager, '_run_command') as mock_command:
            # Simulate timeout
            mock_command.side_effect = asyncio.TimeoutError()
            
            result = await self.manager.connect_device("192.168.1.100", timeout=1.0)
            assert result is False


class TestConfigManager:
    """Test configuration management."""
    
    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config_file = self.temp_dir / "test_config.yaml"
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_config_creation(self):
        """Test configuration creation and validation."""
        config_data = {
            "application": {
                "title": "Test App",
                "version": "1.0.0",
                "theme": "dark"
            },
            "logging": {
                "level": "DEBUG",
                "file_enabled": True
            }
        }
        
        # Write test config
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        manager = ConfigManager(str(self.config_file))
        config = manager.get_config()
        
        assert config.application.title == "Test App"
        assert config.application.version == "1.0.0"
        assert config.logging.level == "DEBUG"
    
    def test_config_validation(self):
        """Test configuration validation."""
        invalid_config = {
            "application": {
                "title": "",  # Invalid empty title
                "version": "invalid",  # Invalid version format
                "theme": "invalid_theme"  # Invalid theme
            }
        }
        
        import yaml
        with open(self.config_file, 'w') as f:
            yaml.dump(invalid_config, f)
        
        with pytest.raises(Exception):  # Should raise validation error
            ConfigManager(str(self.config_file))


class TestDependencyInjection:
    """Test dependency injection system."""
    
    def setup_method(self):
        self.container = Container()
    
    def test_service_registration(self):
        """Test service registration and resolution."""
        # Register a mock service
        mock_service = Mock()
        self.container.register("test_service", lambda: mock_service)
        
        # Resolve service
        resolved = self.container.resolve("test_service")
        assert resolved is mock_service
    
    def test_singleton_behavior(self):
        """Test singleton service behavior."""
        call_count = 0
        
        def factory():
            nonlocal call_count
            call_count += 1
            return Mock()
        
        self.container.register("singleton_service", factory, singleton=True)
        
        # Resolve multiple times
        service1 = self.container.resolve("singleton_service")
        service2 = self.container.resolve("singleton_service")
        
        assert service1 is service2
        assert call_count == 1
    
    def test_dependency_resolution(self):
        """Test automatic dependency resolution."""
        # Register dependencies
        self.container.register("dep1", lambda: Mock())
        self.container.register("dep2", lambda: Mock())
        
        # Register service with dependencies
        def service_factory(dep1, dep2):
            service = Mock()
            service.dep1 = dep1
            service.dep2 = dep2
            return service
        
        self.container.register("service_with_deps", service_factory)
        
        # Resolve service - dependencies should be injected
        service = self.container.resolve("service_with_deps")
        assert hasattr(service, 'dep1')
        assert hasattr(service, 'dep2')


class TestServiceRegistry:
    """Test service registry integration."""
    
    def setup_method(self):
        self.config = ServiceConfiguration(
            log_level="DEBUG",
            config_path=None,
            src_dir=Path("src"),
            icon_path=Path("icon.ico")
        )
        self.registry = ServiceRegistry(self.config)
    
    def test_service_registration(self):
        """Test complete service registration."""
        self.registry.register_application_services()
        
        # Test that core services are registered
        container = self.registry.container
        
        # These should not raise KeyError
        platform_detector = container.resolve("platform_detector")
        executable_finder = container.resolve("executable_finder")
        process_manager = container.resolve("process_manager")
        
        assert platform_detector is not None
        assert executable_finder is not None
        assert process_manager is not None
    
    @patch('enhanced_application.EnhancedCastingApplication')
    def test_application_creation(self, mock_app_class):
        """Test application creation through registry."""
        mock_app = Mock()
        mock_app_class.return_value = mock_app
        
        self.registry.register_application_services()
        app = self.registry.create_application()
        
        assert app is mock_app
        mock_app_class.assert_called_once()


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
