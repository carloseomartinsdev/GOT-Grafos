import pandas as pd
import json
import os

print("Lendo dataset...")
df = pd.read_csv('dataset_interacoes_personagens.csv')
df['falante_oficial'] = df['falante_oficial'].str.strip().str.upper()
df['ouvinte_oficial'] = df['ouvinte_oficial'].str.strip().str.upper()

print(f"Total de interações: {len(df)}")

interactions = {}
for _, row in df.iterrows():
    a, b = sorted([row['falante_oficial'], row['ouvinte_oficial']])
    key = f"{a}|||{b}"
    if key not in interactions:
        interactions[key] = []
    interactions[key].append({
        's': int(row['temporada']),
        'e': int(row['episodio']),
        'c': int(row['cena']),
        'fala': str(row['fala'])[:150],
        'tipo': str(row['tipo_interacao'])
    })

output = 'public/interactions_index.json'
with open(output, 'w', encoding='utf-8') as f:
    json.dump(interactions, f, ensure_ascii=False, separators=(',', ':'))

size = os.path.getsize(output)
print(f"Pares únicos: {len(interactions)}")
print(f"Arquivo gerado: {output} ({size/1024:.0f} KB)")
