"""Enhanced main application with professional architecture."""

import asyncio
import logging
from typing import Optional
from dataclasses import dataclass

from enhanced_config import ConfigManager, AppConfigModel
from error_handling import ErrorHandler, CastingException
from adb_manager import ADBManager
from cast_manager import CastManager
from async_operations import AsyncDeviceManager
from models import AppState, QuestDevice, Transport, DeviceState
from gui import CastingGUI
from utils import resource_path


@dataclass
class ApplicationMetrics:
    """Application performance and usage metrics."""
    startup_time: float = 0.0
    device_detection_count: int = 0
    successful_casts: int = 0
    failed_casts: int = 0
    wireless_connections: int = 0


class EnhancedCastingApplication:
    """
    Enhanced casting application with professional architecture.
    
    Features:
    - Dependency injection
    - Async operations
    - Structured error handling
    - Performance metrics
    - Configuration hot-reloading
    """
    
    def __init__(
        self,
        config_manager: ConfigManager,
        error_handler: ErrorHandler,
        adb_manager: ADBManager,
        cast_manager: CastManager,
        async_device_manager: AsyncDeviceManager,
        platform_service,
        icon_path: str
    ):
        # Injected dependencies
        self.config_manager = config_manager
        self.error_handler = error_handler
        self.adb_manager = adb_manager
        self.cast_manager = cast_manager
        self.async_device_manager = async_device_manager
        self.platform_service = platform_service
        self.icon_path = icon_path
        
        # Application state
        self.app_state = AppState()
        self.metrics = ApplicationMetrics()
        self.logger = logging.getLogger(__name__)
        
        # GUI will be initialized during startup
        self.gui: Optional[CastingGUI] = None
        
        # Async event loop
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        
        self.logger.info("Enhanced application initialized")
    
    async def initialize_async(self):
        """Initialize async components."""
        self.loop = asyncio.get_event_loop()
        
        # Setup configuration change watching
        self.config_manager.watch_changes(self._on_config_changed)
        
        # Load current configuration
        config = self.config_manager.config
        
        # Initialize GUI with enhanced error handling
        try:
            self.gui = CastingGUI(config, self.icon_path)
            
            # Connect enhanced callbacks
            self.gui.on_cast_requested = self._handle_cast_request_async
            self.gui.on_wireless_toggle = self._handle_wireless_toggle_async
            
            self.logger.info("GUI initialized successfully")
            
        except Exception as e:
            error = self.error_handler.handle_exception(e, "GUI initialization")
            raise CastingException(error, e)
    
    def _on_config_changed(self, new_config: AppConfigModel):
        """Handle configuration changes."""
        self.logger.info("Configuration changed, updating application")
        
        # Update logging level
        logging.getLogger().setLevel(getattr(logging, new_config.log_level))
        
        # Update GUI theme if available
        if self.gui:
            try:
                self.gui.update_theme(new_config.ui_theme)
            except Exception as e:
                self.logger.warning(f"Failed to update GUI theme: {e}")
    
    async def _handle_cast_request_async(self):
        """Handle cast request with async operations and progress feedback."""
        try:
            current_device = self.app_state.current_device
            if not current_device:
                error = self.error_handler.get_error("DEVICE_NOT_FOUND")
                self.gui.show_warning(
                    error.user_message_hebrew or error.message,
                    error.suggested_action or "Connect device and try again"
                )
                return
            
            # Show progress dialog
            progress_dialog = self.gui.show_progress_dialog("Starting cast...", cancelable=True)
            
            def update_progress(progress: float, message: str = ""):
                if progress_dialog:
                    progress_dialog.update(progress, message)
            
            try:
                # Check for Wi-Fi connection preference
                wifi_serial = self.adb_manager.find_wifi_serial()
                
                # Start casting asynchronously
                success = await self.async_device_manager.start_casting_async(
                    current_device,
                    wifi_serial,
                    progress_callback=update_progress
                )
                
                if success:
                    self.metrics.successful_casts += 1
                    self.logger.info("Casting started successfully")
                else:
                    self.metrics.failed_casts += 1
                    error = self.error_handler.get_error("CAST_START_FAILED")
                    self.gui.show_error(
                        error.user_message_hebrew or error.message,
                        error.suggested_action or "Check device connection"
                    )
                
            finally:
                if progress_dialog:
                    progress_dialog.close()
                
        except CastingException as e:
            self.metrics.failed_casts += 1
            self.gui.show_error(
                e.error.user_message_hebrew or e.error.message,
                e.error.suggested_action or "Please try again"
            )
        except Exception as e:
            self.metrics.failed_casts += 1
            error = self.error_handler.handle_exception(e, "Cast request")
            self.gui.show_error(
                error.user_message_hebrew or error.message,
                error.suggested_action or "Unexpected error occurred"
            )
    
    async def _handle_wireless_toggle_async(self):
        """Handle wireless toggle with async operations."""
        try:
            current_device = self.app_state.current_device
            if not current_device:
                return
            
            if current_device.is_wifi:
                # Disconnect from wireless
                await self._disconnect_wireless_async()
            else:
                # Connect to wireless
                await self._connect_wireless_async()
                
        except CastingException as e:
            self.gui.show_error(
                e.error.user_message_hebrew or e.error.message,
                e.error.suggested_action or "Please try again"
            )
        except Exception as e:
            error = self.error_handler.handle_exception(e, "Wireless toggle")
            self.gui.show_error(
                error.user_message_hebrew or error.message,
                error.suggested_action or "Unexpected error occurred"
            )
    
    async def _connect_wireless_async(self):
        """Connect to wireless ADB with progress feedback."""
        # Show progress dialog
        progress_dialog = self.gui.show_progress_dialog("Connecting wirelessly...", cancelable=True)
        
        def update_progress(progress: float, message: str = ""):
            if progress_dialog:
                progress_dialog.update(progress, message)
        
        try:
            update_progress(0.1, "Detecting device...")
            
            # Detect device
            device = await self.async_device_manager.detect_device_async()
            
            if not device.is_authorized:
                error = self.error_handler.get_error("DEVICE_UNAUTHORIZED")
                self.gui.show_warning(
                    error.user_message_hebrew or error.message,
                    error.suggested_action or "Please authorize on device"
                )
                return
            
            update_progress(0.3, "Getting device IP...")
            
            # Get Wi-Fi IP
            ip = self.adb_manager.get_wifi_ip()
            if not ip:
                error = self.error_handler.get_error("WIRELESS_CONNECTION_FAILED", "Could not get device IP")
                raise CastingException(error)
            
            update_progress(0.5, "Enabling wireless mode...")
            
            # Connect wirelessly
            success, message = await self.async_device_manager.connect_wireless_async(
                ip,
                progress_callback=lambda p, m: update_progress(0.5 + p * 0.5, m)
            )
            
            if success:
                self.metrics.wireless_connections += 1
                wifi_address = f"{ip}:{self.config_manager.config.wireless_port}"
                self.app_state.last_wifi_serial = wifi_address
                
                self.gui.show_info("Wi-Fi Connected", f"{message}\nYou can now disconnect the USB cable")
                await self._refresh_device_status_async()
            else:
                error = self.error_handler.get_error("WIRELESS_CONNECTION_FAILED", message)
                raise CastingException(error)
                
        finally:
            if progress_dialog:
                progress_dialog.close()
    
    async def _disconnect_wireless_async(self):
        """Disconnect from wireless ADB."""
        current_device = self.app_state.current_device
        if current_device and current_device.is_wifi:
            # Run in thread pool to avoid blocking
            await self.loop.run_in_executor(
                None,
                self.adb_manager.disconnect_wireless,
                current_device.serial
            )
        
        self.app_state.last_wifi_serial = None
        await self._refresh_device_status_async()
    
    async def _refresh_device_status_async(self):
        """Refresh device status asynchronously."""
        try:
            device = await self.async_device_manager.detect_device_async()
            self.app_state.update_device(device)
            self.gui.update_device_status(device)
            self.metrics.device_detection_count += 1
            
        except Exception as e:
            self.logger.error(f"Failed to refresh device status: {e}")
            # Create unknown device state for GUI
            unknown_device = QuestDevice(Transport.UNKNOWN, DeviceState.UNKNOWN, None)
            self.gui.update_device_status(unknown_device)
    
    def _schedule_refresh(self):
        """Schedule periodic device status refresh."""
        async def refresh_loop():
            while True:
                await self._refresh_device_status_async()
                config = self.config_manager.config
                await asyncio.sleep(config.refresh_interval_ms / 1000.0)
        
        asyncio.create_task(refresh_loop())
    
    async def start_async(self):
        """Start the application asynchronously."""
        import time
        start_time = time.time()
        
        try:
            # Initialize async components
            await self.initialize_async()
            
            # Initial device status check
            await self._refresh_device_status_async()
            
            # Start auto-refresh
            self._schedule_refresh()
            
            # Record startup time
            self.metrics.startup_time = time.time() - start_time
            self.logger.info(f"Application started in {self.metrics.startup_time:.2f}s")
            
            # Run GUI (this will block until GUI is closed)
            if self.gui:
                self.gui.run()
            
        except Exception as e:
            error = self.error_handler.handle_exception(e, "Application startup")
            self.logger.critical(f"Application failed to start: {error.message}")
            raise
    
    def run(self):
        """Run the application."""
        try:
            # Use asyncio.run for Python 3.7+
            asyncio.run(self.start_async())
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.critical(f"Application crashed: {e}")
            raise
        finally:
            self.logger.info("Application shutting down")
            self._log_metrics()
    
    def _log_metrics(self):
        """Log application metrics."""
        self.logger.info(f"Application Metrics:")
        self.logger.info(f"  Startup time: {self.metrics.startup_time:.2f}s")
        self.logger.info(f"  Device detections: {self.metrics.device_detection_count}")
        self.logger.info(f"  Successful casts: {self.metrics.successful_casts}")
        self.logger.info(f"  Failed casts: {self.metrics.failed_casts}")
        self.logger.info(f"  Wireless connections: {self.metrics.wireless_connections}")
