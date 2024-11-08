from openai import OpenAI
from .api import novita_api_key

client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key=novita_api_key,
)
max_tokens = 512
stream = True

model_type = "meta-llama/llama-3.1-70b-instruct"
model_type = "google/gemma-2-9b-it"

def generate_text(content: str):
    messages = [
        {"role": "user", "content": content}
    ]
    
    response = client.chat.completions.create(
        model=model_type,
        messages=messages,
        max_tokens=max_tokens,
        stream=stream
    )

    if stream:
        return ''.join(chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
    else:
        return response.choices[0].message.content
