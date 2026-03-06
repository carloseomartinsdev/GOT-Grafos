import pandas as pd
import json
import requests

print("="*60)
print("IDENTIFICADOR DE PERSONAGENS - GoT (API Gratuita)")
print("="*60)

# Carrega dataset
df = pd.read_csv('dataset_personagens.csv')
exclude = ['CUT TO', 'INT', 'EXT', 'MAN', 'WOMAN', 'ALL', 'MEN', 'WOMEN', 'CROWD']
df_filtered = df[~df['personagem'].isin(exclude)]
personagens = df_filtered['personagem'].tolist()

print(f"\nTotal de personagens: {len(personagens)}")
print("\nEscolha a API:")
print("1 - OpenRouter (gratuito com modelos limitados)")
print("2 - Groq (gratuito, requer cadastro)")
print("3 - Pular e usar dicionário manual")

opcao = input("\nOpção (1-3): ").strip()

if opcao == '3':
    print("\nExecute: python criar_dicionario_manual.py")
    exit()

# Monta prompt
prompt = f"""Analise esta lista de personagens de Game of Thrones e retorne 3 informações para cada um:
1. Nome principal completo
2. Variações/apelidos (separados por vírgula)
3. Família ou grupo

Personagens: {', '.join(personagens[:50])}

Retorne APENAS um JSON válido:
{{
  "personagens": [
    {{"nome": "NOME", "variacoes": "VAR1,VAR2", "familia": "FAMILIA"}}
  ]
}}"""

if opcao == '1':
    api_key = input("\nAPI Key OpenRouter (https://openrouter.ai/keys): ")
    url = 'https://openrouter.ai/api/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'google/gemini-2.0-flash-exp:free',
        'messages': [{'role': 'user', 'content': prompt}]
    }
elif opcao == '2':
    api_key = input("\nAPI Key Groq (https://console.groq.com/keys): ")
    url = 'https://api.groq.com/openai/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.1
    }

print("\nEnviando requisição...")
response = requests.post(url, headers=headers, json=payload, timeout=120)

if response.status_code == 200:
    result = response.json()['choices'][0]['message']['content']
    
    # Extrai JSON
    if '```json' in result:
        start = result.find('```json') + 7
        end = result.find('```', start)
        json_str = result[start:end].strip()
    else:
        start = result.find('{')
        end = result.rfind('}') + 1
        json_str = result[start:end]
    
    dicionario = json.loads(json_str)
    
    # Salva CSV
    with open('personagens_dicionario.csv', 'w', encoding='utf-8') as f:
        f.write('Nome,Variações,Familia\n')
        for item in dicionario['personagens']:
            f.write(f'"{item["nome"]}","{item["variacoes"]}","{item["familia"]}"\n')
    
    print(f"\n✓ Dicionário criado: personagens_dicionario.csv")
else:
    print(f"\n[ERRO] Status: {response.status_code}")
    print(response.text)
