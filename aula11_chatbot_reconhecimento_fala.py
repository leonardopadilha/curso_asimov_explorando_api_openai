# pip install --upgrade wheel

import openai
import speech_recognition as sr
from io import BytesIO
from playsound import playsound
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

recognizer = sr.Recognizer()

arquivo_audio = './arquivos/audios/audio_assistant.mp3'


def grava_audio():
  with sr.Microphone() as source:
    print("Ouvindo...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio = recognizer.listen(source)
  return audio

def transcricao_audio(audio):
  #audio = open("./arquivos/audios/audio.wav")
  wav_data = BytesIO(audio.get_wav_data())
  wav_data.name = 'audio.wav'
  transcricao = client.audio.transcriptions.create(
    model='whisper-1',
    file=wav_data
  )
  return transcricao.text

def completa_texto(mensagens):
  resposta = client.chat.completions.create(
    messages=mensagens,
    model='gpt-3.5-turbo-0125',
    max_tokens=1000,
    temperature=0
  )
  return resposta

def cria_audio(texto):
  if Path(arquivo_audio).exists():
    Path(arquivo_audio).unlink() #deletar o arquivo anterior
    
  resposta = client.audio.speech.create(
    model='tts-1',
    voice='onyx',
    input=texto
  )
  resposta.write_to_file(arquivo_audio)


def roda_audio():
  playsound(arquivo_audio)

if __name__ == '__main__':
  """
  Gravando áudio
  audio = grava_audio()
  with open('./arquivos/audios/audio.wav', 'wb') as ad:
    ad.write(audio.get_wav_data())
  """

  """
  Imprimindo uma lista com a pergunta e resposta
  mensagens = []
  audio = grava_audio()
  transcricao = transcricao_audio(audio)

  mensagens.append({'role': 'user', 'content': transcricao})
  resposta = completa_texto(mensagens)
  
  mensagens.append({'role': 'assistant', 'content': resposta.choices[0].message.content})
  print(mensagens)
  """

  mensagens = []

  while True:
    audio = grava_audio()
    transcricao = transcricao_audio(audio)

    mensagens.append({'role': 'user', 'content': transcricao})
    print(f"User: {mensagens[-1]['content']}")

    resposta = completa_texto(mensagens)
    mensagens.append({'role': 'assistant', 'content': resposta.choices[0].message.content})
    print(f"Assistant: {mensagens[-1]['content']}")
    cria_audio(mensagens[-1]["content"])
    roda_audio()