"""Device state management and data structures."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Transport(Enum):
    """Device connection transport types."""
    WIFI = "wifi"
    USB = "usb"
    UNKNOWN = "unknown"


class DeviceState(Enum):
    """Device connection states."""
    DEVICE = "device"
    UNAUTHORIZED = "unauthorized" 
    OFFLINE = "offline"
    UNKNOWN = ""


@dataclass
class QuestDevice:
    """Represents a Meta Quest device and its connection state."""
    transport: Transport
    state: DeviceState
    serial: Optional[str] = None
    
    @property
    def is_wifi(self) -> bool:
        """Check if device is connected via Wi-Fi."""
        return self.transport == Transport.WIFI
    
    @property
    def is_usb(self) -> bool:
        """Check if device is connected via USB."""
        return self.transport == Transport.USB
    
    @property
    def is_authorized(self) -> bool:
        """Check if device is authorized (ready for use)."""
        return self.state == DeviceState.DEVICE
    
    @property
    def is_connected(self) -> bool:
        """Check if device is connected (any state except unknown/offline)."""
        return self.state not in (DeviceState.UNKNOWN, DeviceState.OFFLINE)
    
    @property
    def status_key(self) -> str:
        """Get the key for status color lookup."""
        if self.transport == Transport.WIFI:
            return "wifi"
        return self.state.value
    
    def __bool__(self) -> bool:
        """Device is truthy if it's connected and has a serial."""
        return self.is_connected and self.serial is not None


@dataclass 
class AppState:
    """Global application state."""
    current_device: Optional[QuestDevice] = None
    last_wifi_serial: Optional[str] = None
    
    def update_device(self, device: QuestDevice):
        """Update the current device state."""
        self.current_device = device
        
        # Remember last Wi-Fi serial for reconnection
        if device.is_wifi and device.serial:
            self.last_wifi_serial = device.serial
