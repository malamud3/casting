"""Enhanced configuration management with validation and type safety."""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from pydantic import BaseModel, validator, Field


class ScrcpyConfigModel(BaseModel):
    """Validated scrcpy configuration using Pydantic."""
    render_driver: str = Field(default="opengl", regex="^(opengl|software|direct3d)$")
    crop: str = Field(default="1600:900:2017:510", regex=r"^\d+:\d+:\d+:\d+$")
    bitrate: str = Field(default="4M", regex=r"^\d+[KM]?$")
    max_size: int = Field(default=1024, ge=240, le=2160)
    video_codec: str = Field(default="h264", regex="^(h264|h265|av1)$")
    video_encoder: str = Field(default="OMX.qcom.video.encoder.avc")
    no_audio: bool = True
    no_control: bool = True
    
    @validator('crop')
    def validate_crop_format(cls, v):
        """Validate crop format is valid."""
        parts = v.split(':')
        if len(parts) != 4:
            raise ValueError('Crop must be in format width:height:x:y')
        try:
            [int(p) for p in parts]
        except ValueError:
            raise ValueError('Crop values must be integers')
        return v


class UIThemeModel(BaseModel):
    """UI theme configuration with validation."""
    primary_color: str = Field(default="#007AFF", regex=r"^#[0-9A-Fa-f]{6}$")
    secondary_color: str = Field(default="#8E8E93", regex=r"^#[0-9A-Fa-f]{6}$")
    background_color: str = Field(default="#FFFFFF", regex=r"^#[0-9A-Fa-f]{6}$")
    text_color: str = Field(default="#1C1C1E", regex=r"^#[0-9A-Fa-f]{6}$")
    font_family: str = "SF Pro Display"
    font_size: int = Field(default=13, ge=8, le=24)


class AppConfigModel(BaseModel):
    """Main application configuration with validation."""
    refresh_interval_ms: int = Field(default=2000, ge=500, le=10000)
    adb_timeout_ms: int = Field(default=4000, ge=1000, le=30000)
    wireless_port: str = Field(default="5555", regex=r"^\d{4,5}$")
    log_level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    # Device status colors
    status_colors: Dict[str, str] = Field(default_factory=lambda: {
        "wifi": "#30D158",
        "device": "#30D158", 
        "unauthorized": "#FF9F0A",
        "offline": "#FF453A",
        "": "#FF453A",
    })
    
    # UI theme
    ui_theme: UIThemeModel = Field(default_factory=UIThemeModel)
    
    # scrcpy configuration
    scrcpy: ScrcpyConfigModel = Field(default_factory=ScrcpyConfigModel)
    
    # Advanced settings
    enable_debug_features: bool = False
    auto_connect_wireless: bool = True
    remember_last_device: bool = True
    
    @validator('status_colors')
    def validate_colors(cls, v):
        """Validate all color values are valid hex colors."""
        for key, color in v.items():
            if not color.startswith('#') or len(color) != 7:
                raise ValueError(f'Invalid color format for {key}: {color}')
        return v


class ConfigManager:
    """Enhanced configuration manager with validation and hot-reloading."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or "config.json")
        self.logger = logging.getLogger(__name__)
        self._config: Optional[AppConfigModel] = None
        self._watchers: List[callable] = []
    
    def load_config(self) -> AppConfigModel:
        """Load and validate configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Validate using Pydantic
                self._config = AppConfigModel(**config_data)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Create default configuration
                self._config = AppConfigModel()
                self.save_config()
                self.logger.info("Created default configuration")
                
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.logger.info("Using default configuration")
            self._config = AppConfigModel()
        
        return self._config
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            if not self._config:
                return False
            
            # Create directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dict and save
            config_dict = self._config.dict()
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def update_config(self, **kwargs) -> bool:
        """Update configuration with new values."""
        try:
            if not self._config:
                self.load_config()
            
            # Create updated config
            current_dict = self._config.dict()
            current_dict.update(kwargs)
            
            # Validate new config
            new_config = AppConfigModel(**current_dict)
            self._config = new_config
            
            # Save and notify watchers
            saved = self.save_config()
            if saved:
                self._notify_watchers()
            
            return saved
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False
    
    def watch_changes(self, callback: callable):
        """Register callback for configuration changes."""
        self._watchers.append(callback)
    
    def _notify_watchers(self):
        """Notify all watchers of configuration changes."""
        for callback in self._watchers:
            try:
                callback(self._config)
            except Exception as e:
                self.logger.error(f"Error in config watcher: {e}")
    
    @property
    def config(self) -> AppConfigModel:
        """Get current configuration."""
        if not self._config:
            self.load_config()
        return self._config


# Global config manager instance
config_manager = ConfigManager()


def load_config(config_path: Optional[str] = None) -> AppConfigModel:
    """Load configuration - backward compatibility function."""
    if config_path:
        manager = ConfigManager(config_path)
        return manager.load_config()
    return config_manager.load_config()
