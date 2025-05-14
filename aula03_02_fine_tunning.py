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

mensagens = [
    {'role': 'user', 'content': 'O que é uma equação quadrática?'}
 ]
resposta = client.chat.completions.create(
    messages=mensagens,
    model='ft:gpt-3.5-turbo-0125:student::BWqc9Brg', #modelo gerado pela openai no fine_tunning
    max_tokens=100,
    temperature=0
)
print(resposta.choices[0].message.content)