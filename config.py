"""Configuration settings for the vision-based device control system."""

# Vision Model Configuration
VISION_MODEL_NAME = "Qwen/Qwen-VL-Chat"  # Using Qwen-VL model
VISION_MODEL_DEVICE = "cpu"  # Change to "cuda" if GPU is available

# Text Generation Model Configuration
TEXT_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
TEXT_MODEL_DEVICE = "cpu"  # Change to "cuda" if GPU is available

# Device Control Settings
SCREENSHOT_PATH = "current_screen.png"
MAX_RETRIES = 3
ACTION_DELAY = 0.5  # Delay between actions in seconds

# Model Generation Parameters
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9
