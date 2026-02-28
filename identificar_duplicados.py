import pandas as pd
import json
import requests

print("="*60)
print("IDENTIFICADOR DE PERSONAGENS DUPLICADOS - GoT")
print("="*60)

# Carrega dataset
print("\n[1/5] Carregando dataset...")
df = pd.read_csv('dataset_personagens.csv')
print(f"   Total de personagens no dataset: {len(df)}")

# Filtra personagens relevantes
print("\n[2/5] Filtrando personagens...")
exclude = ['CUT TO', 'INT', 'EXT', 'MAN', 'WOMAN', 'ALL', 'MEN', 'WOMEN', 'CROWD']
df_filtered = df[~df['personagem'].isin(exclude)]
personagens = df_filtered['personagem'].tolist()
print(f"   Personagens filtrados: {len(personagens)}")
print(f"   Enviando todos para análise")

# Monta prompt
print("\n[3/5] Montando prompt para DeepSeek...")
prompt = f"""Analise esta lista de personagens de Game of Thrones e retorne 3 informações para cada um:
1. Nome principal completo
2. Variações/apelidos (separados por vírgula)
3. Família ou grupo (ex: Stark, Lannister, Night's Watch, Targaryen, etc)

Personagens: {', '.join(personagens)}

Retorne APENAS um JSON válido no formato:
{{
  "personagens": [
    {{
      "nome": "NOME_PRINCIPAL",
      "variacoes": "APELIDO1, APELIDO2",
      "familia": "FAMILIA_OU_GRUPO"
    }}
  ]
}}

Exemplos:
- JON SNOW: variações="JON", familia="Stark/Night's Watch"
- TYRION LANNISTER: variações="TYRION", familia="Lannister"
- SANDOR CLEGANE: variações="THE HOUND, HOUND", familia="Clegane"

Retorne apenas o JSON, sem explicações."""
print(f"   Prompt criado ({len(prompt)} caracteres)")

# Chama DeepSeek API
print("\n[4/5] Chamando DeepSeek API...")
api_key = input("   Cole sua API key do DeepSeek: ")
print("   Enviando requisição...")

try:
    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.1,
            'max_tokens': 8000
        },
        timeout=120
    )
except Exception as e:
    print(f"\n[ERRO] Falha na requisição: {e}")
    input("\nPressione Enter para sair...")
    exit()

if response.status_code == 200:
    print("   Resposta recebida com sucesso!")
    
    print("\n[5/5] Processando resposta...")
    try:
        result = response.json()['choices'][0]['message']['content']
        print(f"   Resposta: {len(result)} caracteres")
        
        # Extrai JSON da resposta
        print("   Extraindo JSON...")
        
        # Salva resposta bruta para debug
        with open('resposta_deepseek.txt', 'w', encoding='utf-8') as f:
            f.write(result)
        print("   Resposta salva em: resposta_deepseek.txt")
        
        # Tenta encontrar JSON com marcadores de código
        if '```json' in result:
            start = result.find('```json') + 7
            end = result.find('```', start)
            json_str = result[start:end].strip()
        elif '```' in result:
            start = result.find('```') + 3
            end = result.find('```', start)
            json_str = result[start:end].strip()
        else:
            start = result.find('{')
            end = result.rfind('}') + 1
            if start == -1 or end == 0:
                print(f"\n[ERRO] Não foi possível encontrar JSON na resposta")
                print(f"Primeiros 500 caracteres:\n{result[:500]}")
                input("\nPressione Enter para sair...")
                exit()
            json_str = result[start:end]
        
        print("   Parseando JSON...")
        dicionario = json.loads(json_str)
    except Exception as e:
        print(f"\n[ERRO] Falha ao processar resposta: {e}")
        print(f"Resposta da API:\n{response.text}")
        input("\nPressione Enter para sair...")
        exit()
    
    # Pergunta formato de saída
    print("\n   Escolha o formato de saída:")
    print("   1 - JSON (.json)")
    print("   2 - JavaScript (.js)")
    print("   3 - CSV (.csv)")
    formato = input("   Opção (1-3): ").strip()
    
    # Salva
    print("   Salvando arquivo...")
    if formato == '2':
        filename = 'personagens_dicionario.js'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('const personagensDicionario = ')
            json.dump(dicionario, f, ensure_ascii=False, indent=2)
            f.write(';')
    elif formato == '3':
        filename = 'personagens_dicionario.csv'
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write('Nome,Variações,Familia\n')
            for item in dicionario['personagens']:
                f.write(f'"{item["nome"]}","{item["variacoes"]}","{item["familia"]}"\n')
    else:
        filename = 'personagens_dicionario.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dicionario, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("CONCLUÍDO!")
    print(f"Dicionário criado com {len(dicionario)} entradas principais")
    print(f"Salvo em: {filename}")
    print("="*60)
else:
    print(f"\n[ERRO] Status: {response.status_code}")
    print(response.text)

input("\nPressione Enter para sair...")
