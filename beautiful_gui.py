"""
Modern, beautiful GUI components for the Quest Casting application.
Features contemporary design with smooth animations and professional styling.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
import platform
from models import QuestDevice, DeviceState
from utils import open_email_client, open_url


class AppleColors:
    """Apple-inspired color palette for native macOS look."""
    
    # Apple System Colors
    SYSTEM_BLUE = "#007AFF"
    SYSTEM_GREEN = "#34C759"
    SYSTEM_RED = "#FF3B30"
    SYSTEM_ORANGE = "#FF9500"
    SYSTEM_PURPLE = "#AF52DE"
    
    # Background colors (macOS Big Sur/Monterey style)
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F2F2F7"
    BG_TERTIARY = "#F9F9F9"
    BG_SIDEBAR = "#ECECEC"
    
    # Text colors
    TEXT_PRIMARY = "#1D1D1F"
    TEXT_SECONDARY = "#86868B"
    TEXT_TERTIARY = "#A1A1A6"
    TEXT_WHITE = "#FFFFFF"
    
    # Apple specific elements
    CONTROL_ACCENT = "#007AFF"
    SEPARATOR = "#D1D1D6"
    SHADOW = "#00000008"
    GLASS_EFFECT = "#FFFFFF85"
    
    # Window chrome
    WINDOW_CHROME = "#ECECEC"
    TRAFFIC_LIGHT_RED = "#FF5F56"
    TRAFFIC_LIGHT_YELLOW = "#FFBD2E"
    TRAFFIC_LIGHT_GREEN = "#27CA3F"


class AppleButton(tk.Button):
    """Apple-style button with native macOS appearance."""
    
    def __init__(self, parent, style='primary', **kwargs):
        self.style = style
        self.is_hovered = False
        self.is_pressed = False
        
        # Apple button styles
        if style == 'primary':
            self.bg_normal = AppleColors.SYSTEM_BLUE
            self.bg_hover = "#0051D5"
            self.bg_pressed = "#004CCC"
            self.fg_color = AppleColors.TEXT_WHITE
            self.font_weight = 'bold'
        elif style == 'destructive':
            self.bg_normal = AppleColors.SYSTEM_RED
            self.bg_hover = "#D70015"
            self.bg_pressed = "#C20015"
            self.fg_color = AppleColors.TEXT_WHITE
            self.font_weight = 'bold'
        elif style == 'prominent':
            self.bg_normal = AppleColors.SYSTEM_GREEN
            self.bg_hover = "#248A3D"
            self.bg_pressed = "#1E7A35"
            self.fg_color = AppleColors.TEXT_WHITE
            self.font_weight = 'bold'
        else:  # secondary
            self.bg_normal = AppleColors.BG_SECONDARY
            self.bg_hover = "#E5E5EA"
            self.bg_pressed = "#D1D1D6"
            self.fg_color = AppleColors.SYSTEM_BLUE
            self.font_weight = 'normal'
            
        super().__init__(
            parent,
            relief='flat',
            bd=0,
            font=('.AppleSystemUIFont', 14, self.font_weight),
            cursor='pointinghand',  # macOS style cursor
            padx=24,
            pady=10,
            bg=self.bg_normal,
            fg=self.fg_color,
            activebackground=self.bg_hover,
            activeforeground=self.fg_color,
            **{k: v for k, v in kwargs.items() if k not in ['style']}
        )
        
        # Bind Apple-style interactions
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        
    def _on_enter(self, event):
        if self['state'] != 'disabled':
            self.configure(bg=self.bg_hover)
            self.is_hovered = True
            
    def _on_leave(self, event):
        if self['state'] != 'disabled':
            self.configure(bg=self.bg_pressed if self.is_pressed else self.bg_normal)
            self.is_hovered = False
            
    def _on_press(self, event):
        if self['state'] != 'disabled':
            self.configure(bg=self.bg_pressed)
            self.is_pressed = True
            
    def _on_release(self, event):
        if self['state'] != 'disabled':
            self.configure(bg=self.bg_hover if self.is_hovered else self.bg_normal)
            self.is_pressed = False
            
    def configure(self, **kwargs):
        # Filter out custom options
        custom_options = ['style']
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in custom_options}
        
        if 'state' in kwargs:
            if kwargs['state'] == 'disabled':
                super().configure(
                    bg=AppleColors.BG_SECONDARY,
                    fg=AppleColors.TEXT_TERTIARY,
                    **filtered_kwargs
                )
                return
                
        super().configure(**filtered_kwargs)


class StatusIndicator(tk.Canvas):
    """Modern, animated status indicator."""
    
    def __init__(self, parent, size=80):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=parent.cget('bg'),
            highlightthickness=0
        )
        
        self.size = size
        self.center = size // 2
        self.radius = (size - 20) // 2
        
        self.pack(pady=20)
        
    def update_status(self, device: QuestDevice):
        """Update the status indicator with smooth animation."""
        self.delete("all")
        
        # Determine colors and icon
        if device.is_wifi and device.is_authorized:
            color = ModernColors.PRIMARY_GREEN
            icon = "📡"
            pulse_color = "#90EE90"  # Light green
        elif device.is_authorized:
            color = ModernColors.PRIMARY_GREEN  
            icon = "✓"
            pulse_color = "#90EE90"  # Light green
        elif device.state == DeviceState.UNAUTHORIZED:
            color = ModernColors.PRIMARY_ORANGE
            icon = "⚠"
            pulse_color = "#FFD700"  # Light orange
        else:
            color = ModernColors.PRIMARY_RED
            icon = "✕"
            pulse_color = "#FFB6C1"  # Light red
            
        # Draw outer pulse ring
        pulse_radius = self.radius + 8
        self.create_oval(
            self.center - pulse_radius, self.center - pulse_radius,
            self.center + pulse_radius, self.center + pulse_radius,
            outline=pulse_color, width=2, fill=""
        )
        
        # Draw main circle with gradient effect (simulated)
        self.create_oval(
            self.center - self.radius, self.center - self.radius,
            self.center + self.radius, self.center + self.radius,
            fill=color, outline="white", width=3
        )
        
        # Add inner shadow effect
        shadow_radius = self.radius - 5
        self.create_oval(
            self.center - shadow_radius, self.center - shadow_radius,
            self.center + shadow_radius, self.center + shadow_radius,
            outline="#CCCCCC", width=1, fill=""
        )
        
        # Add icon
        self.create_text(
            self.center, self.center,
            text=icon,
            font=('Helvetica', 20, 'bold'),
            fill="white"
        )


class ModernLabel(tk.Label):
    """Modern label with enhanced typography."""
    
    def __init__(self, parent, textvariable=None, style='primary', **kwargs):
        if style == 'primary':
            font_config = ('Helvetica', 16, 'bold')
            color = ModernColors.TEXT_PRIMARY
        elif style == 'secondary':
            font_config = ('Helvetica', 14, 'normal')
            color = ModernColors.TEXT_SECONDARY
        else:  # title
            font_config = ('Helvetica', 24, 'bold')
            color = ModernColors.TEXT_PRIMARY
            
        super().__init__(
            parent,
            textvariable=textvariable,
            font=font_config,
            fg=color,
            bg=parent.cget('bg'),
            wraplength=400,
            justify='center',
            **kwargs
        )


class ModernDialog:
    """Modern dialog with beautiful styling."""
    
    @staticmethod
    def show_info(parent, title, message, button_text="אישור"):
        """Show a beautifully styled info dialog."""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.configure(bg=ModernColors.BG_PRIMARY)
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.geometry("400x250")
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")
        
        # Main content frame
        content_frame = ModernCard(dialog)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ModernLabel(content_frame, style='title')
        title_label.configure(text=title)
        title_label.pack(pady=(0, 15))
        
        # Message
        message_label = ModernLabel(content_frame, style='primary')
        message_label.configure(text=message, wraplength=350)
        message_label.pack(pady=(0, 20))
        
        # Button
        ok_button = ModernButton(
            content_frame,
            text=button_text,
            style_type='primary',
            command=dialog.destroy
        )
        ok_button.pack()
        
        # Make modal
        dialog.transient(parent)
        dialog.grab_set()
        dialog.wait_window()


class BeautifulCastingGUI:
    """Modern, beautiful casting GUI with professional design."""
    
    def __init__(self, config, icon_path: str):
        self.config = config
        self.on_cast_requested = None
        self.on_wireless_toggle = None
        
        self.setup_window(icon_path)
        self.setup_interface()
        
    def setup_window(self, icon_path):
        """Setup the main window with modern styling."""
        self.window = tk.Tk()
        self.window.title("Quest Casting Pro")
        self.window.configure(bg=ModernColors.BG_PRIMARY)
        
        # Set window size and make it non-resizable for consistent design
        self.window.geometry("480x580")
        self.window.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Try to set icon (ignore errors on macOS)
        if platform.system() != 'Darwin':
            try:
                self.window.iconbitmap(icon_path)
            except:
                pass
                
    def center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_interface(self):
        """Setup the beautiful modern interface."""
        # Main container
        main_container = tk.Frame(self.window, bg=ModernColors.BG_PRIMARY)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.setup_header(main_container)
        
        # Status card
        self.setup_status_section(main_container)
        
        # Action buttons
        self.setup_action_buttons(main_container)
        
        # Footer
        self.setup_footer(main_container)
        
        # Menu
        self.setup_menu()
        
    def setup_header(self, parent):
        """Setup the header section."""
        header_frame = tk.Frame(parent, bg=ModernColors.BG_PRIMARY)
        header_frame.pack(fill='x', pady=(0, 30))
        
        # App title
        title_label = ModernLabel(header_frame, style='title')
        title_label.configure(text="Quest Casting Pro")
        title_label.pack()
        
        # Subtitle
        subtitle_label = ModernLabel(header_frame, style='secondary')
        subtitle_label.configure(text="Professional Meta Quest Casting")
        subtitle_label.pack(pady=(5, 0))
        
    def setup_status_section(self, parent):
        """Setup the status section with card design."""
        # Status card
        status_card = ModernCard(parent)
        status_card.pack(fill='x', pady=(0, 30))
        
        # Status indicator
        self.status_indicator = StatusIndicator(status_card)
        
        # Status text
        self.status_text = tk.StringVar(value="מתחבר למכשיר...")
        self.status_label = ModernLabel(status_card, textvariable=self.status_text, style='primary')
        self.status_label.pack(pady=(10, 0))
        
    def setup_action_buttons(self, parent):
        """Setup the action buttons."""
        button_frame = tk.Frame(parent, bg=ModernColors.BG_PRIMARY)
        button_frame.pack(fill='x', pady=(0, 30))
        
        # Cast button (primary action)
        self.cast_btn = ModernButton(
            button_frame,
            text="🎬 הצג מסך",
            style_type='primary',
            command=self._on_cast_clicked,
            state='disabled'
        )
        self.cast_btn.pack(fill='x', pady=(0, 15))
        
        # Wireless button (secondary action)
        self.wireless_btn = ModernButton(
            button_frame,
            text="📡 חיבור אלחוטי",
            style_type='secondary',
            command=self._on_wireless_clicked,
            state='disabled'
        )
        self.wireless_btn.pack(fill='x')
        
    def setup_footer(self, parent):
        """Setup the footer section."""
        footer_frame = tk.Frame(parent, bg=ModernColors.BG_PRIMARY)
        footer_frame.pack(side='bottom', fill='x')
        
        # Quick actions
        quick_frame = tk.Frame(footer_frame, bg=ModernColors.BG_PRIMARY)
        quick_frame.pack()
        
        # Help button
        help_btn = tk.Button(
            quick_frame,
            text="❓ עזרה",
            relief='flat',
            bd=0,
            bg=ModernColors.BG_PRIMARY,
            fg=ModernColors.PRIMARY_BLUE,
            font=('Helvetica', 12),
            cursor='hand2',
            command=self.show_help
        )
        help_btn.pack(side='left', padx=10)
        
        # Instructions button
        inst_btn = tk.Button(
            quick_frame,
            text="📋 הוראות",
            relief='flat',
            bd=0,
            bg=ModernColors.BG_PRIMARY,
            fg=ModernColors.PRIMARY_BLUE,
            font=('Helvetica', 12),
            cursor='hand2',
            command=self.show_instructions
        )
        inst_btn.pack(side='right', padx=10)
        
    def setup_menu(self):
        """Setup the menu bar."""
        menubar = tk.Menu(self.window)
        menubar.add_command(label="הוראות", command=self.show_instructions)
        menubar.add_command(label="עזרה", command=self.show_help)
        menubar.add_command(label="אודות", command=self.show_about)
        self.window.config(menu=menubar)
        
    def _on_cast_clicked(self):
        """Handle cast button click."""
        if self.on_cast_requested:
            self.on_cast_requested()
            
    def _on_wireless_clicked(self):
        """Handle wireless button click."""
        if self.on_wireless_toggle:
            self.on_wireless_toggle()
            
    def update_device_status(self, device: QuestDevice):
        """Update the GUI based on device status."""
        # Update status indicator
        self.status_indicator.update_status(device)
        
        # Update status text and buttons based on device state
        if device.is_wifi and device.is_authorized:
            self.status_text.set("✅ מחובר אלחוטית - מוכן לשידור")
            self.wireless_btn.configure(
                text="🔌 נתק אלחוטית",
                style_type='danger',
                state='normal'
            )
            self.cast_btn.configure(
                style_type='success',
                state='normal'
            )
        elif device.is_authorized:
            self.status_text.set("✅ מכשיר מחובר - מוכן לשידור")
            self.wireless_btn.configure(
                text="📡 חיבור אלחוטי",
                style_type='secondary',
                state='normal' if device.is_usb else 'disabled'
            )
            self.cast_btn.configure(
                style_type='primary',
                state='normal'
            )
        elif device.state == DeviceState.UNAUTHORIZED:
            self.status_text.set("⚠️ נדרש אישור במכשיר")
            self.wireless_btn.configure(
                text="📡 חיבור אלחוטי",
                style_type='secondary',
                state='disabled'
            )
            self.cast_btn.configure(
                style_type='primary',
                state='disabled'
            )
        else:
            self.status_text.set("🔍 מחפש מכשירים...")
            self.wireless_btn.configure(
                text="📡 חיבור אלחוטי",
                style_type='secondary',
                state='disabled'
            )
            self.cast_btn.configure(
                style_type='primary',
                state='disabled'
            )
            
    def show_error(self, title: str, message: str):
        """Show an error dialog."""
        messagebox.showerror(title, message)
        
    def show_warning(self, title: str, message: str):
        """Show a warning dialog."""
        messagebox.showwarning(title, message)
        
    def show_info(self, title: str, message: str):
        """Show an info dialog."""
        ModernDialog.show_info(self.window, title, message)
        
    def show_rtl_info(self, title: str, message: str):
        """Show an RTL info dialog."""
        ModernDialog.show_info(self.window, title, message)
        
    def show_instructions(self):
        """Show instructions dialog."""
        instructions = (
            "🚀 הוראות התחלה מהירה:\n\n"
            "1️⃣ הפעל מצב מפתח בקווסט\n"
            "2️⃣ חבר בכבל USB למחשב\n"
            "3️⃣ אשר גישה במכשיר (Always Allow)\n"
            "4️⃣ לחץ 'הצג מסך' להתחלת שידור\n\n"
            "💡 לחיבור אלחוטי:\n"
            "לחץ 'חיבור אלחוטי' לאחר החיבור הראשוני"
        )
        ModernDialog.show_info(self.window, "הוראות שימוש", instructions)
        
    def show_help(self):
        """Show help dialog."""
        help_text = (
            "🆘 צריך עזרה?\n\n"
            "📧 מייל: info@loginvr.co.il\n"
            "🌐 אתר: www.loginvr.co.il\n"
            "📹 וידאו הדרכה זמין בתפריט\n\n"
            "🔧 פתרון בעיות נפוצות:\n"
            "• ודא שמצב מפתח פעיל\n"
            "• נסה כבל USB אחר\n"
            "• אתחל את שירותי ADB"
        )
        ModernDialog.show_info(self.window, "עזרה ותמיכה", help_text)
        
    def show_about(self):
        """Show about dialog."""
        about_text = (
            "Quest Casting Pro\n\n"
            "⚡ אפליקציה מקצועית לשידור Quest\n"
            "🎮 תמיכה ב-Quest 2/3/Pro\n"
            "📱 חיבור USB ואלחוטי\n"
            "🌟 ממשק מודרני ויפה\n\n"
            "פותח על ידי LoginVR\n"
            "גרסה 2.1.0 · 2025"
        )
        ModernDialog.show_info(self.window, "אודות", about_text)
        
    def run(self):
        """Start the GUI main loop."""
        self.window.mainloop()
        
    def schedule_callback(self, callback: Callable, delay_ms: int):
        """Schedule a callback to run after a delay."""
        self.window.after(delay_ms, callback)


# Update the main GUI class to use the beautiful version
CastingGUI = BeautifulCastingGUI
