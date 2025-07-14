# Cross-Platform Installation Guide

## 🚀 **Now Works on Windows AND macOS!**

The LoginVR Quest Caster v2.1 has been refactored to support both Windows and macOS with automatic platform detection and dependency management.

---

## 🖥️ **Windows Installation**

### **Prerequisites**
- Windows 10/11
- Python 3.8 or later
- Meta Quest 2/3/Pro with developer mode enabled

### **Setup Steps**
1. **Download the application**
   ```bash
   git clone https://github.com/Avi-Kohen/casting.git
   cd casting
   ```

2. **Install dependencies** (if not using bundled binaries)
   - Download ADB from Android SDK Platform Tools
   - Download scrcpy from [GitHub releases](https://github.com/Genymobile/scrcpy/releases)
   - Place `adb.exe` and `scrcpy.exe` in the `src/` folder

3. **Install Quest ADB drivers**
   - Install Oculus desktop app OR
   - Download Quest ADB drivers manually

4. **Run the application**
   ```bash
   python main.py
   ```

---

## 🍎 **macOS Installation**

### **Prerequisites**
- macOS 10.15 (Catalina) or later
- Python 3.8 or later (comes with macOS)
- Homebrew package manager
- Meta Quest 2/3/Pro with developer mode enabled

### **Setup Steps**

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install dependencies**
   ```bash
   # Install ADB and scrcpy via Homebrew
   brew install scrcpy android-platform-tools
   ```

3. **Download the application**
   ```bash
   git clone https://github.com/Avi-Kohen/casting.git
   cd casting
   ```

4. **Run the application**
   ```bash
   python3 main.py
   ```

---

## 🔧 **Cross-Platform Features**

### **Automatic Detection**
The application automatically detects:
- ✅ **Operating system** (Windows, macOS, Linux)
- ✅ **Available executables** (system ADB/scrcpy vs bundled)
- ✅ **Platform-specific subprocess flags**
- ✅ **Appropriate file paths and extensions**

### **Dependency Management**
- **Windows**: Uses bundled `.exe` files in `src/` folder
- **macOS/Linux**: Prefers system-installed tools, falls back to bundled
- **Smart detection**: Checks both locations automatically
- **Helpful errors**: Provides platform-specific installation instructions

### **Cross-Platform Compatibility**
| Feature | Windows | macOS | Linux* |
|---------|---------|-------|---------|
| **GUI** | ✅ Tkinter | ✅ Tkinter | ✅ Tkinter |
| **ADB** | ✅ adb.exe | ✅ Homebrew | ✅ Package manager |
| **scrcpy** | ✅ scrcpy.exe | ✅ Homebrew | ✅ Package manager |
| **Quest Detection** | ✅ | ✅ | ✅ |
| **Wireless Casting** | ✅ | ✅ | ✅ |

*Linux support is theoretical but should work with minor adjustments

---

## 🧪 **Testing Cross-Platform**

### **Verify Installation**
```bash
# Test the refactored code
python3 test_refactored.py

# Should show:
# ✅ All tests passed! The refactored code is working correctly.
```

### **Test Dependencies**
```bash
# Check if ADB works
adb devices

# Check if scrcpy works  
scrcpy --help
```

### **Test the Application**
```bash
# Run the GUI application
python3 main.py
```

---

## 🐛 **Troubleshooting**

### **Windows Issues**
- **"ADB not found"**: Place `adb.exe` in the `src/` folder
- **"scrcpy not found"**: Place `scrcpy.exe` in the `src/` folder  
- **"Device not detected"**: Install Quest ADB drivers from Oculus

### **macOS Issues**
- **"Command not found: brew"**: Install Homebrew first
- **"Permission denied"**: Run with `sudo` if needed for ADB access
- **"Device not authorized"**: Enable "Always allow" on Quest when prompted

### **General Issues**
- **"No devices found"**: Enable developer mode on Quest and connect via USB
- **"Connection failed"**: Try different USB cable or port
- **"Python not found"**: Use `python3` instead of `python` on macOS/Linux

---

## 📱 **Quest Developer Mode Setup**

### **Enable Developer Mode**
1. Install Oculus mobile app
2. Go to Settings → Developer Mode
3. Enable Developer Mode
4. Connect Quest to PC via USB
5. Put on headset and select "Always Allow" when prompted

### **Verify Connection**
```bash
# Should show your Quest device
adb devices
```

---

## 🎯 **Platform-Specific Optimizations**

### **Windows Optimizations**
- Uses `CREATE_NO_WINDOW` flag to hide console windows
- Bundled executables for standalone operation
- Optimized for Windows-style file paths

### **macOS Optimizations**  
- Uses system-installed tools when available
- Respects macOS security model
- Follows Unix-style conventions

### **Performance**
- Same performance across platforms
- Platform-appropriate subprocess handling
- Smart dependency detection reduces startup time

---

**🎉 Enjoy cross-platform Quest casting!**  
*The same great experience on Windows and macOS*
