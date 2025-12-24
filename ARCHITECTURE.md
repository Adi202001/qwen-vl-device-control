# System Architecture

This document provides detailed technical information about the Vision-Based Device Control System architecture.

## Overview

The system implements a three-stage pipeline for vision-based device automation:

1. **Vision Understanding** - Analyzes visual input to understand UI elements
2. **Command Generation** - Translates visual understanding and user intent into actions
3. **Device Control** - Executes the generated actions on the device

## Component Architecture

### 1. Vision Module (`vision_module.py`)

#### Purpose
Captures and analyzes screen content or images to understand UI elements and layout.

#### Key Components

**VisionModule Class**
- Loads and manages Qwen-VL-Chat model
- Handles screenshot capture via PyAutoGUI
- Performs image analysis with vision-language model

**Methods:**
- `capture_screenshot()` - Captures current screen
- `analyze_image()` - Analyzes image with custom query
- `detect_ui_elements()` - Identifies UI components
- `locate_element()` - Finds specific element by description
- `analyze_screen()` - Complete screen capture and analysis

#### Technical Details

**Model**: Qwen/Qwen-VL-Chat
- Vision-Language Model (VLM)
- Can process both images and text
- Trained on UI understanding tasks
- Outputs natural language descriptions

**Input Format**:
```python
query_text = f"<img>{image_path}</img>{query}"
```

**Output**: Natural language description of UI elements

#### Data Flow
```
Screen/Image → PyAutoGUI Capture → PIL Image → Qwen-VL Model → Text Description
```

### 2. Text Generation Module (`text_generation_module.py`)

#### Purpose
Converts vision analysis and user intent into structured device control commands.

#### Key Components

**TextGenerationModule Class**
- Manages TinyLlama language model
- Creates prompts for command generation
- Parses model output into structured commands

**Methods:**
- `generate_commands()` - Main command generation
- `_create_command_prompt()` - Formats prompt for LLM
- `_generate_text()` - Calls LLM for text generation
- `_parse_commands()` - Parses text into command objects
- `interpret_user_query()` - Clarifies user intent

#### Technical Details

**Model**: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Small but capable language model
- Chat-optimized for following instructions
- Fast inference on CPU/GPU

**Prompt Structure**:
```
<|system|>
You are a device control assistant...

<|user|>
UI Elements: {description}
User Intent: {intent}

<|assistant|>
Commands:
```

**Command Format**:
```
CLICK: element_name at position
TYPE: text to type
KEY: key_name
WAIT: seconds
```

#### Data Flow
```
Vision Output + User Intent → Prompt Creation → LLM → Text Response → Command Parser → Structured Commands
```

### 3. Device Control Executor (`device_control_executor.py`)

#### Purpose
Executes device control commands to interact with the operating system and applications.

#### Key Components

**DeviceControlExecutor Class**
- Manages mouse and keyboard control
- Parses position descriptions
- Executes command sequences

**Methods:**
- `execute_command()` - Execute single command
- `execute_commands()` - Execute command sequence
- `_execute_click()` - Mouse click
- `_execute_type()` - Keyboard typing
- `_execute_key()` - Key press
- `_execute_wait()` - Delay
- `_parse_position()` - Convert description to coordinates
- `move_mouse()` - Mouse movement

#### Technical Details

**Libraries Used**:
- **PyAutoGUI**: Cross-platform GUI automation
- **pynput**: Keyboard and mouse control

**Position Parsing**:
- Coordinates: `(x, y)` or `at x, y`
- Relative: `top`, `bottom`, `left`, `right`, `center`
- Combined: `top left`, `bottom right`

**Safety Features**:
- Failsafe: Move mouse to corner to abort
- Configurable delays between actions
- Error handling for failed operations

#### Data Flow
```
Command Object → Action Parser → Device API (PyAutoGUI/pynput) → OS → Application
```

### 4. Main Integration (`main.py`)

#### Purpose
Orchestrates all modules and provides user interface.

#### Key Components

**DeviceControlSystem Class**
- Initializes all modules
- Manages the complete pipeline
- Provides interactive and command-line interfaces

**Methods:**
- `process_user_command()` - End-to-end command processing
- `interactive_mode()` - Interactive shell
- `execute_manual_commands()` - Direct command execution

#### Operation Modes

**1. Interactive Mode**
```
User Input → Vision Analysis → Command Generation → Execution → User
```

**2. Single Command Mode**
```
Command Line Args → Vision Analysis → Command Generation → Execution → Exit
```

**3. Analysis Only Mode**
```
Image Path → Vision Analysis → Display Results → Exit
```

## Data Flow Diagrams

### Complete Pipeline

