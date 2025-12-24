"""Text Generation Module using TinyLlama for command generation."""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import config
from typing import Dict, List


class TextGenerationModule:
    """Generates device control commands from vision analysis using TinyLlama."""
    
    def __init__(self, model_name: str = None, device: str = None):
        """Initialize the text generation module with TinyLlama model.
        
        Args:
            model_name: Name of the TinyLlama model to use
            device: Device to run the model on ('cpu' or 'cuda')
        """
        self.model_name = model_name or config.TEXT_MODEL_NAME
        self.device = device or config.TEXT_MODEL_DEVICE
        
        print(f"Loading text generation model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).eval()
        
        # Create text generation pipeline
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1
        )
        
        print("Text generation model loaded successfully!")
    
    def generate_commands(self, vision_output: Dict, user_intent: str) -> List[Dict]:
        """Generate device control commands based on vision output and user intent.
        
        Args:
            vision_output: Output from the vision module
            user_intent: What the user wants to do
            
        Returns:
            List of command dictionaries with action types and parameters
        """
        # Create a prompt for the model
        prompt = self._create_command_prompt(vision_output, user_intent)
        
        # Generate commands
        response = self._generate_text(prompt)
        
        # Parse the response into structured commands
        commands = self._parse_commands(response)
        
        return commands
    
    def _create_command_prompt(self, vision_output: Dict, user_intent: str) -> str:
        """Create a prompt for command generation.
        
        Args:
            vision_output: Output from vision analysis
            user_intent: User's desired action
            
        Returns:
            Formatted prompt string
        """
        ui_description = vision_output.get("raw_description", "")
        
        prompt = f"""<|system|>
You are a device control assistant. Given a description of UI elements and a user's intent, generate a sequence of device control commands.

Available commands:
- CLICK: Click on an element (requires: element_name, position)
- TYPE: Type text into a field (requires: text)
- KEY: Press a keyboard key (requires: key_name)
- WAIT: Wait for a duration (requires: seconds)

Respond with commands in this format, one per line:
CLICK: element_name at position
TYPE: text to type
KEY: key_name
WAIT: seconds

<|user|>
UI Elements: {ui_description}

User Intent: {user_intent}

Generate the commands needed to accomplish this task.
<|assistant|>
Commands:
"""
        return prompt
    
    def _generate_text(self, prompt: str) -> str:
        """Generate text using the TinyLlama model.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        outputs = self.generator(
            prompt,
            max_new_tokens=config.MAX_NEW_TOKENS,
            temperature=config.TEMPERATURE,
            top_p=config.TOP_P,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        generated_text = outputs[0]['generated_text']
        
        # Extract only the assistant's response
        if "<|assistant|>" in generated_text:
            response = generated_text.split("<|assistant|>")[-1].strip()
        else:
            response = generated_text[len(prompt):].strip()
        
        return response
    
    def _parse_commands(self, response: str) -> List[Dict]:
        """Parse the generated text into structured commands.
        
        Args:
            response: Generated command text
            
        Returns:
            List of command dictionaries
        """
        commands = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.lower().startswith("commands:"):
                continue
            
            # Parse CLICK command
            if line.upper().startswith("CLICK:"):
                parts = line[6:].strip()
                commands.append({
                    "action": "click",
                    "target": parts,
                    "raw": line
                })
            
            # Parse TYPE command
            elif line.upper().startswith("TYPE:"):
                text = line[5:].strip()
                commands.append({
                    "action": "type",
                    "text": text,
                    "raw": line
                })
            
            # Parse KEY command
            elif line.upper().startswith("KEY:"):
                key = line[4:].strip()
                commands.append({
                    "action": "key",
                    "key": key,
                    "raw": line
                })
            
            # Parse WAIT command
            elif line.upper().startswith("WAIT:"):
                try:
                    seconds = float(line[5:].strip())
                    commands.append({
                        "action": "wait",
                        "duration": seconds,
                        "raw": line
                    })
                except ValueError:
                    print(f"Warning: Could not parse wait duration from: {line}")
        
        return commands
    
    def interpret_user_query(self, query: str, vision_output: Dict) -> str:
        """Interpret and clarify user's intent based on available UI elements.
        
        Args:
            query: User's query or command
            vision_output: Current screen analysis
            
        Returns:
            Clarified intent or confirmation
        """
        ui_description = vision_output.get("raw_description", "")
        
        prompt = f"""<|system|>
You are a helpful assistant that interprets user requests for UI automation.
<|user|>
Available UI elements: {ui_description}

User request: {query}

Is this request possible with the available UI? If yes, rephrase it as a clear action. If no, explain why.
<|assistant|>
"""
        
        response = self._generate_text(prompt)
        return response


if __name__ == "__main__":
    # Example usage
    print("Initializing Text Generation Module...")
    text_gen = TextGenerationModule()
    
    # Example vision output
    example_vision_output = {
        "raw_description": "The screen shows a web browser with a search bar at the top, "
                          "a submit button on the right, and several menu items.",
        "image_path": "example.png"
    }
    
    # Example user intent
    user_intent = "Search for 'machine learning tutorials'"
    
    print(f"\nGenerating commands for: {user_intent}")
    commands = text_gen.generate_commands(example_vision_output, user_intent)
    
    print("\nGenerated Commands:")
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")
