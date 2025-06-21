import time
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

# print(dir(client.beta))

# print(openai.__version__)

vector_store = client.beta.vector_stores.create(name= 'Apostilas Asimov Aula 06')

files = ['./arquivos/Explorando a API da OpenAI.pdf',
          './arquivos/Explorando o Universo das IAs com Hugging Face.pdf']

file_stream = [open(f, 'rb') for f in files]

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id,
  files=file_stream
)

#print(file_batch.status)
#print(file_batch.file_counts)


assistant = client.beta.assistants.create(
  name='Tutor Asimov',
  instructions='Você é um tutor de uma escola de programação. Você é ótimo para responder \
    perguntas teóricas sobre a api da OpenAI e sobre a utilização da biblioteca do Hugging \
      Face com Python. Você utiliza as apostilas do curso para basear suas respostas. Caso \
        você não encontre as respostas nas apostilas informadas, você fala que não sabe \
        responder.',
  tools=[{'type': 'file_search'}],
  tool_resources={'file_search': {'vector_store_ids': [vector_store.id]}},
  model='gpt-4o-mini'
)

# Primeiro se cria uma thread, depois adiciona mensagem na thread e por fim, pedimos para 
# o assistant rodar essa thread.

# Criando um thread
thread = client.beta.threads.create()

# Adicionando mensagem a thread criada
mensagem_texto = "Segundo o documento fornecido, o que é o Hugging Face?"
mensagem_texto = "Segundo o documento fornecido, como utilizar assistants com python?"
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role='user',
  content=mensagem_texto
)

# Executando a thread no assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions='O nome do usuário é Leonardo e ele deseja ser um usuário premium.'
)

while run.status in ['queued', 'in_progress', 'cancelling']:
  time.sleep(1)
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

if run.status == 'completed':
  mensagens = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(mensagens.data[0].content[0].text.value)

else:
  print('Erro!!!', run.status)

mensagens = client.beta.threads.messages.list(
  thread_id=thread.id
)
mensagem = list(mensagens)[0].content[0].text
print()
anotacoes = mensagem.annotations
citacoes = []
for index, anotacao in enumerate(anotacoes):
  mensagem.value = mensagem.value.replace(anotacao.text, f"[{index}]")
  if file_cit := getattr(anotacao, 'file_citation', None):
    file = client.files.retrieve(file_cit.file_id)
    citacoes.append(f"[{index}] {file.filename}")
citacoes = "\n".join(citacoes)
mensagem.value = f"{mensagem.value}\n\n{citacoes}"
print(mensagem.value)

"""
# Analisando os passos do modelo
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

for step in run_steps.data[::-1]:
  print('\n=== Step: ', step.step_details.type)

  if step.step_details.type == 'tool_calls':
    for tool_call in step.step_details.tool_calls:
      if tool_call.type == 'file_search':
        print(tool_call)
      else:
        print('------')
        print(tool_call.code_interpreter.input)
        print('------')
        print('Result')
        if tool_call.code_interpreter.outputs:
          print(tool_call.code_interpreter.outputs[0].logs)

  if step.step_details.type == 'message_creation':
    message = client.beta.threads.messages.retrieve(
      thread_id=thread.id,
      message_id=step.step_details.message_creation.message_id
    )
    print(message.content[0].text.value)
"""
