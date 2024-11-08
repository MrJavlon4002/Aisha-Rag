from groq import Groq
from .api import groq_api_key

client = Groq(api_key = groq_api_key)


# model = "llama3-groq-8b-8192-tool-use-preview" # bad in uzbek
# model = "gemma2-9b-it" # very clear analysis but problem in gender
# model = "llama-3.2-11b-text-preview" # good in gender and normal analysis
# model = "mixtral-8x7b-32768" # bad in uzbek

def generate_text(content: str):
    completion = client.chat.completions.create(
        model = model,
        messages = [{"role": "user", "content": content}],
        temperature = 0,
        max_tokens = 200,
        stream = True,
        stop = None,
    )

    overall_text = ""
    for chunk in completion:
        overall_text += chunk.choices[0].delta.content or ""
    return overall_text.strip()
