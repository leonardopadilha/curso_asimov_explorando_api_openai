import json
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.Client()

with open('arquivos/chatbot_respostas.json', encoding='utf-8') as f:
    json_resposta = json.load(f)

with open('arquivos/chatbot_respostas.jsonl', 'w', encoding='utf-8') as f:
    for entrada in json_resposta:
        resposta = {
            'resposta': entrada['resposta'],
            'categoria': entrada['categoria'],
            'fonte': 'AsimoBot'
        }
        entrada_jsonl = {
            'messages': [
                { 'role': 'user', 'content': entrada['pergunta'] },
                { 'role': 'assistant', 'content': json.dumps(resposta, ensure_ascii=False, indent=2) }
            ]
        }
        json.dump(entrada_jsonl, f, ensure_ascii=False)
        f.write('\n')

'''
file = client.files.create(
    file=open('arquivos/chatbot_respostas.jsonl', 'rb'),
    purpose='fine-tune'
)

client.fine_tuning.jobs.create(
    training_file=file.id,
    model='gpt-3.5-turbo'
)

client.fine_tuning.jobs.list()
'''

system_mes = '''
Responda as perguntas em um parágrafo de até 20 palavras. Categorize as respostas no seguintes conteúdos: física, matemática, língua portuguesa ou outros.
Retorne a resposta em um formato json, com as keys: 
fonte: valor deve ser sempre AsimoBot
resposta: a resposta para a pergunta
categoria: a categoria da pergunta
'''

mensagens = [
    {'role': 'system', 'content': system_mes}, # Consumo alto de tokens
    {'role': 'user', 'content': 'O que é uma equação quadrática?'}
 ]
resposta = client.chat.completions.create(
    messages=mensagens,
    model='gpt-3.5-turbo',
    max_tokens=100,
    temperature=0
)
print(resposta.choices[0].message.content)