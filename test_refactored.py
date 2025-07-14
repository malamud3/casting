"""
Test script for the refactored casting application.
Tests the modular components without requiring actual hardware.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the casting directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from config import load_config, AppConfig, ScrcpyConfig
from models import QuestDevice, Transport, DeviceState, AppState
from adb_manager import ADBManager
from cast_manager import CastManager
from platform_utils import PlatformManager, platform_manager


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_default_config(self):
        """Test loading default configuration."""
        config = AppConfig()
        self.assertEqual(config.refresh_interval_ms, 2000)
        self.assertEqual(config.wireless_port, "5555")
        self.assertIsInstance(config.scrcpy, ScrcpyConfig)
    
    def test_config_loading(self):
        """Test loading configuration from file."""
        config = load_config()
        self.assertIsInstance(config, AppConfig)
        self.assertIsInstance(config.scrcpy, ScrcpyConfig)


class TestModels(unittest.TestCase):
    """Test data models."""
    
    def test_quest_device(self):
        """Test QuestDevice model."""
        # Test Wi-Fi device
        wifi_device = QuestDevice(Transport.WIFI, DeviceState.DEVICE, "192.168.1.100:5555")
        self.assertTrue(wifi_device.is_wifi)
        self.assertFalse(wifi_device.is_usb)
        self.assertTrue(wifi_device.is_authorized)
        self.assertTrue(wifi_device.is_connected)
        self.assertEqual(wifi_device.status_key, "wifi")
        
        # Test USB unauthorized device
        usb_device = QuestDevice(Transport.USB, DeviceState.UNAUTHORIZED, "ABC123")
        self.assertFalse(usb_device.is_wifi)
        self.assertTrue(usb_device.is_usb)
        self.assertFalse(usb_device.is_authorized)
        self.assertTrue(usb_device.is_connected)
        self.assertEqual(usb_device.status_key, "unauthorized")
    
    def test_app_state(self):
        """Test AppState model."""
        state = AppState()
        self.assertIsNone(state.current_device)
        self.assertIsNone(state.last_wifi_serial)
        
        # Update with Wi-Fi device
        wifi_device = QuestDevice(Transport.WIFI, DeviceState.DEVICE, "192.168.1.100:5555")
        state.update_device(wifi_device)
        self.assertEqual(state.current_device, wifi_device)
        self.assertEqual(state.last_wifi_serial, "192.168.1.100:5555")


class TestADBManager(unittest.TestCase):
    """Test ADB manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = AppConfig()
        self.adb_manager = ADBManager(self.config, "/fake/adb/path")
    
    @patch('subprocess.run')
    def test_detect_quest_device_wifi(self, mock_run):
        """Test detecting Wi-Fi Quest device."""
        # Mock ADB devices output with Wi-Fi device
        mock_run.return_value.stdout = """List of devices attached
192.168.1.100:5555	device	product:hollywood transport_id:2"""
        mock_run.return_value.returncode = 0
        
        device = self.adb_manager.detect_quest_device()
        self.assertEqual(device.transport, Transport.WIFI)
        self.assertEqual(device.state, DeviceState.DEVICE)
        self.assertEqual(device.serial, "192.168.1.100:5555")
    
    @patch('subprocess.run')
    def test_detect_quest_device_usb(self, mock_run):
        """Test detecting USB Quest device."""
        # Mock ADB devices output with USB device
        mock_run.return_value.stdout = """List of devices attached
1WMHH123456789	unauthorized	usb:1-1 product:hollywood"""
        mock_run.return_value.returncode = 0
        
        device = self.adb_manager.detect_quest_device()
        self.assertEqual(device.transport, Transport.USB)
        self.assertEqual(device.state, DeviceState.UNAUTHORIZED)
        self.assertEqual(device.serial, "1WMHH123456789")
    
    @patch('subprocess.run')
    def test_detect_no_device(self, mock_run):
        """Test when no device is detected."""
        # Mock ADB devices output with no devices
        mock_run.return_value.stdout = """List of devices attached"""
        mock_run.return_value.returncode = 0
        
        device = self.adb_manager.detect_quest_device()
        self.assertEqual(device.transport, Transport.UNKNOWN)
        self.assertEqual(device.state, DeviceState.UNKNOWN)
        self.assertIsNone(device.serial)


class TestCastManager(unittest.TestCase):
    """Test cast manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = AppConfig()
        self.cast_manager = CastManager(self.config, "/fake/src/dir")
    
    def test_generate_scrcpy_command(self):
        """Test scrcpy command generation."""
        cmd = self.cast_manager.generate_scrcpy_command("192.168.1.100:5555")
        
        # Verify command structure
        self.assertIn("-s", cmd)
        self.assertIn("192.168.1.100:5555", cmd)
        self.assertIn("--render-driver", cmd)
        self.assertIn("opengl", cmd)
        self.assertIn("--crop", cmd)
        self.assertIn("1600:900:2017:510", cmd)


class TestPlatformUtils(unittest.TestCase):
    """Test cross-platform functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.platform_mgr = PlatformManager()
    
    def test_platform_detection(self):
        """Test platform detection works correctly."""
        # Should detect current platform
        self.assertIsInstance(self.platform_mgr.is_windows, bool)
        self.assertIsInstance(self.platform_mgr.is_macos, bool)
        self.assertIsInstance(self.platform_mgr.is_linux, bool)
        
        # Exactly one should be True
        platform_flags = [
            self.platform_mgr.is_windows,
            self.platform_mgr.is_macos, 
            self.platform_mgr.is_linux
        ]
        self.assertEqual(sum(platform_flags), 1)
    
    def test_executable_paths(self):
        """Test executable path generation."""
        src_dir = "/fake/src"
        
        adb_path = self.platform_mgr.get_adb_executable(src_dir)
        scrcpy_path = self.platform_mgr.get_scrcpy_executable(src_dir)
        
        # Should return valid paths
        self.assertIsInstance(adb_path, str)
        self.assertIsInstance(scrcpy_path, str)
        self.assertTrue(len(adb_path) > 0)
        self.assertTrue(len(scrcpy_path) > 0)
    
    def test_subprocess_flags(self):
        """Test subprocess flags are appropriate for platform."""
        flags = self.platform_mgr.get_subprocess_flags()
        self.assertIsInstance(flags, dict)
        
        # Windows should have creationflags, others should be empty
        if self.platform_mgr.is_windows:
            self.assertIn("creationflags", flags)
        else:
            self.assertEqual(flags, {})
    
    def test_installation_instructions(self):
        """Test that installation instructions are provided."""
        instructions = self.platform_mgr.get_installation_instructions()
        self.assertIsInstance(instructions, str)
        self.assertTrue(len(instructions) > 50)  # Should be substantial text


class TestCrossplatformIntegration(unittest.TestCase):
    """Test cross-platform integration."""
    
    def test_cast_manager_dependencies(self):
        """Test cast manager dependency checking."""
        from cast_manager import CastManager
        from config import AppConfig
        
        config = AppConfig()
        cast_mgr = CastManager(config, "/fake/src/dir")
        
        # Should not crash when checking dependencies
        deps_ok, deps_msg = cast_mgr.check_dependencies()
        self.assertIsInstance(deps_ok, bool)
        self.assertIsInstance(deps_msg, str)


def run_tests():
    """Run all tests."""
    print("Running tests for the refactored casting application...\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestADBManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCastManager))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatformUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossplatformIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatformUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossplatformIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\n✅ All tests passed! The refactored code is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
