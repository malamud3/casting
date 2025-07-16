# Quest Casting Pro - Professional Edition

A sophisticated, enterprise-grade Python application for casting Meta Quest devices to your computer with advanced error handling, async operations, and dependency injection.

## ✨ Features

### Core Functionality
- **🎮 Meta Quest Casting**: Stream your Quest device to PC/Mac
- **📱 Device Discovery**: Automatic USB and wireless device detection
- **🔄 Wireless Connection**: Connect to Quest devices over WiFi
- **⚡ High Performance**: Async operations for non-blocking UI

### Professional Features
- **🏗️ SOLID Architecture**: Modular design following SOLID principles
- **🔧 Dependency Injection**: Professional IoC container
- **🚨 Error Handling**: Centralized error management with Hebrew localization
- **📊 Metrics & Monitoring**: Application performance tracking
- **⚙️ Configuration Management**: YAML-based config with validation
- **🧪 Comprehensive Testing**: Full test suite with async support

### Cross-Platform Support
- **🍎 macOS**: Native UI styling and optimizations
- **🪟 Windows**: Full compatibility with Windows 10/11
- **🐧 Linux**: Ubuntu and other distributions supported

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python 3.8 or higher
python --version

# Install ADB (Android Debug Bridge)
# macOS: brew install android-platform-tools
# Windows: Download from Android SDK
# Linux: sudo apt install android-tools-adb

# Install scrcpy
# macOS: brew install scrcpy
# Windows: Download from GitHub releases
# Linux: sudo apt install scrcpy
```

### Installation
```bash
# Clone or download the project
cd casting

# Install dependencies
pip install -r requirements.txt

# Run the application
python main_enhanced.py
```

### Basic Usage
1. **Connect Quest**: Connect your Quest device via USB
2. **Enable Developer Mode**: Enable developer mode on your Quest
3. **Launch App**: Run the casting application
4. **Start Casting**: Click "Start Casting" to begin

## 🏗️ Architecture

### Professional Design Patterns

```
Enhanced Application Architecture
├── 🎯 Dependency Injection Container
├── 🔧 Service Registry & Factory
├── 📊 Application Metrics
├── 🚨 Centralized Error Handling
├── ⚡ Async Device Operations
└── ⚙️ Configuration Management
```

### Core Services

#### Error Handling System
```python
from error_handling import ErrorHandler, ErrorSeverity

handler = ErrorHandler()
error = handler.create_error(
    "DEVICE_001", 
    "Device not found", 
    ErrorSeverity.ERROR
)
```

#### Async Device Operations
```python
from async_operations import AsyncDeviceManager

manager = AsyncDeviceManager()
devices = await manager.scan_devices(progress_callback)
```

#### Configuration Management
```python
from enhanced_config import ConfigManager

config = ConfigManager("config.yaml")
settings = config.get_config()
```

#### Dependency Injection
```python
from dependency_injection import ServiceRegistry

registry = ServiceRegistry(config)
registry.register_application_services()
app = registry.create_application()
```

## ⚙️ Configuration

### Configuration File (`config.yaml`)
```yaml
application:
  title: "Quest Casting Pro"
  theme: "auto"  # auto, light, dark
  language: "he"  # he, en

device_discovery:
  scan_timeout: 10.0
  wireless_port_range: [5555, 5585]

display:
  default_resolution: "1920x1080"
  default_bitrate: "8M"
  show_touches: true

logging:
  level: "INFO"
  file_enabled: true
  file_path: "logs/casting.log"
```

### Environment Variables
```bash
export CASTING_CONFIG_PATH="/path/to/config.yaml"
export CASTING_LOG_LEVEL="DEBUG"
export CASTING_SRC_DIR="/path/to/src"
```

## 🧪 Testing

### Run Test Suite
```bash
# Install development dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest test_enhanced.py -v

# Run with coverage
pytest test_enhanced.py --cov=. --cov-report=html

