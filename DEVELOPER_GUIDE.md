# Developer Guide - LoginVR Quest Caster v2.1

## 🏗️ Architecture Overview

The application follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────┐
│   main.py       │  ← Application Controller
├─────────────────┤
│   gui.py        │  ← Presentation Layer
├─────────────────┤
│ adb_manager.py  │  ← Business Logic Layer  
│ cast_manager.py │
├─────────────────┤
│   models.py     │  ← Data Layer
│   config.py     │
├─────────────────┤
│   utils.py      │  ← Infrastructure Layer
└─────────────────┘
```

## 📝 Code Organization

### **main.py** - Application Controller
- **CastingApplication class**: Main application orchestrator
- Dependency injection for all managers
- Event handling coordination
- Application lifecycle management

### **config.py** - Configuration Management
- **AppConfig dataclass**: Main configuration container
- **ScrcpyConfig dataclass**: scrcpy-specific settings
- JSON file loading with fallback to defaults
- Type-safe configuration access

### **models.py** - Data Models
- **QuestDevice**: Device state representation
- **Transport/DeviceState enums**: Type-safe state values
- **AppState**: Global application state
- Rich comparison and property methods

### **adb_manager.py** - ADB Operations
- **ADBManager class**: All ADB command operations
- Device detection and parsing
- Wi-Fi/USB connection management
- Subprocess handling with timeouts

### **cast_manager.py** - Casting Logic
- **CastManager class**: scrcpy operations
- Command generation from configuration
- Process management for casting
- Script generation and updates

### **gui.py** - User Interface
- **CastingGUI class**: Main GUI controller
- Modular dialog classes
- RTL text support for Hebrew
- Callback-based event handling

### **utils.py** - Utilities
- Resource path resolution
- Logging configuration
- Helper functions

## 🧪 Testing Strategy

### **Test Structure**
- **Unit tests** for each major component
- **Mocking** for external dependencies (subprocess, file I/O)
- **Integration tests** for component interactions
- **Regression tests** for bug fixes

### **Running Tests**
```bash
# Run all tests
python3 test_refactored.py

# Run with verbose output
python3 -v test_refactored.py

# Run specific test class
python3 -m unittest test_refactored.TestADBManager
```

### **Adding New Tests**
1. Create test class inheriting from `unittest.TestCase`
2. Use `@patch` decorator for mocking external calls
3. Test both success and failure scenarios
4. Add assertions for expected behavior

## 🔧 Configuration Management

### **Default Configuration**
Configuration loads automatically from `config.json` with these defaults:
- Refresh interval: 2000ms
- ADB timeout: 4000ms  
- Wireless port: 5555
- scrcpy settings: optimized for Quest

### **Adding New Config Options**
1. Add field to appropriate dataclass in `config.py`
2. Update `config.json` with default value
3. Use the config value in relevant manager
4. Add test coverage for the new option

### **Configuration Validation**
- Dataclasses provide runtime type checking
- JSON schema validation on load
- Fallback to defaults on invalid config
- User-friendly error messages

## 📊 Logging & Debugging

### **Logging Levels**
- **DEBUG**: Detailed ADB commands and responses
- **INFO**: Application lifecycle events
- **WARNING**: Recoverable errors
- **ERROR**: Serious failures

### **Log Configuration**
```python
# Enable debug logging
setup_logging("DEBUG", "debug.log")

# Console only
setup_logging("INFO")
```

### **Debug Techniques**
1. Enable DEBUG logging to see ADB commands
2. Use test suite to isolate component issues
3. Check `config.json` for configuration problems
4. Monitor subprocess return codes

## 🚀 Adding New Features

### **New ADB Operations**
1. Add method to `ADBManager` class
2. Include proper error handling
3. Add logging for debugging
4. Write unit tests with mocking
5. Update documentation

### **New GUI Components**
1. Create dialog class in `gui.py`
2. Add callback mechanism if needed
3. Support RTL text for Hebrew
4. Test dialog behavior
5. Update main GUI integration

### **New Configuration Options**
1. Extend appropriate dataclass
2. Update JSON schema
3. Add validation logic
4. Document the new option
5. Add migration logic if needed

## 🔄 Development Workflow

### **Before Making Changes**
1. Run existing tests: `python3 test_refactored.py`
2. Check current code with linting tools
3. Review architecture documentation
4. Plan the change scope

### **During Development**
1. Write tests first (TDD approach)
2. Implement minimal viable change
3. Run tests frequently
4. Add logging for debugging
5. Update documentation

### **Before Committing**
1. Run full test suite
2. Test with real hardware if possible
3. Check error handling paths
4. Update relevant documentation
5. Verify configuration compatibility

## 🐛 Troubleshooting

### **Common Issues**

**Import Errors**
- Ensure all files are in the same directory
- Check Python path configuration
- Verify all dependencies exist

**ADB Connection Issues**
- Check ADB binary exists in `src/`
- Verify device is in developer mode
- Test ADB manually: `src/adb.exe devices`

**GUI Problems**
- Check icon file exists
- Verify Tkinter is available
- Test with basic window creation

**Configuration Issues**
- Validate JSON syntax
- Check dataclass field types
- Test with default configuration

### **Debug Commands**
```bash
# Test ADB directly
src/adb.exe devices -l

# Test configuration loading
python3 -c "from config import load_config; print(load_config())"

# Test device detection
python3 -c "from adb_manager import ADBManager; from config import load_config; print(ADBManager(load_config(), 'src/adb.exe').detect_quest_device())"
```

## 📈 Performance Considerations

### **Optimization Areas**
- **ADB polling frequency**: Balance responsiveness vs. CPU usage
- **GUI refresh rate**: Smooth updates without flicker
- **Subprocess management**: Proper cleanup and timeout handling
- **Memory usage**: Avoid holding large objects unnecessarily

### **Monitoring Performance**
- Use logging to track operation timing
- Monitor subprocess resource usage
- Profile GUI responsiveness
- Test with long-running sessions

## 🔒 Security Best Practices

### **Input Validation**
- Validate all ADB output parsing
- Sanitize file paths
- Check subprocess arguments
- Validate configuration values

### **Process Security**
- Use proper subprocess flags
- Handle timeout scenarios
- Clean up processes on exit
- Limit subprocess privileges

### **Error Information**
- Don't expose sensitive paths in errors
- Limit debug information in production
- Sanitize log file content
- Handle exceptions gracefully

---

**Happy coding! 🚀**  
*This guide should help you maintain and extend the codebase effectively.*
