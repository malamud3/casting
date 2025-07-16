"""Async operations for non-blocking device management."""

import asyncio
import logging
from typing import Optional, Callable, Any
from dataclasses import dataclass
from models import QuestDevice
from error_handling import ErrorHandler, DeviceConnectionError


@dataclass
class AsyncOperation:
    """Represents an async operation with progress tracking."""
    name: str
    progress: float = 0.0
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None


class AsyncDeviceManager:
    """Async device operations manager."""
    
    def __init__(self, adb_manager, error_handler: ErrorHandler):
        self.adb_manager = adb_manager
        self.error_handler = error_handler
        self.logger = logging.getLogger(__name__)
        self._current_operations = {}
    
    async def detect_device_async(self, 
                                  progress_callback: Optional[Callable[[float], None]] = None) -> QuestDevice:
        """Asynchronously detect Quest device."""
        operation = AsyncOperation("device_detection")
        
        try:
            if progress_callback:
                progress_callback(0.1)
            
            # Run detection in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            device = await loop.run_in_executor(
                None, 
                self.adb_manager.detect_quest_device
            )
            
            if progress_callback:
                progress_callback(1.0)
                
            operation.status = "completed"
            operation.result = device
            return device
            
        except Exception as e:
            error = self.error_handler.handle_exception(e, "Device detection")
            operation.status = "failed"
            operation.error = error.message
            raise DeviceConnectionError(error, e)
    
    async def connect_wireless_async(self, 
                                   ip: str,
                                   progress_callback: Optional[Callable[[float, str], None]] = None) -> tuple[bool, str]:
        """Asynchronously connect to wireless ADB."""
        operation = AsyncOperation("wireless_connection")
        
        try:
            if progress_callback:
                progress_callback(0.1, "Enabling wireless mode...")
            
            # Enable wireless in thread pool
            loop = asyncio.get_event_loop()
            enabled = await loop.run_in_executor(
                None,
                self.adb_manager.enable_wireless_adb
            )
            
            if not enabled:
                raise Exception("Failed to enable wireless ADB mode")
            
            if progress_callback:
                progress_callback(0.5, "Connecting to device...")
            
            # Small delay for device to start listening
            await asyncio.sleep(1)
            
            # Connect to device
            success, message = await loop.run_in_executor(
                None,
                self.adb_manager.connect_wireless,
                ip
            )
            
            if progress_callback:
                progress_callback(1.0, "Connected!" if success else "Failed")
            
            operation.status = "completed"
            operation.result = (success, message)
            return success, message
            
        except Exception as e:
            error = self.error_handler.handle_exception(e, "Wireless connection")
            operation.status = "failed"
            operation.error = error.message
            if progress_callback:
                progress_callback(1.0, f"Error: {error.message}")
            raise DeviceConnectionError(error, e)
    
    async def start_casting_async(self,
                                device: QuestDevice,
                                wifi_serial: Optional[str] = None,
                                progress_callback: Optional[Callable[[float, str], None]] = None) -> bool:
        """Asynchronously start casting process."""
        operation = AsyncOperation("casting_start")
        
        try:
            if progress_callback:
                progress_callback(0.2, "Preparing casting...")
            
            # Import cast_manager here to avoid circular imports
            from cast_manager import CastManager
            cast_manager = CastManager(self.adb_manager.config, self.adb_manager.src_dir)
            
            if progress_callback:
                progress_callback(0.5, "Starting scrcpy...")
            
            # Start casting in thread pool
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                None,
                cast_manager.start_casting,
                device,
                wifi_serial
            )
            
            if progress_callback:
                progress_callback(1.0, "Casting started!" if success else "Failed to start")
            
            operation.status = "completed" 
            operation.result = success
            return success
            
        except Exception as e:
            error = self.error_handler.handle_exception(e, "Casting start")
            operation.status = "failed"
            operation.error = error.message
            if progress_callback:
                progress_callback(1.0, f"Error: {error.message}")
            return False
