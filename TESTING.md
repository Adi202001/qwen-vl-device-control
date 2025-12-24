# Testing and Validation Guide

This document describes how to test and validate the Vision-Based Device Control System.

## Pre-Installation Testing

### 1. Syntax Validation

All Python files should have valid syntax:

```bash
python -m py_compile *.py
```

Expected output: No errors

### 2. Import Structure Validation

Before installing dependencies, verify the code structure:

```bash
python -c "import ast; [ast.parse(open(f).read()) for f in ['config.py', 'vision_module.py', 'text_generation_module.py', 'device_control_executor.py', 'main.py', 'examples.py', 'utils.py']]"
```

## Post-Installation Testing

### 1. Dependency Check

Run the utility script to verify all dependencies:

```bash
python utils.py
```

This checks:
- All required packages are installed
- System information
- Model availability
- Basic device control functionality

### 2. Module-Level Testing

Test each module independently:

#### Vision Module
```bash
# This will fail if models aren't downloaded, but tests the structure
python -c "from vision_module import VisionModule; print('✓ Vision module structure is valid')"
```

#### Text Generation Module
```bash
python -c "from text_generation_module import TextGenerationModule; print('✓ Text generation module structure is valid')"
```

#### Device Control Executor
```bash
python device_control_executor.py
```

This runs a safe test sequence that demonstrates device control capabilities.

### 3. Integration Testing

#### Test 1: Help System
```bash
python main.py --help
```

Should display comprehensive help information.

#### Test 2: Manual Commands Only
```bash
python main.py --no-vision --no-text-gen
```

Tests the system without loading heavy models.

#### Test 3: Examples
```bash
python examples.py
```

Runs through various example scenarios.

## Functional Testing

### Test Case 1: Basic Command Execution

**Objective**: Verify that basic device commands work

```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

# Test commands
commands = [
    {"action": "wait", "duration": 1.0},
    {"action": "click", "target": "center"}
]

successful, failed = executor.execute_commands(commands)
assert successful == 2 and failed == 0, "Commands should execute successfully"
```

**Expected Result**: Commands execute without errors

### Test Case 2: Command Parsing

**Objective**: Verify command text parsing works correctly

```python
from text_generation_module import TextGenerationModule

# Mock test without loading model
test_response = """Commands:
CLICK: button at top right
TYPE: test input
KEY: enter
WAIT: 1.5"""

# Test parsing logic
lines = test_response.split('\n')
commands = []
for line in lines:
    if line.upper().startswith('CLICK:'):
        commands.append({'action': 'click', 'target': line[6:].strip()})
    elif line.upper().startswith('TYPE:'):
        commands.append({'action': 'type', 'text': line[5:].strip()})
    elif line.upper().startswith('KEY:'):
        commands.append({'action': 'key', 'key': line[4:].strip()})
    elif line.upper().startswith('WAIT:'):
        commands.append({'action': 'wait', 'duration': float(line[5:].strip())})

assert len(commands) == 4, "Should parse 4 commands"
assert commands[0]['action'] == 'click', "First command should be click"
assert commands[1]['text'] == 'test input', "Should parse type text correctly"
```

**Expected Result**: All commands parsed correctly

### Test Case 3: Position Parsing

**Objective**: Verify position parsing from descriptions

```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

# Test position parsing
test_cases = [
    ("center", (executor.screen_width // 2, executor.screen_height // 2)),
    ("top left", (executor.screen_width // 4, executor.screen_height // 4)),
    ("bottom right", (executor.screen_width * 3 // 4, executor.screen_height * 3 // 4))
]

for description, expected in test_cases:
    x, y = executor._parse_position(description)
    assert x is not None and y is not None, f"Should parse position from '{description}'"
    print(f"✓ Parsed '{description}' to ({x}, {y})")
```

**Expected Result**: All positions parsed correctly

### Test Case 4: Key Mapping

**Objective**: Verify special key mappings work

```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

# Test key mappings
special_keys = ['enter', 'tab', 'escape', 'backspace', 'delete']

for key in special_keys:
    assert key in executor.key_mapping, f"Key '{key}' should be mapped"
    print(f"✓ Key '{key}' is mapped")
```

**Expected Result**: All special keys are mapped

### Test Case 5: Vision Analysis (Requires Models)

**Objective**: Test vision module with a sample image

