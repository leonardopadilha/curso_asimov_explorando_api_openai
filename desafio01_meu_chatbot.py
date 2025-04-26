from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

#pergunta = input("Pergunta: ")

def geracao_texto(mensagens):
  resposta = client.chat.completions.create(
    messages=mensagens,
    model="gpt-4o",
    temperature=0,
    max_tokens=1000,
    stream = True
  )

  print('Assistant: ', end='')
  texto_completo = ''
  for stream_resposta in resposta:
    texto = stream_resposta.choices[0].delta.content
    if texto:
      print(texto, end='', flush=True) # flush permite que cada fragmento de texto seja exibido assim que for recebido
      texto_completo += texto

  print()

  mensagens.append({'role': 'assistant', 'content': texto_completo})
  return mensagens

if __name__ == '__main__':

  print('Bem-vindo ao chatBot com Python da Asimov')
  mensagens = []
  while True:
    input_usuario = input('\nUser: ')
    mensagens.append({'role': 'user', 'content': input_usuario})
    mensagens = geracao_texto(mensagens)
