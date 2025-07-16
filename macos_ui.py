"""DEPRECATED: Legacy macOS UI styling - Use ui_themes.py and service_factory.py instead.

This file is kept for backward compatibility.
New code should use the modular UI theme services.
"""

import warnings
import tkinter as tk
from service_factory import ServiceFactory

# Issue deprecation warning
warnings.warn(
    "macos_ui.py is deprecated. Use ServiceFactory.create_platform_service() for UI theming.",
    DeprecationWarning,
    stacklevel=2
)

# Create service for backward compatibility
_platform_service = ServiceFactory.create_platform_service()


class MacOSStyle:
    """DEPRECATED: Legacy macOS styling class."""
    
    @staticmethod
    def apply_macos_styling(window: tk.Tk):
        """DEPRECATED: Apply macOS-specific styling to the main window."""
        warnings.warn(
            "MacOSStyle.apply_macos_styling is deprecated. Use platform_service.apply_window_styling() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        _platform_service.apply_window_styling(window)
    
    @staticmethod
    def get_system_font() -> tuple:
        """DEPRECATED: Get the appropriate system font for the platform."""
        warnings.warn(
            "MacOSStyle.get_system_font is deprecated. Use platform_service.get_system_font() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return _platform_service.get_system_font()
    
    @staticmethod
    def get_button_style() -> dict:
        """DEPRECATED: Get platform-appropriate button styling."""
        warnings.warn(
            "MacOSStyle.get_button_style is deprecated. Use platform_service.get_primary_button_style() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return _platform_service.get_primary_button_style()
    
    @staticmethod
    def get_secondary_button_style() -> dict:
        """DEPRECATED: Get styling for secondary buttons."""
        warnings.warn(
            "MacOSStyle.get_secondary_button_style is deprecated. Use platform_service.get_secondary_button_style() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return _platform_service.get_secondary_button_style()
    
    @staticmethod
    def get_status_colors() -> dict:
        """DEPRECATED: Get platform-appropriate status indicator colors."""
        warnings.warn(
            "MacOSStyle.get_status_colors is deprecated. Use new UI theme services instead.",
            DeprecationWarning,
            stacklevel=2
        )
        # Return compatible colors for backward compatibility
        if _platform_service.is_macos():
            return {
                "wifi": "#30D158",      # System Green
                "device": "#30D158",    # System Green  
                "unauthorized": "#FF9F0A",  # System Orange
                "offline": "#FF453A",   # System Red
                "": "#FF453A",
            }
        else:
            return {
                "wifi": "green",
                "device": "green", 
                "unauthorized": "orange",
                "offline": "red",
                "": "red",
            }


# DEPRECATED: Keep minimal UI components for backward compatibility
# These should be migrated to use the new modular services from ui_themes.py

class ModernStatusIndicator:
    """DEPRECATED: Use new UI components. Minimal backward compatibility wrapper."""
    
    def __init__(self, parent, initial_status="Ready"):
        self.frame = tk.Frame(parent, bg="white")
        font = _platform_service.get_system_font()
        self.label = tk.Label(self.frame, text=initial_status, font=font, bg="white", fg="#1c1c1e")
        self.label.pack()
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def update_status(self, status: str, color: str = "#34C759"):
        self.label.config(text=status)


class ModernButton:
    """DEPRECATED: Use new UI components. Minimal backward compatibility wrapper."""
    
    def __init__(self, parent, text: str, command=None, style_type: str = "primary", state: str = "normal"):
        if style_type == "secondary":
            style = _platform_service.get_secondary_button_style()
        else:
            style = _platform_service.get_primary_button_style()
        
        self.button = tk.Button(parent, text=text, command=command, state=state, **style)
    
    def pack(self, **kwargs):
        self.button.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.button.grid(**kwargs)
    
    def config(self, **kwargs):
        self.button.config(**kwargs)


class ModernLabel:
    """DEPRECATED: Use new UI components. Minimal backward compatibility wrapper."""
    
    def __init__(self, parent, textvariable):
        font = _platform_service.get_system_font()
        self.label = tk.Label(parent, textvariable=textvariable, font=font, bg=parent.cget('bg'))
        
    def pack(self, **kwargs):
        self.label.pack(**kwargs)


class EnhancedRTLDialog:
    """DEPRECATED: Use new UI components. Minimal backward compatibility wrapper."""
    
    @staticmethod
    def show_info(parent, title: str, message: str, ok_text: str = "אישור"):
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(parent)
        
        # Apply platform styling
        _platform_service.apply_window_styling(dialog)
        
        # Basic layout
        dialog.geometry("360x180")
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 180
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 90
        dialog.geometry(f"360x180+{x}+{y}")
        
        # Content
        content_frame = tk.Frame(dialog)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        font = _platform_service.get_system_font()
        message_label = tk.Label(content_frame, text=message, justify="right", 
                               anchor="e", wraplength=320, font=font)
        message_label.pack(pady=(0, 20), fill='both', expand=True)
        
        button_style = _platform_service.get_primary_button_style()
        ok_button = tk.Button(content_frame, text=ok_text, command=dialog.destroy, **button_style)
        ok_button.pack(pady=(10, 0))
        
        dialog.focus_set()
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.wait_window()


# Export aliases for backward compatibility
RTLDialog = EnhancedRTLDialog
