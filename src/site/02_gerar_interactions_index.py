import pandas as pd
import json
import os

print("Lendo datasets...")
df = pd.read_csv('datasets/interacoes.csv')
df_dicionario = pd.read_csv('datasets/personagens_dicionario.csv')

# Criar mapeamento de variações para nome oficial
nome_oficial_map = {}
for _, row in df_dicionario.iterrows():
    oficial = row['NOME_OFICIAL'].upper()
    nome_oficial_map[oficial] = oficial
    for var in str(row['VARIACOES']).split('|'):
        nome_oficial_map[var.strip().upper()] = oficial

# Normalizar nomes
df['falante'] = df['falante'].str.strip().str.upper().map(lambda x: nome_oficial_map.get(x, x))
df['ouvinte'] = df['ouvinte'].str.strip().str.upper().map(lambda x: nome_oficial_map.get(x, x))

print(f"Total de interações: {len(df)}")

interactions = {}
for _, row in df.iterrows():
    a, b = sorted([row['falante'], row['ouvinte']])
    key = f"{a}|||{b}"
    if key not in interactions:
        interactions[key] = []
    interactions[key].append({
        's': int(row['NTemporada']),
        'e': int(row['NEpisodio']),
        'c': int(row['NCena']),
        'fala': str(row['fala'])[:150],
        'tipo': str(row['tipo_interacao'])
    })

output = 'public/resources/jsons/interactions_index.json'
with open(output, 'w', encoding='utf-8') as f:
    json.dump(interactions, f, ensure_ascii=False, separators=(',', ':'))

size = os.path.getsize(output)
print(f"Pares únicos: {len(interactions)}")
print(f"Arquivo gerado: {output} ({size/1024:.0f} KB)")