# Run specific test category
pytest test_enhanced.py::TestErrorHandling -v
```

### Test Categories
- **Error Handling**: Exception management and Hebrew localization
- **Async Operations**: Non-blocking device operations
- **Configuration**: YAML validation and type safety
- **Dependency Injection**: Service registration and resolution

## 🔧 Development

### Project Structure
```
casting/
├── main_enhanced.py              # Enhanced entry point
├── enhanced_application.py       # Main application with metrics
├── error_handling.py            # Centralized error management
├── async_operations.py          # Async device operations
├── enhanced_config.py           # Configuration management
├── dependency_injection.py      # DI container
├── interfaces.py               # Abstract interfaces
├── service_factory.py          # Service factory
├── platform_detector.py        # Platform detection
├── executable_finder.py        # Executable location
├── process_manager.py          # Process management
├── ui_themes.py               # UI theming
├── test_enhanced.py           # Professional test suite
├── config.example.yaml        # Configuration example
└── requirements.txt           # Dependencies
```

### Key Design Principles

#### SOLID Principles
- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable
- **I**nterface Segregation: Many specific interfaces vs one general
- **D**ependency Inversion: Depend on abstractions, not concretions

#### Professional Patterns
- **Dependency Injection**: IoC container for loose coupling
- **Factory Pattern**: Service creation abstraction
- **Observer Pattern**: Progress and status updates
- **Strategy Pattern**: Platform-specific implementations
- **Command Pattern**: Async operation management

### Code Quality Tools
```bash
# Format code
black .

# Type checking
mypy .

# Linting
ruff check .

# Documentation
sphinx-build -b html docs/ docs/_build/
```

## 📊 Monitoring & Metrics

### Application Metrics
```python
from enhanced_application import ApplicationMetrics

metrics = ApplicationMetrics()
print(f"Devices scanned: {metrics.devices_scanned}")
print(f"Successful connections: {metrics.successful_connections}")
print(f"Average scan time: {metrics.average_scan_time}")
```

### Error Tracking
```python
from error_handling import ErrorHandler

handler = ErrorHandler()
errors = handler.get_error_history()
for error in errors:
    print(f"{error.timestamp}: {error.code} - {error.message}")
```

## 🌍 Localization

### Supported Languages
- **Hebrew (עברית)**: Primary language with full UI translation
- **English**: Secondary language for international users

### Adding Translations
```python
# In error_handling.py
HEBREW_TRANSLATIONS = {
    "DEVICE_NOT_FOUND": "המכשיר לא נמצא",
    "CONNECTION_FAILED": "החיבור נכשל",
    # Add more translations...
}
```

## 🚀 Building & Distribution

### Create Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller main_enhanced.spec

# Output in dist/ folder
```

### Package for Distribution
```bash
# Create wheel package
python setup.py bdist_wheel

# Install locally
pip install dist/quest_casting_pro-*.whl
```

## 🐛 Troubleshooting

### Common Issues

#### Device Not Detected
```bash
# Check ADB connection
adb devices

# Restart ADB
adb kill-server && adb start-server
```

#### Permission Errors
```bash
# macOS/Linux: Check permissions
ls -la /dev/tty.*

# Windows: Run as administrator
```

#### Wireless Connection Issues
```bash
# Check network connectivity
ping 192.168.1.100

# Verify port availability
telnet 192.168.1.100 5555
```

### Debug Mode
```bash
# Run with debug logging
python main_enhanced.py --log-level DEBUG

# Check logs
tail -f logs/casting.log
```

## 🤝 Contributing

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/yourusername/casting.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest test_enhanced.py -v
```

### Code Standards
- **Python 3.8+**: Modern Python features and typing
- **Type Hints**: Full type annotation coverage
- **Documentation**: Comprehensive docstrings
- **Testing**: 90%+ code coverage
- **Error Handling**: Graceful failure and recovery

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ADB**: Android Debug Bridge by Google
- **scrcpy**: Screen copy tool by Genymobile
- **Pydantic**: Data validation library
- **PyInstaller**: Python executable builder

---

**Quest Casting Pro** - Professional Meta Quest casting solution with enterprise-grade architecture and reliability.
