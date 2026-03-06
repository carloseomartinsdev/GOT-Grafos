import pandas as pd
import networkx as nx
import json

print("Carregando dados...")
df = pd.read_csv('dataset_interacoes_personagens.csv', low_memory=False)

# Filtrar personagens genéricos
excluir = ['ALL', 'Voice', 'Voices', 'GUARD', 'GUARDS', 'MAN', 'WOMAN', 'SOLDIER', 'SOLDIERS', 'CROWD']
df = df[~df['falante_oficial'].str.lower().str.contains('|'.join([e.lower() for e in excluir]), na=False)]
df = df[~df['ouvinte_oficial'].str.lower().str.contains('|'.join([e.lower() for e in excluir]), na=False)]

# Carregar PageRank do graph_data.json
with open('public/graph_data.json', 'r', encoding='utf-8') as f:
    graph_data = json.load(f)
    pagerank = {node['id']: node['influence_score'] for node in graph_data['nodes']}

print("Analisando cenas importantes...")

# 1. Top cenas com mais personagens importantes
cenas = []
for (temp, ep, cena), group in df.groupby(['temporada', 'episodio', 'cena']):
    personagens = set(group['falante_oficial'].unique()) | set(group['ouvinte_oficial'].dropna().unique())
    
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
for (temp, ep), group in df.groupby(['temporada', 'episodio']):
    num_interacoes = len(group)
    personagens = set(group['falante_oficial'].unique()) | set(group['ouvinte_oficial'].dropna().unique())
    
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

for (temp, ep), group in df.groupby(['temporada', 'episodio']):
    current_chars = set(group['falante_oficial'].unique()) | set(group['ouvinte_oficial'].dropna().unique())
    
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
with open('public/eventos_importantes.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado com sucesso!")
print(f"   - {len(top_cenas)} cenas importantes")
print(f"   - {len(top_episodios)} episódios densos")
print(f"   - {len(turning_points)} turning points")
