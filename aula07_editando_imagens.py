import requests
from PIL import Image
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

# Editando imagens
# https://ai-image-editor.netlify.app

resposta = client.images.edit(
  model='dall-e-2',
  image=open('./arquivos/images_dalle/original.png', 'rb'),
  mask=open('./arquivos/images_dalle/mask.png', 'rb'),
  prompt='Adicione uma vaca e um terneirinho na imagem fornecida',
  n=1,
  size='1024x1024'
)

# salvar imagem
nome_arquivo = f"./arquivos/images_dalle/editada.png"
image_url = resposta.data[0].url
image_data = requests.get(image_url).content
with open(nome_arquivo, 'wb') as f:
  f.write(image_data)

# Mostrando a imagem
imagem = Image.open(nome_arquivo)
imagem.show()