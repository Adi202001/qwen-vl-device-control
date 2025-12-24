"""Example usage scripts for the device control system."""

from device_control_executor import DeviceControlExecutor
import time


def example_basic_commands():
    """Example: Execute basic device control commands."""
    print("=" * 60)
    print("Example 1: Basic Device Commands")
    print("=" * 60)
    
    executor = DeviceControlExecutor()
    
    # Define some basic commands
    commands = [
        {
            "action": "wait",
            "duration": 1.0,
            "raw": "WAIT: 1.0 seconds before starting"
        },
        {
            "action": "click",
            "target": "center of screen",
            "raw": "CLICK: center of screen"
        },
        {
            "action": "type",
            "text": "Hello from device control!",
            "raw": "TYPE: Hello from device control!"
        },
        {
            "action": "key",
            "key": "enter",
            "raw": "KEY: enter"
        }
    ]
    
    executor.execute_commands(commands)


def example_web_search():
    """Example: Simulated web search workflow."""
    print("\n" + "=" * 60)
    print("Example 2: Web Search Workflow")
    print("=" * 60)
    print("Note: This simulates a web search. Adjust coordinates for your screen.")
    
    executor = DeviceControlExecutor()
    
    # Workflow for opening browser and searching
    commands = [
        {
            "action": "wait",
            "duration": 1.0,
            "raw": "WAIT: 1 second"
        },
        {
            "action": "key",
            "key": "cmd",  # or "ctrl" on Windows/Linux
            "raw": "KEY: cmd (open spotlight/search)"
        },
        {
            "action": "type",
            "text": "browser",
            "raw": "TYPE: browser"
        },
        {
            "action": "key",
            "key": "enter",
            "raw": "KEY: enter"
        },
        {
            "action": "wait",
            "duration": 2.0,
            "raw": "WAIT: 2 seconds for browser to open"
        },
        {
            "action": "type",
            "text": "machine learning tutorial",
            "raw": "TYPE: machine learning tutorial"
        },
        {
            "action": "key",
            "key": "enter",
            "raw": "KEY: enter to search"
        }
    ]
    
    print("This example demonstrates a web search workflow.")
    print("Commands would be executed in sequence.")
    print("\nCommands to execute:")
    for i, cmd in enumerate(commands, 1):
        print(f"  {i}. {cmd['raw']}")


def example_form_filling():
    """Example: Fill out a form."""
    print("\n" + "=" * 60)
    print("Example 3: Form Filling Workflow")
    print("=" * 60)
    
    executor = DeviceControlExecutor()
    
    # Simulate filling a form
    commands = [
        {
            "action": "click",
            "target": "name field at top left",
            "raw": "CLICK: name field"
        },
        {
            "action": "type",
            "text": "John Doe",
            "raw": "TYPE: John Doe"
        },
        {
            "action": "key",
            "key": "tab",
            "raw": "KEY: tab to next field"
        },
        {
            "action": "type",
            "text": "john.doe@example.com",
            "raw": "TYPE: john.doe@example.com"
        },
        {
            "action": "key",
            "key": "tab",
            "raw": "KEY: tab to next field"
        },
        {
            "action": "type",
            "text": "This is a test message",
            "raw": "TYPE: This is a test message"
        },
        {
            "action": "click",
            "target": "submit button at bottom",
            "raw": "CLICK: submit button"
        }
    ]
    
    print("This example demonstrates form filling.")
    print("\nCommands to execute:")
    for i, cmd in enumerate(commands, 1):
        print(f"  {i}. {cmd['raw']}")


def example_with_vision_and_llm():
    """Example: Complete system with vision and LLM (requires models loaded)."""
    print("\n" + "=" * 60)
    print("Example 4: Complete System Integration")
    print("=" * 60)
    print("This example uses vision analysis and LLM command generation.")
    print("Note: Requires models to be downloaded and loaded.")
    
    try:
        from main import DeviceControlSystem
        
        # Initialize the complete system
        system = DeviceControlSystem(load_vision=True, load_text_gen=True)
        
        # Example commands
        example_intents = [
            "Analyze the current screen",
            "Click on the search bar and type 'hello world'",
            "Find and click the submit button"
        ]
        
        print("\nExample intents that can be processed:")
        for i, intent in enumerate(example_intents, 1):
            print(f"  {i}. {intent}")
        
        print("\nTo run these, use: python main.py -c '<intent>'")
        
    except Exception as e:
        print(f"Could not load complete system: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")


def example_mouse_control():
    """Example: Mouse movement and clicking."""
    print("\n" + "=" * 60)
    print("Example 5: Mouse Control")
    print("=" * 60)
    
    executor = DeviceControlExecutor()
    
    # Get current position
    x, y = executor.get_mouse_position()
    print(f"Current mouse position: ({x}, {y})")
    
    # Move mouse to different positions
    print("\nMoving mouse to screen center...")
    center_x = executor.screen_width // 2
    center_y = executor.screen_height // 2
    executor.move_mouse(center_x, center_y, duration=1.0)
    
    print("Mouse control example complete.")


if __name__ == "__main__":
    print("Vision-Based Device Control System - Examples")
    print("=" * 60)
    print("\nThese examples demonstrate different capabilities:")
    print()
    
    # Run examples
    try:
        example_basic_commands()
        time.sleep(1)
        
        example_web_search()
        time.sleep(1)
        
        example_form_filling()
        time.sleep(1)
        
        example_mouse_control()
        time.sleep(1)
        
        example_with_vision_and_llm()
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
