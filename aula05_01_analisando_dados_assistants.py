import pandas as pd

dataset = pd.read_csv('./arquivos/supermarket_sales.csv')
dataset.head(5)

dataset['Rating'].mean()

import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

file = client.files.create(
    file=open('./arquivos/supermarket_sales.csv', 'rb'),
    purpose='assistants'
)

assitant = client.beta.assistants.create(
    name="Analista Fianceiro",
    instructions='Você é um analista financeiro de um supermercado. Você deve utilizar os dados \
        .csv informados relativos as vendas do supermercado para realizar as suas análises.',
    tools=[{'type': 'code_interpreter'}],
    tool_resources={'code_interpreter': {'file_ids': [file.id]}},
    model='gpt-4o-mini'
)

thread = client.beta.threads.create()

texto_mensagem = 'Qual é o raqting médio das vendas do supermercado? O arquivo estáno formato csv.'
texto_mensagem = 'Gere um gráfico de pizza com o percentual de vendas por meio de pagamento. O arquivo está no formato csv.'

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content=texto_mensagem
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assitant.id,
    instructions='O nome do usuário é Adriano Soares e ele é um usuário Premium.'
)

import time

while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

run.status

if run.status == 'completed':
    mensagens = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(mensagens)
else:
    print('Errro', run.status)


print(mensagens.data[0].content[0])

run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

for step in run_steps.data[::-1]:
    print('\n=== Step:', step.step_details.type)
    if step.step_details.type == 'tool_calls':
        for tool_call in step.step_details.tool_calls:
            print('-----')
            print(tool_call.code_interpreter.input)
            print('-----')
            print('Result')

            # Para debugar os outputs
            # print(tool_call.code_interpreter.outputs)

            # if tool_call.code_interpreter.outputs[0].type == 'logs':
            if tool_call.code_interpreter.outputs and tool_call.code_interpreter.outputs[0].type == 'logs':
                print(tool_call.code_interpreter.outputs[0].logs)
    if step.step_details.type == 'message_creation':
        message = client.beta.threads.messages.retrieve(
            thread_id=thread.id,
            message_id=step.step_details.message_creation.message_id
        )
        if message.content[0].type == 'text':
            print(message.content[0].text.value)
        
        if message.content[0].type == 'image_file':
            file_id = message.content[0].image_file.file_id
            image_data = client.files.content(file_id)
            with open(f'arquivos/{file_id}.png', 'wb') as f:
                f.write(image_data.read())
                print(f'Imagem {file_id} salva')
            
            import matplotlib.pyplot as plt
            import matplotlib.image as mpimg

            img = mpimg.imread(f'./arquivos/{file_id}.png')
            fig, ax = plt.subplots()
            ax.set_axis_off()
            ax.imshow(img)
            plt.show()
