# Quick Start Guide

This guide will help you get started with the Vision-Based Device Control System quickly.

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will take some time as it downloads PyTorch and other libraries.

### 2. Verify Installation

```bash
python utils.py
```

This will check:
- ✓ All dependencies are installed
- ✓ System information
- ✓ Basic device control functionality

## First Run

### Option 1: Interactive Mode (Recommended for first-time users)

```bash
python main.py
```

This launches an interactive session where you can:
- Type commands in natural language
- Type `analyze` to see what's on screen
- Type `quit` to exit

**Example session:**
```
> analyze
[Shows current screen analysis]

> click the center of the screen
[Executes the command]

> quit
```

### Option 2: Single Command

```bash
python main.py --command "click the center of screen"
```

### Option 3: Run Examples

```bash
python examples.py
```

This demonstrates various capabilities without requiring models to be loaded.

## Understanding the System

### The Three Stages

Every command goes through three stages:

1. **Vision Analysis** 🔍
   - Captures/analyzes screen or image
   - Detects UI elements
   - Understands layout

2. **Command Generation** 🤖
   - Processes vision output
   - Generates action sequence
   - Plans steps to achieve goal

3. **Execution** ⚡
   - Executes mouse clicks
   - Types text
   - Presses keys

### Basic Commands

The system understands natural language but generates structured commands:

| Command Type | Example | What it does |
|--------------|---------|--------------|
| CLICK | `CLICK: button at center` | Clicks mouse at location |
| TYPE | `TYPE: hello world` | Types the text |
| KEY | `KEY: enter` | Presses a key |
| WAIT | `WAIT: 2.0` | Waits 2 seconds |

## Common Use Cases

### 1. Automate Form Filling

```bash
python main.py --command "fill in the name field with John Doe"
```

### 2. Navigate Applications

```bash
python main.py --command "click on the File menu and select Save"
```

### 3. Analyze UI

```bash
python main.py --analyze-image screenshot.png
```

This just analyzes without executing any actions.

## Tips for Success

### 1. Start Simple
Begin with basic commands like "click center" before complex workflows.

### 2. Test Safely
- Close important applications before testing
- Use test applications or documents
- Remember the failsafe: move mouse to corner to abort

### 3. Be Specific
Instead of: "click the button"
Use: "click the submit button in the bottom right"

### 4. Check Vision Output
Use `analyze` command first to see what the system can detect:
```
> analyze
```

### 5. Iterative Approach
Break complex tasks into smaller steps:
```
> click the search bar
> type machine learning
> press enter
```

## Configuration

Edit `config.py` to customize:

```python
# Use GPU if available (much faster!)
VISION_MODEL_DEVICE = "cuda"  # Change from "cpu" to "cuda"
TEXT_MODEL_DEVICE = "cuda"

# Adjust timing
ACTION_DELAY = 0.5  # Seconds between actions

# Model parameters
TEMPERATURE = 0.7  # Lower = more deterministic
```

## Troubleshooting

### Models Not Loading

**Issue**: First run takes very long
**Solution**: Models are downloading (5-10 GB total). Wait for completion.

### Commands Not Working

**Issue**: Click not working on correct element
**Solution**: 
1. Use `analyze` to see what the system detects
2. Be more specific in descriptions
3. Try using relative positions (top, bottom, left, right, center)

### Mouse/Keyboard Not Responding

**Issue**: No mouse movement or typing
**Solution**: 
1. Check permissions (macOS requires accessibility permissions)
2. Verify `pyautogui` works: `python -c "import pyautogui; print(pyautogui.position())"`

### Out of Memory

**Issue**: System crashes with memory error
**Solution**: 
1. Use CPU instead of GPU in config.py (slower but uses less RAM)
2. Close other applications
3. Process one command at a time

## Safety Tips

⚠️ **Important Safety Information**

1. **Failsafe**: Move mouse to screen corner to stop all actions
2. **Test Environment**: Always test in safe environment first
3. **Supervision**: Monitor the system during operation
4. **Start Slow**: Use `ACTION_DELAY` setting to slow down for observation
5. **Backup**: Keep backups of important data when testing

## Next Steps

Once comfortable with basics:

1. **Explore Examples**: Run `python examples.py` to see more use cases
2. **Read Full README**: Check README.md for complete documentation
3. **Customize**: Edit modules for your specific needs
4. **Create Scripts**: Build automation scripts for repetitive tasks

## Getting Help

- Check README.md for detailed documentation
- Run `python main.py --help` for all command-line options
- Run `python utils.py` for system diagnostics
- Open an issue on GitHub for bugs or questions

## Quick Reference

```bash
# Interactive mode
python main.py

# Single command
python main.py -c "your command here"

# Analyze image
python main.py --analyze-image screenshot.png

# Run examples
python examples.py

# System check
python utils.py

# Help
python main.py --help
```

---

**Ready to start?** Run `python main.py` and type `analyze` to see what the system can detect on your current screen!
