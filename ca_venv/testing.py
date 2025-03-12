import openai
import os

# Ensure API key is set correctly


openai_client = openai.OpenAI(api_key="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")

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

print(response.choices[0].message.content)