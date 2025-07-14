# LoginVR Quest Caster · v 2.1 (2025-07)

🚀 **REFACTORED FOR ENTERPRISE DEVELOPMENT**  
🌍 **NOW WORKS ON WINDOWS AND macOS!**

One-click mirroring of your **Meta Quest 2 / 3 / Pro** to any Windows 10 / 11 PC or macOS device.  
Built with **Python + Tkinter** on top of ADB and [scrcpy].

[scrcpy]: https://github.com/Genymobile/scrcpy

---

## ✨ What's new in 2.1 (Cross-Platform Edition)

| Category | Upgrade |
|----------|---------|
| **� Cross-Platform Support** | Runs natively on Windows, macOS, and Linux with automatic platform detection |
| **�🏗️ Modular Architecture** | Complete separation of concerns: config, models, ADB management, GUI, and casting logic in separate modules |
| **🔧 Smart Dependency Management** | Automatically detects system-installed tools or uses bundled binaries |
| **📊 Structured Logging** | Comprehensive logging system with configurable levels and file output |
| **🧪 Unit Testing** | Full test suite covering all major components with mocking for hardware dependencies |
| **⚡ Better Error Handling** | Platform-specific error messages and installation instructions |
| **📱 Enhanced Models** | Type-safe device state management with enums and dataclasses |
| **🎯 SOLID Principles** | Single responsibility, dependency injection, and proper abstraction layers |

---

## 🏗️ New Architecture

### **Modular Structure**
```text
casting/
├─ main.py              ← Application controller & entry point
├─ config.py            ← Configuration management with dataclasses
├─ models.py            ← Data models (QuestDevice, AppState, enums)
├─ adb_manager.py       ← ADB operations & device detection
├─ cast_manager.py      ← Screen casting logic via scrcpy
├─ gui.py               ← Tkinter GUI components & dialogs
├─ utils.py             ← Utility functions & logging setup
├─ config.json          ← Default configuration file
├─ test_refactored.py   ← Comprehensive test suite
├─ requirements.txt     ← Python dependencies (none!)
└─ src/                 ← Binary resources (adb, scrcpy, etc.)
```

### **Key Design Patterns**
- **🎯 Dependency Injection**: Managers receive configuration and dependencies
- **📋 Observer Pattern**: GUI callbacks for user actions
- **🏭 Factory Pattern**: Device state creation from ADB output
- **🛡️ Command Pattern**: Encapsulated ADB and scrcpy operations

---

## 🖼️ Status Indicators

| State | Circle | Label | Description |
|-------|--------|-------|-------------|
| **No device / offline** | 🔴 | "וודא שהקווסט דלוק…" | Device not detected |
| **USB unauthorised** | 🟡 | "אשר גישה במכשיר…" | Needs developer mode approval |
| **USB ready** | 🟢 | "מכשיר מחובר" | Connected via USB |
| **Wi-Fi ready** | 🟢 | "מכשיר מחובר אלחוטית" | Wireless casting active |

---

## 🚀 Quick Start

### **Development Setup**
```bash
# Clone and enter directory
cd casting/

# Run tests to verify everything works
python3 test_refactored.py

# Run the application
python3 main.py
```

### **Configuration**
Edit `config.json` to customize:
```json
{
  "refresh_interval_ms": 2000,
  "adb_timeout_ms": 4000,  
  "wireless_port": "5555",
  "scrcpy": {
    "crop": "1600:900:2017:510",
    "bitrate": "4M",
    "max_size": 1024
  }
}
```

---

## 🧪 Testing & Quality

### **Run Test Suite**
```bash
python3 test_refactored.py
```

### **Test Coverage**
- ✅ Configuration loading & validation
- ✅ Device state models & enums  
- ✅ ADB device detection (mocked)
- ✅ scrcpy command generation
- ✅ Error handling scenarios

### **Code Quality Features**
- 🎯 **Type hints** throughout codebase
- 📝 **Comprehensive docstrings** 
- 🧹 **Pylint-clean** code style
- 🔒 **Exception safety** with specific error types
- 📊 **Structured logging** with different levels

---

## 🖥️ Platform Support

| Platform | Status | Installation |
|----------|--------|---------------|
| **Windows 10/11** | ✅ **Fully Supported** | Bundled executables or manual install |
| **macOS** | ✅ **Fully Supported** | Homebrew: `brew install scrcpy android-platform-tools` |
| **Linux** | 🟡 **Theoretical** | Package manager: `apt install scrcpy adb` |

### **Automatic Platform Detection**
- 🔍 **Smart detection** of Windows vs macOS vs Linux
- 🛠️ **Auto-discovery** of system-installed ADB and scrcpy
- 📁 **Fallback** to bundled binaries when needed
- 💬 **Platform-specific** error messages and installation guides

### **Prerequisites**
- **Python ≥ 3.8** for modern type hints and dataclasses
- **Meta Quest 2/3/Pro** with developer mode enabled
- **Platform-specific tools** (auto-detected or bundled)

---

## 🔧 Development Benefits

### **For Developers**
- 🧪 **Easy testing** with comprehensive test suite
- 🔧 **Simple configuration** via JSON files  
- 📊 **Debug logging** for troubleshooting
- 🏗️ **Modular design** for easy feature additions
- 📱 **Type safety** prevents runtime errors

### **For End Users**  
- ⚡ **Same great UX** with better reliability
- 🐛 **Better error messages** with specific guidance
- 🔄 **More stable** wireless connections
- 📝 **Detailed logging** for support cases

---

## 📈 Migration from v2.0

The refactored version maintains **100% API compatibility** for end users while providing a much better foundation for developers:

- **✅ Same UI & functionality**
- **✅ Same configuration options** 
- **✅ Same binary dependencies**
- **🆕 Better error handling**
- **🆕 Comprehensive logging**
- **🆕 Easy testing & debugging**

---

## 🤝 Contributing

The new modular structure makes contributions much easier:

1. **🧪 Write tests** in `test_refactored.py`
2. **🔧 Add configuration** options in `config.py`
3. **📱 Extend models** in `models.py` 
4. **🎨 Improve GUI** in `gui.py`
5. **⚡ Enhance ADB** operations in `adb_manager.py`

---

**Built with ❤️ for enterprise-grade reliability**  
*LoginVR · 2025 · v2.1.0*
