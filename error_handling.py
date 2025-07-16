"""Enhanced error handling and exception management."""

import logging
from typing import Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ApplicationError:
    """Structured error information."""
    code: str
    message: str
    details: Optional[str] = None
    severity: ErrorSeverity = ErrorSeverity.ERROR
    user_message_hebrew: Optional[str] = None
    suggested_action: Optional[str] = None


class CastingException(Exception):
    """Base exception for casting application."""
    
    def __init__(self, error: ApplicationError, original_exception: Optional[Exception] = None):
        self.error = error
        self.original_exception = original_exception
        super().__init__(error.message)


class DeviceConnectionError(CastingException):
    """Device connection related errors."""
    pass


class CastingProcessError(CastingException):
    """Casting process related errors."""
    pass


class ConfigurationError(CastingException):
    """Configuration related errors."""
    pass


class ErrorHandler:
    """Centralized error handling and user feedback."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._error_translations = {
            "DEVICE_NOT_FOUND": ApplicationError(
                code="DEVICE_NOT_FOUND",
                message="No Quest device detected",
                user_message_hebrew="המכשיר אינו מחובר",
                suggested_action="Connect Quest device and enable developer mode",
                severity=ErrorSeverity.WARNING
            ),
            "DEVICE_UNAUTHORIZED": ApplicationError(
                code="DEVICE_UNAUTHORIZED", 
                message="Device detected but not authorized",
                user_message_hebrew="המכשיר זוהה אך לא אושרה הגישה",
                suggested_action="Put on headset and select 'Always Allow' for USB debugging",
                severity=ErrorSeverity.WARNING
            ),
            "CAST_START_FAILED": ApplicationError(
                code="CAST_START_FAILED",
                message="Failed to start casting process",
                user_message_hebrew="לא הצלחנו להתחיל את השידור",
                suggested_action="Check that all required files exist and device is connected",
                severity=ErrorSeverity.ERROR
            ),
            "WIRELESS_CONNECTION_FAILED": ApplicationError(
                code="WIRELESS_CONNECTION_FAILED",
                message="Failed to establish wireless connection",
                user_message_hebrew="החיבור האלחוטי נכשל",
                suggested_action="Ensure device is on same WiFi network",
                severity=ErrorSeverity.ERROR
            )
        }
    
    def get_error(self, error_code: str, details: Optional[str] = None) -> ApplicationError:
        """Get structured error information."""
        error = self._error_translations.get(error_code)
        if error and details:
            error.details = details
        return error or ApplicationError(
            code=error_code,
            message=f"Unknown error: {error_code}",
            details=details
        )
    
    def handle_exception(self, exception: Exception, context: str = "") -> ApplicationError:
        """Convert exception to structured error."""
        if isinstance(exception, CastingException):
            self.logger.error(f"{context}: {exception.error.message}", exc_info=True)
            return exception.error
        
        # Map common exceptions to user-friendly errors
        error_code = "UNKNOWN_ERROR"
        if "device" in str(exception).lower():
            error_code = "DEVICE_CONNECTION_ERROR"
        elif "permission" in str(exception).lower():
            error_code = "PERMISSION_ERROR" 
        elif "timeout" in str(exception).lower():
            error_code = "TIMEOUT_ERROR"
        
        self.logger.error(f"{context}: {str(exception)}", exc_info=True)
        return ApplicationError(
            code=error_code,
            message=str(exception),
            details=context,
            severity=ErrorSeverity.ERROR
        )
