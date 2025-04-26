import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

pergunta = input("Pergunta: ")

resposta = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Você é um engenheiro agrônomo sarcástico mas que não responde perguntas que não estejam relacionadas a frutas."},
        {"role": "user", "content": pergunta}
    ],
    stream = True
)

# Exibe a mensagem conforme ela é gerada
for stream_resposta in resposta:
    texto = stream_resposta.choices[0].delta.content
    if texto:
        print(texto, end='')

#texto_completo = ""
#for chunk in resposta:
#    if chunk.choices[0].delta.content:
#        texto_completo += chunk.choices[0].delta.content
#print(texto_completo)

