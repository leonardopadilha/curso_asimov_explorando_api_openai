import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

pergunta = input("Pergunta: ")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Você é um engenheiro agrônomo sarcástico mas que não responde perguntas que não estejam relacionadas a frutas."},
        {"role": "user", "content": pergunta}
    ]
)

print(response.choices[0].message.content)
#print(response.choices[0].message.model_dump(exclude_none=True))