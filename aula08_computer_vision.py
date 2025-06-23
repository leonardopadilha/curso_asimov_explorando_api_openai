import base64
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

'''
resposta = client.chat.completions.create(
  model='gpt-4o-mini',
  messages=[{
    'role': 'user',
    'content': [
      { 'type': 'text', 'text': 'Descreva a imagem fornecida' },
      { 'type': 'image_url', 'image_url': { 'url': 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Spain%E2%80%99s_chilly_blanket_ESA22415247.jpeg'}}
    ]
  }]
)

print(resposta.choices[0].message.content)
print()
'''

def encode_image(caminho_imagem):
  with open(caminho_imagem, 'rb') as img:
    return base64.b64encode(img.read()).decode('utf-8')
  

# Formatos aceitos: ['png', 'jpeg', 'gif', 'webp']
caminho = "./arquivos/images_dalle/original.png"
base64_image = encode_image(caminho)

resposta = client.chat.completions.create(
  model='gpt-4o-mini',
  messages=[{
    'role': 'user',
    'content': [
      { 'type': 'text', 'text': 'Descreva a imagem fornecida' },
      { 'type': 'image_url', 'image_url': { 'url': f"data:image/jpeg;base64,{base64_image}"}}
    ]
  }],
  max_tokens=1000
)

print(resposta.choices[0].message.content)
