from openai import OpenAI

# needs the OPENAI_API_KEY environment variable set 
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, world!"},
    ])

print(response.choices[0].message.content)