import os
import json
import requests
import pandas as pd
import re

def dividir_script_por_cenas(script):
    """Divide script em blocos de até 3000 caracteres por cena"""
    cenas = re.split(r'\n-{3,}\n|\n\[', script)
    blocos = []
    bloco_atual = ""
    
    for i, cena in enumerate(cenas):
        if i > 0 and not cena.startswith('['):
            cena = '[' + cena
        
        if len(bloco_atual) + len(cena) > 3000 and bloco_atual:
            blocos.append(bloco_atual)
            bloco_atual = cena
        else:
            bloco_atual += cena
    
    if bloco_atual:
        blocos.append(bloco_atual)
    
    return blocos

def processar_bloco_deepseek(bloco, api_key, num_bloco):
    prompt = f"""Analise este trecho de script de Game of Thrones e retorne JSON com interações.

Script:
{bloco}

Para cada interação:
- cena: número da cena
- descricao_cena: descrição
- falante_oficial: quem fala (nome completo em MAIÚSCULAS)
- ouvinte_oficial: quem ouve (nome completo em MAIÚSCULAS)
- fala: texto
- tamanho_fala: comprimento
- num_personagens_cena: total na cena
- tipo_interacao: "direct" (2 personagens), "group" (3+)

Retorne APENAS JSON:
{{
  "interacoes": [
    {{
      "cena": 1,
      "descricao_cena": "",
      "falante_oficial": "JON SNOW",
      "ouvinte_oficial": "SANSA STARK",
      "fala": "texto",
      "tamanho_fala": 50,
      "num_personagens_cena": 2,
      "tipo_interacao": "direct"
    }}
  ]
}}"""
    
    print(f"   Bloco {num_bloco}...")
    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.1,
            'max_tokens': 8192
        },
        timeout=180
    )
    
    if response.status_code != 200:
        raise Exception(f"Erro API: {response.status_code}")
    
    result = response.json()['choices'][0]['message']['content']
    
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
        json_str = result[start:end]
    
    return json.loads(json_str)['interacoes']

def processar_episodio_com_deepseek(caminho_arquivo, api_key, temporada, episodio):
    cache_file = f"cache_{temporada}{episodio}.json"
    if os.path.exists(cache_file):
        print(f"   Usando cache...")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        script = f.read()
    
    blocos = dividir_script_por_cenas(script)
    print(f"   Dividido em {len(blocos)} blocos")
    
    todas_interacoes = []
    for i, bloco in enumerate(blocos, 1):
        try:
            interacoes = processar_bloco_deepseek(bloco, api_key, i)
            todas_interacoes.extend(interacoes)
        except Exception as e:
            print(f"   Erro no bloco {i}: {e}")
            continue
    
    for interacao in todas_interacoes:
        interacao['temporada'] = temporada
        interacao['episodio'] = episodio
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(todas_interacoes, f, ensure_ascii=False, indent=2)
    
    return todas_interacoes

def main():
    api_key = input("Cole sua API key do DeepSeek: ").strip()
    
    temporada = input("Temporada (ex: s01): ").strip()
    episodio = input("Episódio (ex: e01): ").strip()
    
    caminho = f"genius/{temporada}/got_{temporada}{episodio}.txt"
    
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return
    
    print(f"\nProcessando {temporada}{episodio}...")
    
    try:
        interacoes = processar_episodio_com_deepseek(caminho, api_key, temporada, episodio)
        
        df = pd.DataFrame(interacoes)
        output = f"interacoes_{temporada}{episodio}.csv"
        df.to_csv(output, index=False, encoding='utf-8')
        
        print(f"\n✓ Concluído!")
        print(f"  Interações encontradas: {len(interacoes)}")
        print(f"  Salvo em: {output}")
        
    except Exception as e:
        print(f"\n✗ Erro: {e}")

if __name__ == '__main__':
    main()