```bash
# Create a simple test image first
python -c "from PIL import Image, ImageDraw; img = Image.new('RGB', (800, 600), 'white'); draw = ImageDraw.Draw(img); draw.rectangle([100, 100, 300, 150], outline='black', fill='lightblue'); draw.text((150, 120), 'Button', fill='black'); img.save('test_image.png')"

# Analyze the test image
python main.py --analyze-image test_image.png
```

**Expected Result**: System describes the button in the image

### Test Case 6: End-to-End (Requires Models)

**Objective**: Test complete system integration

```bash
python main.py --command "analyze the screen"
```

**Expected Result**: 
1. Vision module captures screen
2. Analyzes UI elements
3. Returns description

## Safety Testing

### Test 1: Failsafe Mechanism

**Procedure**: 
1. Run a command that moves the mouse
2. Quickly move mouse to screen corner
3. Verify system stops

**Expected Result**: System aborts when mouse reaches corner

### Test 2: Invalid Command Handling

```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

# Test with invalid command
invalid_command = {"action": "invalid_action"}
result = executor.execute_command(invalid_command)

assert result == False, "Invalid commands should return False"
print("✓ Invalid commands handled correctly")
```

**Expected Result**: Invalid commands handled gracefully

### Test 3: Error Recovery

```python
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

# Test with malformed commands
commands = [
    {"action": "click", "target": ""},  # Empty target
    {"action": "type"},  # Missing text
    {"action": "key"},  # Missing key
]

for cmd in commands:
    try:
        result = executor.execute_command(cmd)
        print(f"✓ Handled malformed command: {cmd}")
    except Exception as e:
        print(f"✗ Failed to handle: {cmd}, Error: {e}")
```

**Expected Result**: All malformed commands handled without crashes

## Performance Testing

### Test 1: Model Loading Time

```python
import time

# Test vision model loading
start = time.time()
from vision_module import VisionModule
vision = VisionModule()
vision_time = time.time() - start

print(f"Vision model loaded in {vision_time:.2f} seconds")

# Test text model loading
start = time.time()
from text_generation_module import TextGenerationModule
text_gen = TextGenerationModule()
text_time = time.time() - start

print(f"Text generation model loaded in {text_time:.2f} seconds")
```

**Expected Result**: Models load within reasonable time (depends on hardware)

### Test 2: Command Execution Speed

```python
import time
from device_control_executor import DeviceControlExecutor

executor = DeviceControlExecutor()

commands = [{"action": "wait", "duration": 0.1}] * 10

start = time.time()
executor.execute_commands(commands)
elapsed = time.time() - start

print(f"10 commands executed in {elapsed:.2f} seconds")
assert elapsed < 5.0, "Commands should execute quickly"
```

**Expected Result**: Commands execute efficiently

## Validation Checklist

Before considering the system production-ready:

- [ ] All Python files have valid syntax
- [ ] All dependencies install successfully
- [ ] Vision module loads and analyzes images
- [ ] Text generation module generates valid commands
- [ ] Device executor performs actions correctly
- [ ] Main script runs in interactive mode
- [ ] Command-line arguments work as expected
- [ ] Examples run without errors
- [ ] Safety mechanisms (failsafe) work
- [ ] Error handling prevents crashes
- [ ] Documentation is clear and accurate

## Common Issues and Solutions

### Issue: Models won't download
**Solution**: Check internet connection, ensure enough disk space (10GB+)

### Issue: GPU out of memory
**Solution**: Set `VISION_MODEL_DEVICE = "cpu"` and `TEXT_MODEL_DEVICE = "cpu"` in config.py

### Issue: Commands execute on wrong elements
**Solution**: Use more specific descriptions, test with `analyze` command first

### Issue: Permissions denied (macOS)
**Solution**: Grant accessibility permissions in System Preferences > Security & Privacy

### Issue: Import errors
**Solution**: Ensure virtual environment is activated, reinstall dependencies

## Continuous Testing

When modifying the system:

1. Run syntax check: `python -m py_compile *.py`
2. Run utility diagnostics: `python utils.py`
3. Test affected modules individually
4. Run examples: `python examples.py`
5. Test in interactive mode: `python main.py`

## Reporting Issues

When reporting bugs, include:

1. Python version: `python --version`
2. Operating system
3. Output of: `python utils.py`
4. Full error traceback
5. Steps to reproduce

---

**Note**: Some tests require models to be downloaded and may take significant time and resources to run.
