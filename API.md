# API Reference

Complete API documentation for all modules in the Vision-Based Device Control System.

## Table of Contents

1. [Vision Module](#vision-module)
2. [Text Generation Module](#text-generation-module)
3. [Device Control Executor](#device-control-executor)
4. [Main System](#main-system)
5. [Utilities](#utilities)
6. [Configuration](#configuration)

---

## Vision Module

### `VisionModule`

Main class for vision-based screen and image understanding.

#### Constructor

```python
VisionModule(model_name: str = None, device: str = None)
```

**Parameters:**
- `model_name` (str, optional): Hugging Face model identifier. Defaults to `config.VISION_MODEL_NAME`
- `device` (str, optional): Device to run model on ('cpu' or 'cuda'). Defaults to `config.VISION_MODEL_DEVICE`

**Example:**
```python
from vision_module import VisionModule

# Default configuration
vision = VisionModule()

# Custom configuration
vision = VisionModule(model_name="Qwen/Qwen-VL-Chat", device="cuda")
```

#### Methods

##### `capture_screenshot(save_path: str = None) -> str`

Captures current screen and saves it.

**Parameters:**
- `save_path` (str, optional): Path to save screenshot. Defaults to `config.SCREENSHOT_PATH`

**Returns:**
- str: Path to saved screenshot

**Example:**
```python
path = vision.capture_screenshot("my_screen.png")
```

##### `analyze_image(image_path: str, query: str = None) -> str`

Analyzes an image and returns description.

**Parameters:**
- `image_path` (str): Path to image file
- `query` (str, optional): Custom query about the image

**Returns:**
- str: Natural language description of the image

**Example:**
```python
description = vision.analyze_image("screenshot.png", "What buttons are visible?")
```

##### `detect_ui_elements(image_path: str) -> Dict[str, any]`

Detects UI elements in an image.

**Parameters:**
- `image_path` (str): Path to image file

**Returns:**
- dict: Dictionary containing:
  - `raw_description` (str): Description of UI elements
  - `image_path` (str): Path to analyzed image

**Example:**
```python
result = vision.detect_ui_elements("screenshot.png")
print(result["raw_description"])
```

##### `locate_element(image_path: str, element_description: str) -> str`

Locates a specific element in the image.

**Parameters:**
- `image_path` (str): Path to image file
- `element_description` (str): Description of element to find

**Returns:**
- str: Location information

**Example:**
```python
location = vision.locate_element("screenshot.png", "submit button")
```

##### `analyze_screen(custom_query: str = None) -> Tuple[str, Dict]`

Captures and analyzes current screen.

**Parameters:**
- `custom_query` (str, optional): Custom query about screen

**Returns:**
- tuple: (screenshot_path, analysis_dict)

**Example:**
```python
path, analysis = vision.analyze_screen("List all clickable elements")
```

---

## Text Generation Module

### `TextGenerationModule`

Generates device control commands from vision output and user intent.

#### Constructor

```python
TextGenerationModule(model_name: str = None, device: str = None)
```

**Parameters:**
- `model_name` (str, optional): Hugging Face model identifier. Defaults to `config.TEXT_MODEL_NAME`
- `device` (str, optional): Device to run model on. Defaults to `config.TEXT_MODEL_DEVICE`

**Example:**
```python
from text_generation_module import TextGenerationModule

text_gen = TextGenerationModule()
```

#### Methods

##### `generate_commands(vision_output: Dict, user_intent: str) -> List[Dict]`

Generates command sequence from vision analysis and user intent.

**Parameters:**
- `vision_output` (dict): Output from vision module
- `user_intent` (str): What user wants to accomplish

**Returns:**
- list: List of command dictionaries

**Example:**
```python
vision_output = {"raw_description": "Search bar at top, submit button on right"}
user_intent = "Search for machine learning"

commands = text_gen.generate_commands(vision_output, user_intent)
```

##### `interpret_user_query(query: str, vision_output: Dict) -> str`

Interprets and clarifies user intent.

**Parameters:**
- `query` (str): User's query
- `vision_output` (dict): Current UI state

**Returns:**
- str: Clarified intent or feasibility assessment

**Example:**
```python
clarification = text_gen.interpret_user_query("click the button", vision_output)
```

---

## Device Control Executor

### `DeviceControlExecutor`

Executes device control commands.

#### Constructor

```python
DeviceControlExecutor()
```

**Example:**
```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()
```

#### Methods

##### `execute_command(command: Dict) -> bool`

Executes a single device control command.

**Parameters:**
- `command` (dict): Command dictionary with action and parameters

**Returns:**
- bool: True if successful, False otherwise

**Command Format:**
```python
# Click command
{"action": "click", "target": "center", "raw": "CLICK: center"}

# Type command
{"action": "type", "text": "Hello", "raw": "TYPE: Hello"}

# Key command
{"action": "key", "key": "enter", "raw": "KEY: enter"}

# Wait command
{"action": "wait", "duration": 1.0, "raw": "WAIT: 1.0"}
```

**Example:**
```python
command = {"action": "click", "target": "center"}
success = executor.execute_command(command)
```

##### `execute_commands(commands: List[Dict]) -> Tuple[int, int]`

Executes a sequence of commands.

**Parameters:**
- `commands` (list): List of command dictionaries

**Returns:**
- tuple: (successful_count, failed_count)

**Example:**
```python
commands = [
    {"action": "click", "target": "search bar"},
    {"action": "type", "text": "test"},
    {"action": "key", "key": "enter"}
]
successful, failed = executor.execute_commands(commands)
```

##### `get_mouse_position() -> Tuple[int, int]`

Gets current mouse position.

**Returns:**
- tuple: (x, y) coordinates

**Example:**
```python
x, y = executor.get_mouse_position()
```

##### `move_mouse(x: int, y: int, duration: float = 0.5)`

Moves mouse to specified position.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `duration` (float): Time to take for movement

**Example:**
```python
executor.move_mouse(500, 300, duration=1.0)
```

---

## Main System

### `DeviceControlSystem`

Integrated system combining all modules.

#### Constructor

```python
DeviceControlSystem(load_vision: bool = True, load_text_gen: bool = True)
```

**Parameters:**
- `load_vision` (bool): Whether to load vision module
- `load_text_gen` (bool): Whether to load text generation module

**Example:**
```python
from main import DeviceControlSystem

# Full system
system = DeviceControlSystem()

# Executor only
system = DeviceControlSystem(load_vision=False, load_text_gen=False)
```

#### Methods

##### `process_user_command(user_intent: str, image_path: str = None) -> bool`

Processes user command through complete pipeline.

**Parameters:**
- `user_intent` (str): What user wants to do
- `image_path` (str, optional): Image to analyze, if None captures screen

**Returns:**
- bool: True if successful

**Example:**
```python
success = system.process_user_command("Click the submit button")
```

##### `interactive_mode()`

Runs system in interactive mode.

**Example:**
```python
system.interactive_mode()
```

##### `execute_manual_commands(commands_list: list)`

Executes predefined commands without vision/text generation.

**Parameters:**
- `commands_list` (list): List of command dictionaries

**Example:**
```python
commands = [{"action": "click", "target": "center"}]
system.execute_manual_commands(commands)
```

---

## Utilities

### Functions in `utils.py`

#### `check_dependencies() -> bool`

Checks if all required packages are installed.

**Returns:**
- bool: True if all dependencies present

**Example:**
```python
from utils import check_dependencies

if check_dependencies():
    print("Ready to go!")
```

#### `check_models() -> bool`

Checks if models are downloaded.

**Returns:**
- bool: True if all models available

**Example:**
```python
from utils import check_models

check_models()
```

#### `get_system_info()`

Prints system information.

**Example:**
```python
from utils import get_system_info

get_system_info()
```

#### `save_commands_to_file(commands: List[Dict], filename: str)`

Saves commands to JSON file.

**Parameters:**
- `commands` (list): Command list
- `filename` (str): Output file

**Example:**
```python
from utils import save_commands_to_file

commands = [{"action": "click", "target": "center"}]
save_commands_to_file(commands, "my_commands.json")
```

#### `load_commands_from_file(filename: str) -> List[Dict]`

Loads commands from JSON file.

**Parameters:**
- `filename` (str): Input file

**Returns:**
- list: Command list

**Example:**
```python
from utils import load_commands_from_file

commands = load_commands_from_file("my_commands.json")
```

---

## Configuration

### Variables in `config.py`

#### Model Configuration

```python
VISION_MODEL_NAME = "Qwen/Qwen-VL-Chat"
TEXT_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

VISION_MODEL_DEVICE = "cpu"  # or "cuda"
TEXT_MODEL_DEVICE = "cpu"    # or "cuda"
```

#### Execution Settings

```python
SCREENSHOT_PATH = "current_screen.png"
MAX_RETRIES = 3
ACTION_DELAY = 0.5  # seconds
```

#### Model Parameters

```python
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9
```

**Usage:**
```python
import config

# Modify at runtime
config.ACTION_DELAY = 1.0
config.TEMPERATURE = 0.5
```

---

## Command Specifications

### Command Types

#### CLICK Command

```python
{
    "action": "click",
    "target": str,  # Element description or coordinates
    "raw": str      # Original command text
}
```

**Target formats:**
- Coordinates: `"at 100, 200"` or `"(100, 200)"`
- Position: `"center"`, `"top left"`, `"bottom right"`
- Description: `"submit button"`, `"search bar"`

#### TYPE Command

```python
{
    "action": "type",
    "text": str,   # Text to type
    "raw": str     # Original command text
}
```

#### KEY Command

```python
{
    "action": "key",
    "key": str,    # Key name
    "raw": str     # Original command text
}
```

**Supported keys:**
- Basic: `enter`, `tab`, `space`, `backspace`, `delete`, `escape`
- Modifiers: `shift`, `ctrl`, `alt`, `cmd`
- Arrows: `up`, `down`, `left`, `right`
- Navigation: `home`, `end`, `pageup`, `pagedown`

#### WAIT Command

```python
{
    "action": "wait",
    "duration": float,  # Seconds to wait
    "raw": str          # Original command text
}
```

---

## Error Handling

### Common Exceptions

#### Vision Module
- `ModelNotFoundError`: Model not available
- `ImageAnalysisError`: Failed to analyze image
- `ScreenshotError`: Failed to capture screen

#### Text Generation Module
- `ModelNotFoundError`: Model not available
- `GenerationError`: Failed to generate text
- `ParseError`: Failed to parse commands

#### Device Control Executor
- `InvalidCommandError`: Unknown command type
- `ExecutionError`: Failed to execute command
- `PositionError`: Invalid position specification

### Error Handling Pattern

```python
try:
    system = DeviceControlSystem()
    system.process_user_command("click button")
except Exception as e:
    print(f"Error: {e}")
    # Handle gracefully
```

---

## Best Practices

### 1. Resource Management

```python
# Load models once, reuse
system = DeviceControlSystem()
system.process_user_command("command 1")
system.process_user_command("command 2")
# Models stay loaded
```

### 2. Error Handling

```python
success = executor.execute_command(command)
if not success:
    # Handle failure
    pass
```

### 3. Batch Processing

```python
commands = [cmd1, cmd2, cmd3]
successful, failed = executor.execute_commands(commands)
```

### 4. Custom Configurations

```python
# Create custom config
my_config = {
    "vision_model": "custom/model",
    "device": "cuda"
}

vision = VisionModule(
    model_name=my_config["vision_model"],
    device=my_config["device"]
)
```

---

## Version Information

Current API Version: 1.0.0

Last Updated: 2024

For updates and issues, visit: https://github.com/Adi202001/qwen-vl-device-control
