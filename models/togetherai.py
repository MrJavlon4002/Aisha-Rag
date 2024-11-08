from together import Together
from .api import together_api_key

client = Together(api_key=together_api_key)

# model_type = "Qwen/Qwen2.5-72B-Instruct-Turbo" # bad in Uzbek
model_type = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO" # bad in uzbek

def generate_text(content: str):
    messages = [{"role": "user", "content": content}]
    response = client.chat.completions.create(
            model=model_type,
            messages=messages
        )
    return response.choices[0].message.content