"""
LLM generator for response
"""

class Generator:
    def __init__(self, model_name="gpt-3.5-turbo", api_key=None):
        """Initialize generator"""
        self.model_name = model_name
        self.api_key = api_key
    
    def generate(self, prompt):
        """Generate response"""
        pass
    
    def generate_stream(self, prompt):
        """Generate response with streaming"""
        pass

if __name__ == "__main__":
    pass