```
┌─────────────┐
│ User Intent │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Capture Screen  │
└──────┬──────────┘
       │
       ▼
┌─────────────────────────┐
│ Vision Analysis (Qwen)  │
│ Output: UI Description  │
└──────┬──────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Command Generation (TinyLlama)│
│ Output: Structured Commands   │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────┐
│ Parse Commands       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Execute Commands     │
│ (PyAutoGUI/pynput)   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Device Actions       │
└──────────────────────┘
```

### Command Object Structure

```python
{
    "action": "click" | "type" | "key" | "wait",
    
    # For click:
    "target": "description or coordinates",
    
    # For type:
    "text": "string to type",
    
    # For key:
    "key": "key name",
    
    # For wait:
    "duration": float,
    
    # All:
    "raw": "original command string"
}
```

## Configuration System

### Configuration File (`config.py`)

Centralizes all system parameters:

```python
# Model Selection
VISION_MODEL_NAME = "Qwen/Qwen-VL-Chat"
TEXT_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Device Placement
VISION_MODEL_DEVICE = "cpu"  # or "cuda"
TEXT_MODEL_DEVICE = "cpu"    # or "cuda"

# Execution Parameters
ACTION_DELAY = 0.5  # seconds between actions
MAX_RETRIES = 3

# Model Parameters
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9
```

## Error Handling Strategy

### Vision Module
- Model loading failures → Graceful degradation
- Screenshot failures → Retry mechanism
- Analysis errors → Return empty description

### Text Generation Module
- Model loading failures → Graceful degradation
- Generation failures → Return empty command list
- Parse errors → Skip malformed commands

### Device Control Executor
- Invalid actions → Log and continue
- Position parsing failures → Try alternative methods
- Execution failures → Report and mark as failed

## Performance Considerations

### Memory Usage
- **Vision Model**: ~3-4 GB RAM/VRAM
- **Text Model**: ~2-3 GB RAM/VRAM
- **Total System**: ~6-8 GB minimum

### Inference Speed (CPU)
- Vision Analysis: ~5-10 seconds
- Command Generation: ~2-5 seconds
- Command Execution: <1 second per action

### Inference Speed (GPU - CUDA)
- Vision Analysis: ~1-2 seconds
- Command Generation: ~0.5-1 second
- Command Execution: <1 second per action

## Extension Points

### Adding New Command Types

1. Update `TextGenerationModule._parse_commands()`:
```python
elif line.upper().startswith("NEWCOMMAND:"):
    commands.append({"action": "newcommand", ...})
```

2. Update `DeviceControlExecutor.execute_command()`:
```python
elif action == "newcommand":
    return self._execute_newcommand(command)
```

3. Implement the execution method:
```python
def _execute_newcommand(self, command: Dict) -> bool:
    # Implementation
    pass
```

### Using Different Models

Edit `config.py`:
```python
VISION_MODEL_NAME = "your/vision-model"
TEXT_MODEL_NAME = "your/text-model"
```

Ensure the models are compatible with Hugging Face transformers library.

### Adding New Analysis Types

Extend `VisionModule` class:
```python
def custom_analysis(self, image_path: str) -> Dict:
    query = "Your custom query"
    response = self.analyze_image(image_path, query)
    return {"custom_result": response}
```

## Security Considerations

### Input Validation
- Sanitize user commands before processing
- Validate file paths for image analysis
- Check command parameters before execution

### Safety Mechanisms
- PyAutoGUI failsafe (move mouse to corner)
- Configurable delays to prevent runaway automation
- Error handling to prevent system instability

### Privacy
- Screenshots contain sensitive information
- Store temporarily, clean up after use
- Don't log sensitive user input

## Testing Architecture

### Unit Tests
- Test individual module methods
- Mock heavy dependencies (models)
- Verify command parsing logic

### Integration Tests
- Test module interactions
- Verify data flow between components
- Test complete pipeline

### System Tests
- End-to-end functionality
- Performance benchmarks
- Safety mechanism validation

## Future Architecture Improvements

1. **Model Optimization**
   - Quantization for faster inference
   - Model distillation for smaller size
   - Caching for repeated analyses

2. **Enhanced Vision**
   - OCR integration for text detection
   - Object detection for precise localization
   - Multi-modal fusion for better understanding

3. **Smarter Commands**
   - Learning from user corrections
   - Context-aware command generation
   - Multi-step planning

4. **Better Execution**
   - Visual feedback during execution
   - Undo/redo functionality
   - Recording and replay of sequences

5. **Platform Support**
   - Mobile device control (Android/iOS)
   - Web browser automation
   - API-based application control

---

This architecture provides a solid foundation for vision-based device automation while remaining extensible and maintainable.
