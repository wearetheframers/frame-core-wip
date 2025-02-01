import os
from dotenv import load_dotenv
from .hosts import MEM0_SERVER_HOST

# Load environment variables from .env file
load_dotenv()

# API Keys for various services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

MEM0_API_KEY = os.getenv("MEM0_API_KEY", "")
