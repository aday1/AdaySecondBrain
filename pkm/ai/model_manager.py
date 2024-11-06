import json
import requests
from pathlib import Path

class OllamaManager:
    def __init__(self, config_path="config/ollama_config.json"):
        self.config = self._load_config(config_path)
        self.base_url = "http://localhost:11434"
        
    def _load_config(self, config_path):
        with open(config_path) as f:
            return json.load(f)
    
    def get_available_models(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            return response.json()["models"]
        except:
            return []
            
    def generate_response(self, prompt, model="mistral"):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt}
            )
            return response.json()["response"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
