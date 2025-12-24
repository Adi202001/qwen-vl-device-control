"""Utility functions for the device control system."""

import os
import sys
from typing import Dict, List
import json


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'torch',
        'transformers',
        'PIL',
        'pyautogui',
        'pynput',
        'cv2',
        'numpy',
        'tqdm'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'cv2':
                import cv2
            else:
                __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies are installed!")
        return True


def check_models():
    """Check if models are downloaded."""
    from transformers import AutoTokenizer
    import config
    
    print("\nChecking models...")
    
    models_to_check = [
        ("Vision Model", config.VISION_MODEL_NAME),
        ("Text Generation Model", config.TEXT_MODEL_NAME)
    ]
    
    all_available = True
    
    for name, model_name in models_to_check:
        try:
            print(f"Checking {name} ({model_name})...")
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            print(f"✓ {name} is available")
        except Exception as e:
            print(f"✗ {name} needs to be downloaded")
            print(f"  Error: {e}")
            all_available = False
    
    if all_available:
        print("\n✓ All models are available!")
    else:
        print("\nℹ Models will be downloaded on first use.")
    
    return all_available


def get_system_info():
    """Get system information."""
    import platform
    import pyautogui
    
    print("\n" + "=" * 60)
    print("System Information")
    print("=" * 60)
    
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Architecture: {platform.machine()}")
    
    screen_width, screen_height = pyautogui.size()
    print(f"Screen Resolution: {screen_width}x{screen_height}")
    
    # Check for GPU
    try:
        import torch
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"CUDA Version: {torch.version.cuda}")
        else:
            print("GPU: Not available (using CPU)")
    except:
        print("GPU: Unable to detect")
    
    print("=" * 60)


def save_commands_to_file(commands: List[Dict], filename: str):
    """Save commands to a JSON file.
    
    Args:
        commands: List of command dictionaries
        filename: Output filename
    """
    with open(filename, 'w') as f:
        json.dump(commands, f, indent=2)
    print(f"Commands saved to {filename}")


def load_commands_from_file(filename: str) -> List[Dict]:
    """Load commands from a JSON file.
    
    Args:
        filename: Input filename
        
    Returns:
        List of command dictionaries
    """
    with open(filename, 'r') as f:
        commands = json.load(f)
    print(f"Loaded {len(commands)} commands from {filename}")
    return commands


def create_sample_commands_file():
    """Create a sample commands file for testing."""
    sample_commands = [
        {
            "action": "wait",
            "duration": 1.0,
            "raw": "WAIT: 1.0"
        },
        {
            "action": "click",
            "target": "center",
            "raw": "CLICK: center"
        },
        {
            "action": "type",
            "text": "Sample text",
            "raw": "TYPE: Sample text"
        },
        {
            "action": "key",
            "key": "enter",
            "raw": "KEY: enter"
        }
    ]
    
    filename = "sample_commands.json"
    save_commands_to_file(sample_commands, filename)
    return filename


def test_device_control():
    """Test basic device control functionality."""
    print("\nTesting Device Control...")
    print("This will move your mouse and type. Press Ctrl+C to cancel.")
    print("Starting in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        from device_control_executor import DeviceControlExecutor
        
        executor = DeviceControlExecutor()
        
        # Safe test commands
        test_commands = [
            {
                "action": "wait",
                "duration": 0.5,
                "raw": "WAIT: 0.5"
            }
        ]
        
        executor.execute_commands(test_commands)
        
        print("✓ Device control test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Device control test failed: {e}")
        return False


def main():
    """Run utility checks and tests."""
    print("=" * 60)
    print("Device Control System - Utility & Diagnostics")
    print("=" * 60)
    
    # System info
    get_system_info()
    
    # Check dependencies
    print("\n" + "=" * 60)
    print("Checking Dependencies")
    print("=" * 60)
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\nPlease install missing dependencies before continuing.")
        return 1
    
    # Check models
    print("\n" + "=" * 60)
    print("Checking Models")
    print("=" * 60)
    check_models()
    
    # Test device control
    print("\n" + "=" * 60)
    print("Device Control Test")
    print("=" * 60)
    test_device_control()
    
    # Create sample file
    print("\n" + "=" * 60)
    print("Creating Sample Files")
    print("=" * 60)
    sample_file = create_sample_commands_file()
    print(f"Created sample commands file: {sample_file}")
    
    print("\n" + "=" * 60)
    print("Diagnostics Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'python main.py' for interactive mode")
    print("2. Run 'python examples.py' to see examples")
    print("3. Run 'python main.py --help' for all options")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
