import os

from ollama import Client
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

ollama_client = Client(host=OLLAMA_URL)
ollama_client.pull('llama3.1')

def get_client():
    return ollama_client