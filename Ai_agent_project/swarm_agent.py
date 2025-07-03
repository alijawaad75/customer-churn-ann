from typing import List
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class SwarmAgent:
    def __init__(
        self,
        model_name: str = "gpt2",
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """
        Initialize the Swarm AI agent.
        
        Args:
            model_name (str): Name of the model to use
            device (str): Device to run the model on (cuda/cpu)
        """
        self.device = device
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.initialize_model()

    def initialize_model(self):
        """Initialize the model and tokenizer."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.model.to(self.device)
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            raise

    def process_input(self, input_text: str) -> str:
        """
        Process input text and generate a response.
        
        Args:
            input_text (str): Input text to process            
        Returns:
            str: Generated response
        """
        try:
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt"
            ).to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=100,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            return response
        except Exception as e:
            print(f"Error processing input: {str(e)}")
            return "Error processing input"

    def swarm_process(self, inputs: List[str]) -> List[str]:
        """
        Process multiple inputs in parallel (swarm processing).
        
        Args:
            inputs (List[str]): List of input texts to process
            
        Returns:
            List[str]: List of generated responses
        """
        return [self.process_input(input_text) for input_text in inputs]

    def update_model(self, new_model_name: str):
        """
        Update the model to a different one.
        
        Args:
            new_model_name (str): Name of the new model to use
        """
        self.model_name = new_model_name
        self.initialize_model() 