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
            style.update({
                'bg': '#757575',
                'activebackground': '#616161'
            })
        
        return style
    
    @staticmethod
    def get_status_colors() -> dict:
        """Get platform-appropriate status indicator colors."""
        system = platform.system()
        
        if system == 'Darwin':  # macOS - use system colors
            return {
                "wifi": "#30D158",      # System Green
                "device": "#30D158",    # System Green
                "unauthorized": "#FF9F0A",  # System Orange
                "offline": "#FF453A",   # System Red
                "": "#FF453A",
            }
        else:
            # Keep original colors for Windows/Linux
            return {
                "wifi": "green",
                "device": "green",
                "unauthorized": "orange",
                "offline": "red",
                "": "red",
            }


class ModernStatusIndicator:
    """Enhanced status indicator with modern styling."""
    
    def __init__(self, parent: tk.Widget, colors: dict):
        self.colors = colors
        self.system = platform.system()
        
        # Create frame for better layout
        self.frame = tk.Frame(parent, bg=parent.cget('bg'))
        self.frame.pack(pady=(20, 10))
        
        # Create canvas with larger size for better visibility
        canvas_size = 40 if self.system == 'Darwin' else 30
        self.canvas = tk.Canvas(
            self.frame, 
            width=canvas_size, 
            height=canvas_size, 
            highlightthickness=0,
            bg=parent.cget('bg')
        )
        self.canvas.pack()
        
        # Create the status circle with shadow effect on macOS
        if self.system == 'Darwin':
            # Shadow circle for depth
            self.shadow = self.canvas.create_oval(2, 2, 38, 38, fill="#E0E0E0", outline="")
            # Main circle
            self.circle = self.canvas.create_oval(0, 0, 36, 36, fill="#FF453A", outline="white", width=2)
        else:
            # Standard circle for other platforms
            margin = (canvas_size - 20) // 2
            self.circle = self.canvas.create_oval(
                margin, margin, 
                canvas_size - margin, canvas_size - margin, 
                fill="red", outline=""
            )
    
    def update_status(self, device):
        """Update the status indicator based on device state."""
        color = self.colors.get(device.status_key, self.colors.get("", "red"))
        self.canvas.itemconfig(self.circle, fill=color)
        
        # Add pulse animation on macOS for active states
        if self.system == 'Darwin' and device.is_connected:
            self._pulse_animation()
    
    def _pulse_animation(self):
        """Subtle pulse animation for connected devices on macOS."""
        # This could be enhanced with actual animation
        pass


class ModernLabel:
    """Enhanced label with better typography."""
    
    def __init__(self, parent: tk.Widget, textvariable: tk.StringVar):
        font = MacOSStyle.get_system_font()
        
        self.label = tk.Label(
            parent,
            textvariable=textvariable,
            font=font,
            fg='#1C1C1E' if platform.system() == 'Darwin' else 'black',
            bg=parent.cget('bg')
        )
        self.label.pack(pady=(0, 20))


class ModernButton:
    """Enhanced button with platform-native styling."""
    
    def __init__(self, parent: tk.Widget, text: str, command: callable, 
                 style_type: str = 'primary', state: str = 'normal'):
        
        if style_type == 'primary':
            style = MacOSStyle.get_button_style()
        else:
            style = MacOSStyle.get_secondary_button_style()
        
        self.button = tk.Button(
            parent,
            text=text,
            command=command,
            state=state,
            **style
        )
        
        # Add hover effects
        self._setup_hover_effects()
    
    def _setup_hover_effects(self):
        """Add hover effects for better UX."""
        original_bg = self.button.cget('bg')
        hover_bg = self.button.cget('activebackground')
        
        def on_enter(event):
            self.button.config(bg=hover_bg)
        
        def on_leave(event):
            self.button.config(bg=original_bg)
        
        self.button.bind("<Enter>", on_enter)
        self.button.bind("<Leave>", on_leave)
    
    def pack(self, **kwargs):
        """Pack the button with default spacing."""
        default_kwargs = {'pady': 8, 'padx': 20, 'fill': 'x'}
        default_kwargs.update(kwargs)
        self.button.pack(**default_kwargs)
    
    def config(self, **kwargs):
        """Configure the button."""
        self.button.config(**kwargs)


class EnhancedRTLDialog:
    """Improved RTL dialog with better macOS integration."""
    
    @staticmethod
    def show_info(parent: tk.Tk, title: str, message: str, ok_text: str = "אישור"):
        """Show an enhanced RTL information dialog."""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(parent)
        
        # Apply macOS styling if available
        MacOSStyle.apply_macos_styling(dialog)
        
        # Better sizing and positioning
        dialog.geometry("360x180")
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 180
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 90
        dialog.geometry(f"360x180+{x}+{y}")
        
        # Content frame with padding
        content_frame = tk.Frame(dialog, bg='white' if platform.system() == 'Darwin' else dialog.cget('bg'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Message label with better typography
        font = MacOSStyle.get_system_font()
        message_label = tk.Label(
            content_frame,
            text=message,
            justify="right",
            anchor="e",
            wraplength=320,
            font=font,
            fg='#1C1C1E' if platform.system() == 'Darwin' else 'black',
            bg=content_frame.cget('bg')
        )
        message_label.pack(pady=(0, 20), fill='both', expand=True)
        
        # Enhanced OK button
        button_style = MacOSStyle.get_button_style()
        ok_button = tk.Button(
            content_frame,
            text=ok_text,
            command=dialog.destroy,
            **button_style
        )
        ok_button.pack(pady=(10, 0))
        
        # Center focus and handle escape key
        dialog.focus_set()
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.bind('<Return>', lambda e: dialog.destroy())
        
        dialog.wait_window()


# Export the enhanced dialog as the default
RTLDialog = EnhancedRTLDialog
