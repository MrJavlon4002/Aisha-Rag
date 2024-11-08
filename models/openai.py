from openai import OpenAI

from .api import openai_api_key

model_type = "gpt-4o"

client = OpenAI(
    api_key = openai_api_key,
)

max_tokens = 512
stream = False

def generate_text(content: str):
    messages = [{"role": "user", "content": content}]
    response = client.chat.completions.create(model=model_type, messages=messages, max_tokens=max_tokens, stream=stream)
    return response.choices[0].message.content if not stream else ''.join(chunk.choices[0].delta.content for chunk in response)