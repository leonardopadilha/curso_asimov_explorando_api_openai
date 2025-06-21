import requests
from PIL import Image
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

nome = 'senhoras_bosque'
modelo='dall-e-3',
prompt='Crie uma imagem de duas senhoras conversando em um bosque amplo com árvores floridas',
qualidade='hd',
style='natural',

resposta = client.images.generate(
  model='dall-e-3',
  prompt='Crie uma imagem de duas senhoras conversando em um bosque amplo com árvores floridas',
  size='1024x1024',
  quality='hd',
  style='natural',
  n=1
)

# Realizando o processo de melhoria automática do prompt
#print(resposta.data[0].revised_prompt)

# url onde está a imagem
#print(resposta.data[0].url)

# salvar imagem
nome_arquivo = f"./arquivos/images_dalle/{nome}_{modelo}_{qualidade}_{style}.jpg"
image_url = resposta.data[0].url
image_data = requests.get(image_url).content
with open(nome_arquivo, 'wb') as f:
  f.write(image_data)

# Mostrando a imagem
imagem = Image.open(nome_arquivo)
imagem.show()