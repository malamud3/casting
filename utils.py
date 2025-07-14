"""Utility functions and helpers."""

import os
import sys
import webbrowser
from urllib.parse import quote


def resource_path(name: str) -> str:
    """
    Return absolute path to *name*, whether running from source or a PyInstaller bundle.
    
    Args:
        name: Resource filename
        
    Returns:
        Absolute path to the resource
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    if not base.endswith("src"):
        base = os.path.join(base, "src")
    return os.path.join(base, name)


def open_email_client(email: str, subject: str, body: str):
    """
    Open the default email client with pre-filled email.
    
    Args:
        email: Recipient email address
        subject: Email subject
        body: Email body
    """
    uri = f"mailto:{email}?subject={quote(subject)}&body={quote(body)}"
    webbrowser.open_new(uri)


def open_url(url: str):
    """
    Open URL in the default web browser.
    
    Args:
        url: URL to open
    """
    webbrowser.open_new(url)


def setup_logging(level: str = "INFO", log_file: str = None):
    """
    Set up application logging.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    import logging
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    handlers = [console_handler]
    
    # Set up file handler if specified
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        except Exception as e:
            print(f"Warning: Could not set up file logging: {e}")
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        handlers=handlers,
        force=True
    )
    
    # Reduce noise from some modules
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
