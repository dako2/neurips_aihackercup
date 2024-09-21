import os
from anthropic import Anthropic
import openai
import google.generativeai as genai
from dotenv import load_dotenv
import ollama

# Load environment variables from .env file
load_dotenv()

class LLM:
    def __init__(self, model_name="anthropic") -> None:
        self.prompt = ""
        self.response = ""
        self.model_name = model_name.lower()  # Normalize model name to lower case

        # Initialize the respective model client based on model_name
        self.anthro_client = None
        self.gemini_model = None
        self.openai_client_initialized = False

        self.client = None

        if self.model_name == "anthropic":
            self.initialize_anthropic()
        elif self.model_name == "openai":
            self.initialize_openai()
        elif self.model_name == "gemini":
            self.initialize_gemini()
        elif self.model_name == "codegemma" or "llama3.1":
            self.initialize_ollama(self.model_name)
        else:
            raise ValueError(f"Model '{self.model_name}' is not supported.")

    def __list__(self):
        return ['gemini','anthropic', 'openai', 'codegemma', 'llama3.1',]

    def initialize_ollama(self, model_name):
        # Prepare the messages for the model
        messages = [
            {
                'role': 'user',
                'content': ''
            }
        ]
        ollama.chat(model=model_name, messages=messages)
  
    def ollama(self, prompt):
        # Prepare the messages for the model
        messages = [
            {
                'role': 'user',
                'content': prompt
            }
        ]
        self.response = ollama.chat(model=self.model_name, messages=messages)
        return self.response['message']['content']

    def initialize_anthropic(self):
        """Initialize the Anthropic (Claude) client."""
        ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        if not ANTHROPIC_API_KEY:
            raise RuntimeError("Anthropic API key not found in environment variables.")
        self.anthro_client = Anthropic(api_key=ANTHROPIC_API_KEY)

    def initialize_openai(self):
        """Initialize the OpenAI client."""
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise RuntimeError("OpenAI API key not found in environment variables.")
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI()
        self.openai_client_initialized = True

    def openai(self, prompt):
        """Call the OpenAI (GPT-4) model using the new ChatCompletion API."""
        if not self.openai_client_initialized:
            raise RuntimeError("OpenAI client is not initialized.")
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            #max_tokens=1024
        )        
        # Extract the response content
        self.response = response.choices[0].message.content.strip()
        return self.response
 
    def initialize_gemini(self):
        """Initialize the Gemini client."""
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise RuntimeError("Gemini API key not found in environment variables.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    def anthropic(self, prompt):
        """Call the Anthropic (Claude) model."""
        if not self.anthro_client:
            raise RuntimeError("Anthropic client is not initialized.")
        
        message = self.anthro_client.completions.create(
            #max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-opus-20240229",
        )
        self.response = message['completion']
        return self.response

    def gemini(self, prompt):
        """Call the Gemini model."""
        if not self.gemini_model:
            raise RuntimeError("Gemini model is not initialized.")
        
        response = self.gemini_model.generate_content(prompt)
        if response:
            self.response = response.text
        else:
            self.response = "No response received from Gemini."
        return self.response
 
    def run(self, prompt):
        """Run the selected model."""
        if self.model_name == "anthropic":
            return self.anthropic(prompt)
        elif self.model_name == "gemini":
            return self.gemini(prompt)
        elif self.model_name == "openai":
            return self.openai(prompt)
        elif self.model_name == "codegemma" or "llama3.1":
            return self.ollama(prompt)
        else:
            return "Model not supported. Please choose from 'anthropic', 'gemini', or 'openai'."

# Example usage
if __name__ == "__main__":
    
    llm = LLM(model_name="llama3.1")
    prompt = "what day is it today?"
    response = llm.run(prompt)
    print(response)
