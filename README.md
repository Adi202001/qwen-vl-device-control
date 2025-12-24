# Vision-Based Device Control System

A complete AI-powered device automation system that combines computer vision, natural language processing, and device control to automate user interactions with applications and UI elements.

## 🏗️ Architecture

The system consists of three main modules working together:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Intent / Command                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Vision Module (Qwen-VL-1B)                              │
│  - Captures and analyzes screen/images                       │
│  - Detects UI elements (buttons, text fields, menus)        │
│  - Understands layout and visual context                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Text Generation Module (TinyLlama-1.1B)                 │
│  - Processes vision output and user intent                   │
│  - Generates structured control commands                     │
│  - Plans action sequences (click, type, key press)          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Device Control Executor                                  │
│  - Executes generated commands                               │
│  - Performs mouse clicks, keyboard typing, key presses      │
│  - Provides feedback on execution status                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Components

### 1. Vision Module (`vision_module.py`)
- **Model**: Qwen-VL-Chat (Vision-Language Model)
- **Capabilities**:
  - Screen capture and analysis
  - UI element detection (buttons, text fields, menus, icons)
  - Layout understanding and element positioning
  - Natural language descriptions of visual content
  - Element location queries

### 2. Text Generation Module (`text_generation_module.py`)
- **Model**: TinyLlama-1.1B-Chat
- **Capabilities**:
  - Converts vision analysis into actionable commands
  - Generates command sequences from user intent
  - Supports multiple command types: CLICK, TYPE, KEY, WAIT
  - Parses natural language into structured actions

### 3. Device Control Executor (`device_control_executor.py`)
- **Technologies**: PyAutoGUI, pynput
- **Capabilities**:
  - Mouse control (click, move)
  - Keyboard control (typing, special keys)
  - Position parsing (coordinates, relative positions)
  - Command sequence execution
  - Error handling and retry logic

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Adi202001/qwen-vl-device-control.git
cd qwen-vl-device-control
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: First run will download the required models (Qwen-VL and TinyLlama), which may take some time depending on your internet connection.

### GPU Support (Optional)
For better performance, install PyTorch with CUDA support:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Then update `config.py` to use GPU:
```python
VISION_MODEL_DEVICE = "cuda"
TEXT_MODEL_DEVICE = "cuda"
```

## 🚀 Usage

### Interactive Mode

Run the system in interactive mode to process commands in real-time:

```bash
python main.py
```

In interactive mode:
- Type your intent (e.g., "click the submit button")
- Type `analyze` to see current screen analysis
- Type `quit` to exit

### Single Command Execution

Execute a single command and exit:

```bash
python main.py --command "click the search button and type 'hello world'"
```

### Analyze an Image

Analyze a specific image without executing commands:

```bash
python main.py --analyze-image screenshot.png
```

### Command-Line Options

```
usage: main.py [-h] [--command COMMAND] [--image IMAGE]
               [--analyze-image ANALYZE_IMAGE] [--no-vision] [--no-text-gen]
               [--interactive]

Vision-Based Device Control System

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND, -c COMMAND
                        Execute a single command and exit
  --image IMAGE, -i IMAGE
                        Path to image to analyze (default: capture screen)
  --analyze-image ANALYZE_IMAGE
                        Only analyze an image without executing commands
  --no-vision           Do not load vision module
  --no-text-gen         Do not load text generation module
  --interactive, -I     Run in interactive mode (default if no command
                        specified)
```

## 📚 Examples

### Example 1: Basic Commands

```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

commands = [
    {"action": "click", "target": "center", "raw": "CLICK: center"},
    {"action": "type", "text": "Hello World!", "raw": "TYPE: Hello World!"},
    {"action": "key", "key": "enter", "raw": "KEY: enter"}
]

executor.execute_commands(commands)
```

### Example 2: Complete System Integration

```python
from main import DeviceControlSystem

system = DeviceControlSystem()
system.process_user_command("Find the search button and click it")
```

### Example 3: Running Examples

Run the included examples:

```bash
python examples.py
```

## 🎯 Supported Commands

The text generation module generates commands in the following formats:

| Command | Format | Description |
|---------|--------|-------------|
| CLICK | `CLICK: element_name at position` | Click on a UI element |
| TYPE | `TYPE: text to type` | Type text into active field |
| KEY | `KEY: key_name` | Press a keyboard key |
| WAIT | `WAIT: seconds` | Wait for specified duration |

### Supported Keys

- Basic: `enter`, `tab`, `space`, `backspace`, `delete`, `escape`
- Modifiers: `shift`, `ctrl`, `alt`, `cmd`
- Arrows: `up`, `down`, `left`, `right`
- Navigation: `home`, `end`, `pageup`, `pagedown`

## ⚙️ Configuration

Edit `config.py` to customize system behavior:

```python
# Vision Model Configuration
VISION_MODEL_NAME = "Qwen/Qwen-VL-Chat"
VISION_MODEL_DEVICE = "cpu"  # or "cuda"

# Text Generation Model Configuration
TEXT_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
TEXT_MODEL_DEVICE = "cpu"  # or "cuda"

# Device Control Settings
SCREENSHOT_PATH = "current_screen.png"
MAX_RETRIES = 3
ACTION_DELAY = 0.5  # seconds

# Model Generation Parameters
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9
```

## 🔐 Safety Features

- **PyAutoGUI Failsafe**: Move mouse to corner of screen to abort
- **Action Delay**: Configurable delay between actions
- **Error Handling**: Graceful failure handling with detailed error messages
- **Command Validation**: Validates commands before execution

## 🛠️ Development

### Project Structure

```
qwen-vl-device-control/
├── config.py                      # Configuration settings
├── vision_module.py               # Vision analysis using Qwen-VL
├── text_generation_module.py     # Command generation using TinyLlama
├── device_control_executor.py    # Device control execution
├── main.py                        # Main integration script
├── examples.py                    # Usage examples
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

### Running Individual Modules

Each module can be run independently for testing:

```bash
# Test vision module
python vision_module.py

# Test text generation module
python text_generation_module.py

# Test device control executor
python device_control_executor.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This system can control your mouse and keyboard. Use with caution and always test in a safe environment first. The authors are not responsible for any unintended actions performed by the system.

## 🔮 Future Enhancements

- [ ] Add OCR for better text element detection
- [ ] Implement computer vision for more accurate element localization
- [ ] Add support for multi-monitor setups
- [ ] Create a GUI interface for easier control
- [ ] Add recording and playback of action sequences
- [ ] Implement error recovery and retry mechanisms
- [ ] Add support for mobile device control (Android/iOS)
- [ ] Create browser extension for web automation

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.