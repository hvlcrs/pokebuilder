
import os
import ollama

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from google import genai

# Load environment variables from .env file
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path, override=True)

# Initialize OpenAI client
openai_client = OpenAI()

# Initialize Gemini client
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def emb_openai(text):
    return (
        openai_client.embeddings.create(input=text, model="text-embedding-3-small")
        .data[0]
        .embedding
    )

# Function to get the embedding of a text
def emb_gemini(text):
    return (
        gemini_client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text).embeddings[0].values
    )

def emb_ollama(text):
    return (
        ollama.embed(model="nomic-embed-text", input=text).embeddings[0]
    )