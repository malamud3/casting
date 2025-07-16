"""Enhanced main entry point with professional error handling and dependency injection."""

import sys
import traceback
import logging
from pathlib import Path

from dependency_injection import ServiceRegistry, ServiceConfiguration
from utils import resource_path


def setup_exception_handling():
    """Setup global exception handling."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger = logging.getLogger("uncaught")
        logger.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    
    sys.excepthook = handle_exception


def create_service_configuration() -> ServiceConfiguration:
    """Create service configuration from environment and arguments."""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Quest Casting Application")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--src-dir", default="src", help="Source directory path")
    parser.add_argument("--icon", help="Icon file path")
    
    args = parser.parse_args()
    
    return ServiceConfiguration(
        log_level=args.log_level,
        config_path=args.config,
        src_dir=resource_path(args.src_dir),
        icon_path=args.icon or resource_path("temp.ico")
    )


def main():
    """Enhanced main entry point with dependency injection."""
    try:
        # Setup global exception handling
        setup_exception_handling()
        
        # Create service configuration
        config = create_service_configuration()
        
        # Create service registry with dependency injection
        registry = ServiceRegistry(config)
        registry.register_application_services()
        
        # Create and run application
        app = registry.create_application()
        app.run()
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Try: pip install -r requirements.txt")
        sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Make sure all required files are in the correct location")
        sys.exit(1)
        
    except PermissionError as e:
        print(f"❌ Permission denied: {e}")
        print("💡 Try running as administrator or check file permissions")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print(f"📝 Full error details:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
