# llama_calls/llama_service.py
from ollama import Client


def generate_ai_answer(client: Client, message: str) -> str:
    response = client.chat(
        model='llama3.1',
        messages=[
            {
                'role': 'user',
                'content': (
                    "Think of a helpful and short reply to this question. Make sure it is clear and concise. "
                    "If it is not a question, prompt for a question, or if it is an informal response, respond back nicely and humorously. "
                    "Only answer technical questions though. Thanks! 🫠\n\nQuestion: "
                    f"\n{message}"
                ),
            }
        ]
    )
    if response.get('message'):
        ollama_response = response['message'].get('content')
        formatted = bytes(ollama_response, "utf-8").decode("unicode_escape")
        return formatted
    else:
        return "No response available 🫠"
