from openai import OpenAI


client = OpenAI()

SYSTEM_PROMPT = (
    "You are a acting as Prateek a 35 year old male living in the us and are a software engineer."
    "You love watching thrillers and action movies."
    # need to add 50-100 examples of my personal convo to make it more personalized.
)

response1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can You tell me a joke?"},
    ],
)

print(response1.choices[0].message.content)

# 