#!/usr/bin/env python3
"""
Demo script to showcase the enhanced macOS UI improvements.
Run this to see the new interface in action.
"""

import sys
import os
import platform

# Add the casting directory to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from main import CastingApplication
    
    def main():
        print("🚀 Starting LoginVR Quest Caster with Enhanced UI")
        print(f"🖥️  Platform: {platform.system()}")
        
        if platform.system() == 'Darwin':
            print("🍎 macOS detected - Loading enhanced UI styling:")
            print("   ✅ Native macOS colors (System Green, Orange, Red)")
            print("   ✅ SF Pro Display font")
            print("   ✅ Larger status indicator with shadow")
            print("   ✅ Modern button styling with hover effects")
            print("   ✅ Native window appearance")
            print("   ✅ Better spacing and typography")
        elif platform.system() == 'Windows':
            print("🪟 Windows detected - Loading Fluent Design styling:")
            print("   ✅ Segoe UI font")
            print("   ✅ Windows accent colors")
            print("   ✅ Standard button styling")
        else:
            print("🐧 Linux detected - Loading Material Design styling")
        
        print("\n🎨 UI Enhancements:")
        print("   • Larger, more visible status indicator")
        print("   • Platform-native fonts and colors")
        print("   • Enhanced button styling with hover effects")
        print("   • Better spacing and layout")
        print("   • Improved dialog boxes")
        print("   • Cross-platform consistency")
        
        print("\n🎯 Starting application...\n")
        
        try:
            app = CastingApplication()
            app.run()
        except KeyboardInterrupt:
            print("\n👋 Application closed by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("💡 Make sure you have the required dependencies installed")
            
            if platform.system() == 'Darwin':
                print("\n🍎 macOS users run:")
                print("   brew install scrcpy android-platform-tools")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all files are in the same directory")
    print("🔧 Try running: python3 main.py")
