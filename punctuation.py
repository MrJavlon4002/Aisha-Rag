from openai import OpenAI

OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)


def punctuations(text: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Put the punctuation into the text below and return only the text: {text}"
            }
        ]
    )
    
    return completion.choices[0].message.content
