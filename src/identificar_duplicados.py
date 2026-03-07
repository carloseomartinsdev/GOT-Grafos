import pandas as pd
import json
import requests

print("="*60)
print("IDENTIFICADOR DE PERSONAGENS DUPLICADOS - GoT")
print("="*60)

print("\n[1/4] Carregando dataset...")
df = pd.read_csv('datasets/dataset_personagens.csv')
print(f"   Total de personagens no dataset: {len(df)}")

print("\n[2/4] Filtrando personagens...")
exclude = ['CUT TO', 'INT', 'EXT', 'MAN', 'WOMAN', 'ALL', 'MEN', 'WOMEN', 'CROWD']
df_filtered = df[~df['personagem'].isin(exclude)]
personagens = df_filtered['personagem'].tolist()
print(f"   Personagens filtrados: {len(personagens)}")

api_key = input("\n   Cole sua API key do DeepSeek: ")

def montar_prompt(lista):
    return f"""Analise esta lista de personagens de Game of Thrones e retorne 3 informações para cada um:
1. Nome principal completo
2. Variações/apelidos (separados por vírgula)
3. Família ou grupo (ex: Stark, Lannister, Night's Watch, Targaryen, etc)

Personagens: {', '.join(lista)}

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
- JON SNOW: variacoes="JON", familia="Stark/Night's Watch"
- TYRION LANNISTER: variacoes="TYRION", familia="Lannister"
- SANDOR CLEGANE: variacoes="THE HOUND, HOUND", familia="Clegane"

Retorne apenas o JSON, sem explicações."""

def chamar_api(lista, parte):
    print(f"   Enviando parte {parte} ({len(lista)} personagens)...")
    try:
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'deepseek-chat',
                'messages': [{'role': 'user', 'content': montar_prompt(lista)}],
                'temperature': 0.1,
                'max_tokens': 8000
            },
            timeout=180
        )
    except Exception as e:
        print(f"\n[ERRO] Falha na requisição parte {parte}: {e}")
        return None

    if response.status_code != 200:
        print(f"\n[ERRO] Status {response.status_code}: {response.text}")
        return None

    result = response.json()['choices'][0]['message']['content']

    with open(f'resposta_deepseek_parte{parte}.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"   Resposta parte {parte} salva em: resposta_deepseek_parte{parte}.txt")

    dados = parsear_json(result, f'parte{parte}')
    return dados['personagens'] if dados else None

def parsear_json(result, label):
    with open(f'resposta_deepseek_{label}.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    if '```json' in result:
        start = result.find('```json') + 7; end = result.find('```', start)
        json_str = result[start:end].strip()
    elif '```' in result:
        start = result.find('```') + 3; end = result.find('```', start)
        json_str = result[start:end].strip()
    else:
        start = result.find('{'); end = result.rfind('}') + 1
        if start == -1 or end == 0:
            print(f"[ERRO] JSON não encontrado em {label}"); return None
        json_str = result[start:end]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as je:
        print(f"[ERRO] JSON inválido em {label}: {je}"); return None

def mesclar(lista1, lista2):
    mapa = {}
    for item in lista1 + lista2:
        chave = item['nome'].strip().upper()
        if chave not in mapa:
            mapa[chave] = item
        else:
            vars_existentes = {v.strip() for v in mapa[chave]['variacoes'].split(',') if v.strip()}
            vars_novas = {v.strip() for v in item['variacoes'].split(',') if v.strip()}
            mapa[chave]['variacoes'] = ', '.join(sorted(vars_existentes | vars_novas))
    return list(mapa.values())

print("\n[3/4] Chamando DeepSeek API (2 requisições)...")
metade = len(personagens) // 2

resultado1 = chamar_api(personagens[:metade], 1)
if resultado1 is None:
    input("\nPressione Enter para sair...")
    exit()

resultado2 = chamar_api(personagens[metade:], 2)
if resultado2 is None:
    input("\nPressione Enter para sair...")
    exit()

personagens_mesclados = mesclar(resultado1, resultado2)
print(f"   Total após mesclagem: {len(personagens_mesclados)} personagens únicos")

# Verificação de redundância
print("\n[4/5] Verificando duplicados residuais...")
nomes_lista = [item['nome'] for item in personagens_mesclados]
prompt_dedup = f"""Analise esta lista de nomes de personagens de Game of Thrones e identifique pares que são o mesmo personagem (variações, apelidos, erros de grafia).

Nomes: {', '.join(nomes_lista)}

Retorne APENAS um JSON válido no formato:
{{
  "duplicados": [
    {{"manter": "NOME_PRINCIPAL", "remover": "NOME_DUPLICADO"}}
  ]
}}

Se não houver duplicados, retorne: {{"duplicados": []}}
Retorne apenas o JSON, sem explicações."""

try:
    resp_dedup = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={'model': 'deepseek-chat', 'messages': [{'role': 'user', 'content': prompt_dedup}], 'temperature': 0.1, 'max_tokens': 4000},
        timeout=120
    )
    dados_dedup = parsear_json(resp_dedup.json()['choices'][0]['message']['content'], 'dedup')
    if dados_dedup and dados_dedup.get('duplicados'):
        pares = dados_dedup['duplicados']
        print(f"   {len(pares)} duplicado(s) encontrado(s), mesclando...")
        mapa = {item['nome'].upper(): item for item in personagens_mesclados}
        for par in pares:
            chave_manter = par['manter'].upper()
            chave_remover = par['remover'].upper()
            if chave_manter in mapa and chave_remover in mapa:
                vars_manter = {v.strip() for v in mapa[chave_manter]['variacoes'].split(',') if v.strip()}
                vars_remover = {v.strip() for v in mapa[chave_remover]['variacoes'].split(',') if v.strip()}
                vars_remover.add(mapa[chave_remover]['nome'])
                mapa[chave_manter]['variacoes'] = ', '.join(sorted(vars_manter | vars_remover))
                del mapa[chave_remover]
        personagens_mesclados = list(mapa.values())
        print(f"   Total final: {len(personagens_mesclados)} personagens únicos")
    else:
        print("   Nenhum duplicado residual encontrado.")
except Exception as e:
    print(f"   [AVISO] Verificação de duplicados falhou: {e}. Continuando sem ela.")

dicionario = {'personagens': personagens_mesclados}

print("\n[5/5] Salvando...")
print("   Escolha o formato de saída:")
print("   1 - JSON (.json)")
print("   2 - JavaScript (.js)")
print("   3 - CSV (.csv)")
formato = input("   Opção (1-3): ").strip()

if formato == '2':
    filename = 'personagens_dicionario.js'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('const personagensDicionario = ')
        json.dump(dicionario, f, ensure_ascii=False, indent=2)
        f.write(';')
elif formato == '3':
    filename = 'datasets/personagens_dicionario.csv'
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
print(f"Dicionário criado com {len(personagens_mesclados)} entradas")
print(f"Salvo em: {filename}")
print("="*60)

input("\nPressione Enter para sair...")
