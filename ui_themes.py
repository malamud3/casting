"""UI Theme implementations for different platforms."""

import tkinter as tk
from typing import Dict, Tuple
from interfaces import IUITheme


class BaseUITheme(IUITheme):
    """Base UI theme with common styling."""
    
    def get_base_button_style(self) -> Dict:
        """Get base button styling common to all platforms."""
        return {
            'relief': 'flat',
            'borderwidth': 1,
            'pady': 8,
            'padx': 20
        }
    
    def apply_window_styling(self, window: tk.Tk) -> None:
        """Default window styling - can be overridden by platform themes."""
        pass


class MacOSUITheme(BaseUITheme):
    """macOS-specific UI theme."""
    
    def get_system_font(self) -> Tuple[str, int]:
        """Get macOS system font."""
        return ('SF Pro Display', 13)
    
    def get_primary_button_style(self) -> Dict:
        """Get macOS primary button styling."""
        style = self.get_base_button_style()
        style.update({
            'bg': '#007AFF',
            'fg': 'white',
            'activebackground': '#0056CC',
            'activeforeground': 'white',
            'font': self.get_system_font() + ('normal',),
            'cursor': 'pointinghand'
        })
        return style
    
    def get_secondary_button_style(self) -> Dict:
        """Get macOS secondary button styling."""
        style = self.get_primary_button_style()
        style.update({
            'bg': '#8E8E93',
            'activebackground': '#6D6D70'
        })
        return style
    
    def apply_window_styling(self, window: tk.Tk) -> None:
        """Apply macOS-specific window styling."""
        try:
            # Enable native macOS appearance
            window.tk.call('tk', 'scaling', 1.0)
            
            # Configure for macOS dark/light mode support
            window.tk.call("source", "/System/Library/Tcl/pTk/AppKit.tcl")
            window.tk.call("::tk::unsupported::MacWindowStyle", "style", window._w, 
                          "document", "closeBox collapseBox resizable")
            
            # Set native macOS window behavior
            window.tk.call('::tk::unsupported::MacWindowStyle', 'style', window._w, 'document')
            
        except Exception:
            # Fallback to base styling if native calls fail
            super().apply_window_styling(window)


class WindowsUITheme(BaseUITheme):
    """Windows-specific UI theme."""
    
    def get_system_font(self) -> Tuple[str, int]:
        """Get Windows system font."""
        return ('Segoe UI', 10)
    
    def get_primary_button_style(self) -> Dict:
        """Get Windows primary button styling."""
        style = self.get_base_button_style()
        style.update({
            'bg': '#0078D4',
            'fg': 'white',
            'activebackground': '#106EBE',
            'activeforeground': 'white',
            'font': self.get_system_font() + ('normal',)
        })
        return style
    
    def get_secondary_button_style(self) -> Dict:
        """Get Windows secondary button styling."""
        style = self.get_primary_button_style()
        style.update({
            'bg': '#5A5A5A',
            'activebackground': '#4A4A4A'
        })
        return style


class LinuxUITheme(BaseUITheme):
    """Linux-specific UI theme."""
    
    def get_system_font(self) -> Tuple[str, int]:
        """Get Linux system font."""
        return ('Liberation Sans', 10)
    
    def get_primary_button_style(self) -> Dict:
        """Get Linux primary button styling."""
        style = self.get_base_button_style()
        style.update({
            'bg': '#4285F4',
            'fg': 'white',
            'activebackground': '#3367D6',
            'activeforeground': 'white',
            'font': self.get_system_font() + ('normal',)
        })
        return style
    
    def get_secondary_button_style(self) -> Dict:
        """Get Linux secondary button styling."""
        style = self.get_primary_button_style()
        style.update({
            'bg': '#6c757d',
            'activebackground': '#545b62'
        })
        return style
