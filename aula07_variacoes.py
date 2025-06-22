import requests
from PIL import Image
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()


resposta = client.images.create_variation(
  model='dall-e-2',
  image=open('./arquivos/images_dalle/original.png', 'rb'),
  n=1,
  size='1024x1024'
)

# salvar imagem
nome_arquivo = f"./arquivos/images_dalle/variacao.png"
image_url = resposta.data[0].url
image_data = requests.get(image_url).content
with open(nome_arquivo, 'wb') as f:
  f.write(image_data)

# Mostrando a imagem
imagem = Image.open(nome_arquivo)
imagem.show()