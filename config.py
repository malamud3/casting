"""Configuration management for the casting application."""

import json
import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ScrcpyConfig:
    """Configuration for scrcpy parameters."""
    render_driver: str = "opengl"
    crop: str = "1600:900:2017:510"
    bitrate: str = "4M"
    max_size: int = 1024
    video_codec: str = "h264"
    video_encoder: str = "OMX.qcom.video.encoder.avc"
    no_audio: bool = True
    no_control: bool = True


@dataclass
class AppConfig:
    """Main application configuration."""
    refresh_interval_ms: int = 2000
    adb_timeout_ms: int = 4000
    wireless_port: str = "5555"
    
    # UI Colors
    colors: Dict[str, str] = None
    
    # scrcpy configuration
    scrcpy: ScrcpyConfig = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                "wifi": "green",
                "device": "green", 
                "unauthorized": "yellow",
                "offline": "red",
                "": "red",
            }
        
        if self.scrcpy is None:
            self.scrcpy = ScrcpyConfig()


def load_config(config_path: str = None) -> AppConfig:
    """Load configuration from file or return defaults."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Handle nested scrcpy config
                scrcpy_data = data.pop('scrcpy', {})
                scrcpy_config = ScrcpyConfig(**scrcpy_data)
                
                return AppConfig(scrcpy=scrcpy_config, **data)
        except (json.JSONDecodeError, TypeError) as e:
            # Fall back to defaults if config is invalid
            print(f"Warning: Invalid config file, using defaults: {e}")
    
    return AppConfig()


def save_config(config: AppConfig, config_path: str):
    """Save configuration to file."""
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            # Convert dataclass to dict for JSON serialization
            config_dict = {
                'refresh_interval_ms': config.refresh_interval_ms,
                'adb_timeout_ms': config.adb_timeout_ms,
                'wireless_port': config.wireless_port,
                'colors': config.colors,
                'scrcpy': {
                    'render_driver': config.scrcpy.render_driver,
                    'crop': config.scrcpy.crop,
                    'bitrate': config.scrcpy.bitrate,
                    'max_size': config.scrcpy.max_size,
                    'video_codec': config.scrcpy.video_codec,
                    'video_encoder': config.scrcpy.video_encoder,
                    'no_audio': config.scrcpy.no_audio,
                    'no_control': config.scrcpy.no_control,
                }
            }
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Could not save config: {e}")
