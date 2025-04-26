import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

pergunta = input("Pergunta: ")

def geracao_texto(model, mensagens, max_tokens = 1000, temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=mensagens
    )
    print(response.choices[0].message.content)
    #print(response.choices[0].message.model_dump(exclude_none=True))


messages=[
    {"role": "system", "content": "Você é um engenheiro agrônomo sarcástico mas que não responde perguntas que não estejam relacionadas a frutas."},
    {"role": "user", "content": pergunta}
]

geracao_texto("gpt-4o", messages)