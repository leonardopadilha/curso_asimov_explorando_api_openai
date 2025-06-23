import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

audio = open("./arquivos/audios/fala.mp3", 'rb')
transcricao = client.audio.transcriptions.create(
  model='whisper-1',
  file=audio
  #prompt=
)

print(transcricao.text)

print()

# Formato de legenda
audio = open("./arquivos/audios/fala.mp3", 'rb')
transcricao = client.audio.transcriptions.create(
  model='whisper-1',
  file=audio,
  #prompt=,
  response_format='srt'
)

print(transcricao)

print()

audio = open("./arquivos/audios/fala.mp3", 'rb')
transcricao = client.audio.transcriptions.create(
  model='whisper-1',
  file=audio,
  response_format='text',
  language='pt'
  #prompt=
)

print(transcricao)