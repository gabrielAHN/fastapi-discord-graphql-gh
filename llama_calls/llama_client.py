import os
import asyncio
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

ollama_client = Client(host=OLLAMA_URL)

def get_client():
    return ollama_client