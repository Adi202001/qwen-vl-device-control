"""Device Control Executor for executing automation commands."""

import pyautogui
import time
from typing import Dict, List, Tuple, Optional
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import config


class DeviceControlExecutor:
    """Executes device control commands like click, type, and key press."""
    
    def __init__(self):
        """Initialize the device control executor."""
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        
        # Set PyAutoGUI safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = config.ACTION_DELAY
        
        # Get screen size
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"Device Control Executor initialized")
        print(f"Screen size: {self.screen_width}x{self.screen_height}")
        
        # Key mapping for special keys
        self.key_mapping = {
            'enter': Key.enter,
            'return': Key.enter,
            'tab': Key.tab,
            'space': Key.space,
            'backspace': Key.backspace,
            'delete': Key.delete,
            'escape': Key.esc,
            'esc': Key.esc,
            'shift': Key.shift,
            'ctrl': Key.ctrl,
            'control': Key.ctrl,
            'alt': Key.alt,
            'cmd': Key.cmd,
            'command': Key.cmd,
            'up': Key.up,
            'down': Key.down,
            'left': Key.left,
            'right': Key.right,
            'home': Key.home,
            'end': Key.end,
            'pageup': Key.page_up,
            'pagedown': Key.page_down,
        }
    
    def execute_command(self, command: Dict) -> bool:
        """Execute a single device control command.
        
        Args:
            command: Dictionary with action type and parameters
            
        Returns:
            True if successful, False otherwise
        """
        action = command.get("action", "").lower()
        
        try:
            if action == "click":
                return self._execute_click(command)
            elif action == "type":
                return self._execute_type(command)
            elif action == "key":
                return self._execute_key(command)
            elif action == "wait":
                return self._execute_wait(command)
            else:
                print(f"Unknown action: {action}")
                return False
        except Exception as e:
            print(f"Error executing command {command}: {e}")
            return False
    
    def execute_commands(self, commands: List[Dict]) -> Tuple[int, int]:
        """Execute a sequence of commands.
        
        Args:
            commands: List of command dictionaries
            
        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0
        
        print(f"\nExecuting {len(commands)} commands...")
        
        for i, command in enumerate(commands, 1):
            print(f"\nCommand {i}/{len(commands)}: {command.get('raw', command)}")
            
            if self.execute_command(command):
                successful += 1
                print("✓ Success")
            else:
                failed += 1
                print("✗ Failed")
        
        print(f"\nExecution complete: {successful} successful, {failed} failed")
        return successful, failed
    
    def _execute_click(self, command: Dict) -> bool:
        """Execute a click command.
        
        Args:
            command: Click command with target information
            
        Returns:
            True if successful
        """
        target = command.get("target", "")
        
        # Try to parse position from target
        x, y = self._parse_position(target)
        
        if x is not None and y is not None:
            print(f"Clicking at position ({x}, {y})")
            pyautogui.click(x, y)
            return True
        else:
            # If no specific coordinates, try to find element by text/description
            print(f"Searching for element: {target}")
            location = self._find_element_on_screen(target)
            
            if location:
                x, y = location
                print(f"Found element at ({x}, {y}), clicking...")
                pyautogui.click(x, y)
                return True
            else:
                print(f"Could not locate element: {target}")
                return False
    
    def _execute_type(self, command: Dict) -> bool:
        """Execute a type command.
        
        Args:
            command: Type command with text to type
            
        Returns:
            True if successful
        """
        text = command.get("text", "")
        
        if not text:
            print("No text specified for typing")
            return False
        
        print(f"Typing: {text}")
        pyautogui.write(text, interval=0.05)
        return True
    
    def _execute_key(self, command: Dict) -> bool:
        """Execute a key press command.
        
        Args:
            command: Key command with key name
            
        Returns:
            True if successful
        """
        key_name = command.get("key", "").lower().strip()
        
        if not key_name:
            print("No key specified")
            return False
        
        print(f"Pressing key: {key_name}")
        
        # Check if it's a special key
        if key_name in self.key_mapping:
            key = self.key_mapping[key_name]
            self.keyboard.press(key)
            self.keyboard.release(key)
        else:
            # Regular character key
            pyautogui.press(key_name)
        
        return True
    
    def _execute_wait(self, command: Dict) -> bool:
        """Execute a wait command.
        
        Args:
            command: Wait command with duration
            
        Returns:
            True if successful
        """
        duration = command.get("duration", 1.0)
        
        print(f"Waiting for {duration} seconds")
        time.sleep(duration)
        return True
    
    def _parse_position(self, target: str) -> Tuple[Optional[int], Optional[int]]:
        """Parse position from target string.
        
        Args:
            target: String containing position information
            
        Returns:
            Tuple of (x, y) coordinates or (None, None)
        """
        # Try to find coordinate patterns like "at 100, 200" or "(100, 200)"
        import re
        
        # Pattern for "at x, y" or "(x, y)"
        pattern = r'(?:at\s+)?[\(\[]?(\d+)\s*,\s*(\d+)[\)\]]?'
        match = re.search(pattern, target)
        
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            return x, y
        
        # Try to parse position descriptions like "top left", "center", etc.
        target_lower = target.lower()
        
        x = None
        y = None
        
        # Horizontal position
        if 'left' in target_lower:
            x = int(self.screen_width * 0.25)
        elif 'right' in target_lower:
            x = int(self.screen_width * 0.75)
        elif 'center' in target_lower or 'middle' in target_lower:
            x = int(self.screen_width * 0.5)
        
        # Vertical position
        if 'top' in target_lower:
            y = int(self.screen_height * 0.25)
        elif 'bottom' in target_lower:
            y = int(self.screen_height * 0.75)
        elif 'center' in target_lower or 'middle' in target_lower:
            y = int(self.screen_height * 0.5)
        
        return x, y
    
    def _find_element_on_screen(self, description: str) -> Optional[Tuple[int, int]]:
        """Try to find an element on screen by description.
        
        Args:
            description: Text description of element
            
        Returns:
            Tuple of (x, y) if found, None otherwise
        """
        # This is a simplified implementation
        # In a real system, you might use OCR or image recognition
        
        # For now, try to locate by image text if description seems like text
        try:
            # Try to use PyAutoGUI's locateOnScreen with text
            # This would require the element to be visible and recognizable
            print(f"Visual search for '{description}' not implemented in basic version")
            return None
        except Exception as e:
            print(f"Could not find element: {e}")
            return None
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        x, y = pyautogui.position()
        return x, y
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """Move mouse to specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to take for movement
        """
        pyautogui.moveTo(x, y, duration=duration)
        print(f"Moved mouse to ({x}, {y})")


if __name__ == "__main__":
    # Example usage
    print("Initializing Device Control Executor...")
    executor = DeviceControlExecutor()
    
    # Example commands
    example_commands = [
        {"action": "wait", "duration": 1.0, "raw": "WAIT: 1.0"},
        {"action": "click", "target": "center", "raw": "CLICK: center"},
        {"action": "type", "text": "Hello, World!", "raw": "TYPE: Hello, World!"},
        {"action": "key", "key": "enter", "raw": "KEY: enter"},
    ]
    
    print("\nExecuting example commands...")
    executor.execute_commands(example_commands)
