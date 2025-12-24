"""Main integration script for the vision-based device control system."""

import argparse
import sys
from typing import Optional
from vision_module import VisionModule
from text_generation_module import TextGenerationModule
from device_control_executor import DeviceControlExecutor


class DeviceControlSystem:
    """Integrated system combining vision, text generation, and device control."""
    
    def __init__(self, load_vision: bool = True, load_text_gen: bool = True):
        """Initialize the complete device control system.
        
        Args:
            load_vision: Whether to load vision module
            load_text_gen: Whether to load text generation module
        """
        print("=" * 60)
        print("Initializing Vision-Based Device Control System")
        print("=" * 60)
        
        self.executor = DeviceControlExecutor()
        
        self.vision = None
        if load_vision:
            try:
                print("\n[1/2] Loading Vision Module...")
                self.vision = VisionModule()
            except Exception as e:
                print(f"Warning: Could not load vision module: {e}")
                print("Continuing without vision capabilities...")
        
        self.text_gen = None
        if load_text_gen:
            try:
                print("\n[2/2] Loading Text Generation Module...")
                self.text_gen = TextGenerationModule()
            except Exception as e:
                print(f"Warning: Could not load text generation module: {e}")
                print("Continuing without text generation capabilities...")
        
        print("\n" + "=" * 60)
        print("System Initialization Complete!")
        print("=" * 60)
    
    def process_user_command(self, user_intent: str, image_path: Optional[str] = None) -> bool:
        """Process a user command from intent to execution.
        
        Args:
            user_intent: What the user wants to do
            image_path: Optional path to image, if None captures screen
            
        Returns:
            True if successful
        """
        print("\n" + "=" * 60)
        print(f"Processing Command: {user_intent}")
        print("=" * 60)
        
        # Step 1: Vision Analysis
        if self.vision is None:
            print("Error: Vision module not available")
            return False
        
        print("\n[Step 1/3] Analyzing screen/image...")
        if image_path:
            vision_output = self.vision.detect_ui_elements(image_path)
            screenshot_path = image_path
        else:
            screenshot_path, vision_output = self.vision.analyze_screen()
        
        print(f"Vision analysis complete. Image: {screenshot_path}")
        print(f"UI Description: {vision_output['raw_description'][:200]}...")
        
        # Step 2: Command Generation
        if self.text_gen is None:
            print("Error: Text generation module not available")
            return False
        
        print("\n[Step 2/3] Generating control commands...")
        commands = self.text_gen.generate_commands(vision_output, user_intent)
        
        if not commands:
            print("No commands generated. The task may not be possible with current UI.")
            return False
        
        print(f"Generated {len(commands)} commands:")
        for i, cmd in enumerate(commands, 1):
            print(f"  {i}. {cmd.get('raw', cmd)}")
        
        # Step 3: Command Execution
        print("\n[Step 3/3] Executing commands...")
        successful, failed = self.executor.execute_commands(commands)
        
        success = failed == 0 and successful > 0
        
        if success:
            print("\n✓ Command completed successfully!")
        else:
            print(f"\n✗ Command completed with {failed} failures")
        
        return success
    
    def interactive_mode(self):
        """Run the system in interactive mode."""
        print("\n" + "=" * 60)
        print("Interactive Mode - Vision-Based Device Control")
        print("=" * 60)
        print("\nCommands:")
        print("  - Type your intent (e.g., 'click the submit button')")
        print("  - Type 'analyze' to see current screen analysis")
        print("  - Type 'quit' or 'exit' to quit")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Exiting...")
                    break
                
                if user_input.lower() == 'analyze':
                    if self.vision:
                        print("\nAnalyzing current screen...")
                        screenshot_path, analysis = self.vision.analyze_screen()
                        print(f"\nScreenshot: {screenshot_path}")
                        print(f"Analysis:\n{analysis['raw_description']}")
                    else:
                        print("Vision module not available")
                    continue
                
                # Process as a command
                self.process_user_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted by user. Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
    
    def execute_manual_commands(self, commands_list: list):
        """Execute a predefined list of commands without vision/text generation.
        
        Args:
            commands_list: List of command dictionaries
        """
        print("\n" + "=" * 60)
        print("Executing Manual Commands")
        print("=" * 60)
        
        self.executor.execute_commands(commands_list)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Vision-Based Device Control System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python main.py
  
  # Execute a single command
  python main.py --command "click the search button"
  
  # Analyze an image
  python main.py --analyze-image screenshot.png
  
  # Execute without loading models (manual commands only)
  python main.py --no-vision --no-text-gen
        """
    )
    
    parser.add_argument(
        '--command', '-c',
        type=str,
        help='Execute a single command and exit'
    )
    
    parser.add_argument(
        '--image', '-i',
        type=str,
        help='Path to image to analyze (default: capture screen)'
    )
    
    parser.add_argument(
        '--analyze-image',
        type=str,
        help='Only analyze an image without executing commands'
    )
    
    parser.add_argument(
        '--no-vision',
        action='store_true',
        help='Do not load vision module'
    )
    
    parser.add_argument(
        '--no-text-gen',
        action='store_true',
        help='Do not load text generation module'
    )
    
    parser.add_argument(
        '--interactive', '-I',
        action='store_true',
        help='Run in interactive mode (default if no command specified)'
    )
    
    args = parser.parse_args()
    
    # Initialize system
    system = DeviceControlSystem(
        load_vision=not args.no_vision,
        load_text_gen=not args.no_text_gen
    )
    
    # Handle analyze-image mode
    if args.analyze_image:
        if system.vision is None:
            print("Error: Vision module required for image analysis")
            return 1
        
        print(f"\nAnalyzing image: {args.analyze_image}")
        analysis = system.vision.detect_ui_elements(args.analyze_image)
        print("\nAnalysis Results:")
        print(analysis['raw_description'])
        return 0
    
    # Handle single command mode
    if args.command:
        success = system.process_user_command(args.command, args.image)
        return 0 if success else 1
    
    # Default to interactive mode
    system.interactive_mode()
    return 0


if __name__ == "__main__":
    sys.exit(main())
