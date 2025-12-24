"""Vision Module using Qwen-VL for screen and image understanding."""

import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import config
import pyautogui
from typing import Dict, Optional, Tuple


class VisionModule:
    """Handles vision-based screen understanding using Qwen-VL model."""
    
    def __init__(self, model_name: str = None, device: str = None):
        """Initialize the vision module with Qwen-VL model.
        
        Args:
            model_name: Name of the Qwen-VL model to use
            device: Device to run the model on ('cpu' or 'cuda')
        """
        self.model_name = model_name or config.VISION_MODEL_NAME
        self.device = device or config.VISION_MODEL_DEVICE
        
        print(f"Loading vision model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device,
            trust_remote_code=True,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).eval()
        
        print("Vision model loaded successfully!")
    
    def capture_screenshot(self, save_path: str = None) -> str:
        """Capture current screen and save it.
        
        Args:
            save_path: Path to save the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        save_path = save_path or config.SCREENSHOT_PATH
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        print(f"Screenshot saved to: {save_path}")
        return save_path
    
    def analyze_image(self, image_path: str, query: str = None) -> str:
        """Analyze an image and extract UI information.
        
        Args:
            image_path: Path to the image to analyze
            query: Optional query about the image
            
        Returns:
            Description of the UI elements and layout
        """
        default_query = (
            "Describe all visible UI elements in this image including buttons, "
            "text fields, menus, icons, and their positions. Be specific about "
            "what actions are available."
        )
        query = query or default_query
        
        # Prepare the input in Qwen-VL format
        query_text = f"<img>{image_path}</img>{query}"
        
        # Tokenize and generate
        inputs = self.tokenizer(query_text, return_tensors='pt')
        inputs = inputs.to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=config.MAX_NEW_TOKENS,
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the response after the query
        if query in response:
            response = response.split(query)[-1].strip()
        
        return response
    
    def detect_ui_elements(self, image_path: str) -> Dict[str, any]:
        """Detect specific UI elements like buttons, text fields, etc.
        
        Args:
            image_path: Path to the image to analyze
            
        Returns:
            Dictionary containing detected UI elements
        """
        query = (
            "List all interactive UI elements in this image. "
            "For each element, specify: type (button, text field, menu, etc.), "
            "label or text, and approximate position (top, bottom, left, right, center)."
        )
        
        response = self.analyze_image(image_path, query)
        
        return {
            "raw_description": response,
            "image_path": image_path
        }
    
    def locate_element(self, image_path: str, element_description: str) -> str:
        """Find a specific UI element in the image.
        
        Args:
            image_path: Path to the image
            element_description: Description of the element to find
            
        Returns:
            Information about the element's location
        """
        query = (
            f"Where is the {element_description} located in this image? "
            "Provide its position (top, middle, bottom and left, center, right)."
        )
        
        response = self.analyze_image(image_path, query)
        return response
    
    def analyze_screen(self, custom_query: str = None) -> Tuple[str, Dict]:
        """Capture and analyze the current screen.
        
        Args:
            custom_query: Optional custom query about the screen
            
        Returns:
            Tuple of (screenshot_path, analysis_results)
        """
        screenshot_path = self.capture_screenshot()
        
        if custom_query:
            analysis = self.analyze_image(screenshot_path, custom_query)
            results = {"raw_description": analysis, "image_path": screenshot_path}
        else:
            results = self.detect_ui_elements(screenshot_path)
        
        return screenshot_path, results


if __name__ == "__main__":
    # Example usage
    print("Initializing Vision Module...")
    vision = VisionModule()
    
    # Capture and analyze current screen
    print("\nAnalyzing current screen...")
    screenshot_path, analysis = vision.analyze_screen()
    
    print("\nScreen Analysis Results:")
    print(analysis["raw_description"])
