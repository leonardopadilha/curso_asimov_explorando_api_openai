import time
import openai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()
# dataset = pd.read_csv('./arquivos/supermarket_sales.csv')
# print(dataset.head(5))

file = client.files.create(
  file=open('./arquivos/supermarket_sales.csv', 'rb'),
  purpose='assistants'
)

assistant = client.beta.assistants.create(
  name='Analista financeiro',
  instructions='Você é um analista financeiro de um supermercado. Você deve utilizar os dados \
    .csv informados relativos as vendas do supermercado para realizar as suas análises.',
  tools=[{'type': 'code_interpreter'}],
  tool_resources={'code_interpreter': {'file_ids': [file.id]}},
  model='gpt-4o-mini'
)

thread = client.beta.threads.create()

texto_mensagem = 'Qual é o rating médio das vendas do supermercado?'
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role='user',
  content=texto_mensagem
)

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

print()
print()
print()

# Analisando os passos do modelo
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

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
