import pandas as pd
import networkx as nx
import json

print("Carregando dados...")
df = pd.read_csv('datasets/interacoes.csv', low_memory=False)
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

# Carregar PageRank do graph_data.json
with open('public/resources/jsons/graph_data.json', 'r', encoding='utf-8') as f:
    graph_data = json.load(f)
    pagerank = {node['id']: node['influence_score'] for node in graph_data['nodes']}

print("Analisando cenas importantes...")

# 1. Top cenas com mais personagens importantes
cenas = []
for (temp, ep, cena), group in df.groupby(['NTemporada', 'NEpisodio', 'NCena']):
    personagens = set(group['falante'].unique()) | set(group['ouvinte'].dropna().unique())
    
    # Score da cena = soma do influence score dos personagens
    scene_score = sum([pagerank.get(p, 0) for p in personagens])
    
    cenas.append({
        'temporada': int(temp),
        'episodio': int(ep),
        'cena': int(cena),
        'descricao': str(group['descricao_cena'].iloc[0]) if 'descricao_cena' in group.columns and pd.notna(group['descricao_cena'].iloc[0]) else '',
        'num_personagens': len(personagens),
        'personagens': list(personagens)[:10],
        'score': scene_score
    })

top_cenas = sorted(cenas, key=lambda x: x['score'], reverse=True)[:50]

print("Analisando episódios importantes...")

# 2. Episódios mais densos (mais interações)
episodios = []
for (temp, ep), group in df.groupby(['NTemporada', 'NEpisodio']):
    num_interacoes = len(group)
    personagens = set(group['falante'].unique()) | set(group['ouvinte'].dropna().unique())
    
    # Densidade = interações / personagens
    densidade = num_interacoes / len(personagens) if len(personagens) > 0 else 0
    
    episodios.append({
        'temporada': int(temp),
        'episodio': int(ep),
        'num_interacoes': num_interacoes,
        'num_personagens': len(personagens),
        'densidade': densidade
    })

top_episodios = sorted(episodios, key=lambda x: x['densidade'], reverse=True)[:30]

print("Detectando turning points...")

# 3. Turning points - mudanças bruscas na rede por episódio
turning_points = []
prev_chars = set()

for (temp, ep), group in df.groupby(['NTemporada', 'NEpisodio']):
    current_chars = set(group['falante'].unique()) | set(group['ouvinte'].dropna().unique())
    
    # Personagens novos e que saíram
    novos = current_chars - prev_chars
    saidos = prev_chars - current_chars
    
    if len(novos) > 3 or len(saidos) > 3:
        turning_points.append({
            'temporada': int(temp),
            'episodio': int(ep),
            'novos': list(novos)[:5],
            'saidos': list(saidos)[:5],
            'num_novos': len(novos),
            'num_saidos': len(saidos)
        })
    
    prev_chars = current_chars

# Salvar resultados
output = {
    'top_cenas': top_cenas,
    'top_episodios': top_episodios,
    'turning_points': turning_points
}

print("Salvando eventos_importantes.json...")
with open('public/resources/jsons/eventos_importantes.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado com sucesso!")
print(f"   - {len(top_cenas)} cenas importantes")
print(f"   - {len(top_episodios)} episódios densos")
print(f"   - {len(turning_points)} turning points")
