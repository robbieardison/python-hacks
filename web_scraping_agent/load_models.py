import os
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.gemini import GeminiModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
"""openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key is None:
    raise ValueError("The OpenAI API key is not set. Please set it in the .env file.")

import openai
openai.api_key = openai_api_key
"""
#OPENAI_MODEL = OpenAIModel('gpt-4o-mini')
OLLAMA_MODEL = OllamaModel('llama3.3:70b')
#GROQ_MODEL = GroqModel('llama3-groq-8b-8192-tool-use-preview')
#GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp')