import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

arquivo = './arquivos/audios/fala.mp3'

texto = """
Python é uma linguagem de programação interpretada, de alto nível e de propósito geral. 
Foi criada por Guido van Rossum no final da década de 1980, sendo a primeira versão lançada em 1991. 
É conhecida por sua sintaxe simples e clara, que facilita a leitura e escrita de código, e por ser 
uma linguagem versátil, é usada em diversas áreas como desenvolvimento web, ciência de dados, inteligência 
artificial, entre outras. 
"""

resposta = client.audio.speech.create(
  model='tts-1',
  voice='echo',
  input=texto
)

resposta.write_to_file(arquivo)


"""
# Salvando no arquivo na medida em que a voz é gerada
arquivo = './arquivos/audios/fala.mp3'

with client.audio.speech.with_streaming_response.create(
  model='tts-1',
  voice='echo',
  input=texto
) as resposta:
  resposta.stream_to_file(arquivo)
"""