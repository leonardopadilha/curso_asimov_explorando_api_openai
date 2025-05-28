import time
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

assistant = client.beta.assistants.create(
  name='Tutor de Matemática da Asimov',
  instructions='Você é um tutor pessoal de matemática da empresa Asimov. \
    Escreva e execute códigos para responder as perguntas de matemática que lhe forem passadas.',
  tools=[{'type': 'code_interpreter'}],
  model='gpt-3.5-turbo-0125'
)

# Primeiro se cria uma thread, depois adiciona mensagem na thread e por fim, pedimos para 
# o assistant rodar essa thread.

# Criando um thread
thread = client.beta.threads.create()

# Adicionando mensagem a thread criada
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role='user',
  content='Se eu jogar um dado honesto 1000 vezes, qual é a probabilidade de eu obter exatamente 150 vezes o número 6? Resolva com um código'
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


# Analisando os passos do modelo
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

'''
for step in run_steps.data:
  print('=== Step: ', step.step_details.type)

  if step.step_details.type == 'tool_calls':
    for tool_call in step.step_details.tool_calls:
      print('------')
      print(tool_call.code_interpreter.input)
      print('------')
      print(tool_call.code_interpreter.outputs[0].logs)
'''

for step in run_steps.data[::-1]:
  print('\n=== Step: ', step.step_details.type)

  if step.step_details.type == 'tool_calls':
    for tool_call in step.step_details.tool_calls:
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
