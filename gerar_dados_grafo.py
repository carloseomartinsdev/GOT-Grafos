import pandas as pd
import networkx as nx
import json
from networkx.algorithms import community
import math

# Carregar dados
print("Carregando dados...")
df_interacoes = pd.read_csv('dataset_interacoes_personagens.csv', low_memory=False)

# Construir grafo
print("Construindo grafo...")
G = nx.Graph()

interacoes = df_interacoes[['falante_oficial', 'ouvinte_oficial']].dropna()

# Filtrar personagens genéricos
excluir = ['ALL', 'Voice', 'Voices', 'GUARD', 'GUARDS', 'MAN', 'WOMAN', 'SOLDIER', 'SOLDIERS', 'CROWD']

for _, row in interacoes.iterrows():
    falante = row['falante_oficial']
    ouvinte = row['ouvinte_oficial']
    
    # Pular se for personagem genérico
    if any(ex.lower() in falante.lower() for ex in excluir):
        continue
    if any(ex.lower() in ouvinte.lower() for ex in excluir):
        continue
    
    if falante != ouvinte:
        if G.has_edge(falante, ouvinte):
            G[falante][ouvinte]['weight'] += 1
        else:
            G.add_edge(falante, ouvinte, weight=1)

print(f"Nós: {G.number_of_nodes()}, Arestas: {G.number_of_edges()}")

# Detectar comunidades
print("Detectando comunidades...")
communities = community.greedy_modularity_communities(G, weight='weight')
node_community = {}
for i, comm in enumerate(communities):
    for node in comm:
        node_community[node] = i

# Calcular métricas
print("Calculando métricas...")
pagerank = nx.pagerank(G, weight='weight')
betweenness = nx.betweenness_centrality(G, weight='weight')
weighted_degree = dict(G.degree(weight='weight'))

# Calcular Influence Score customizado
print("Calculando Influence Score...")
# Tamanho médio das falas por personagem
fala_stats = df_interacoes.groupby('falante_oficial')['tamanho_fala'].agg(['sum', 'mean', 'count']).to_dict('index')

influence_score = {}
for node in G.nodes():
    score = 0
    
    # Estatísticas de fala do personagem
    total_fala = fala_stats.get(node, {}).get('sum', 0)
    media_fala = fala_stats.get(node, {}).get('mean', 0)
    num_falas = fala_stats.get(node, {}).get('count', 0)
    
    # Para cada conexão
    for neighbor in G.neighbors(node):
        peso_conexao = G[node][neighbor]['weight']
        importancia_vizinho = pagerank.get(neighbor, 0)
        
        # Score = peso_conexão * importância_do_vizinho * média_de_fala
        score += peso_conexao * importancia_vizinho * (media_fala / 100)
    
    # Adicionar componente de volume total de fala
    score += (total_fala / 10000)
    
    influence_score[node] = score

# Normalizar influence score
min_inf = min(influence_score.values())
max_inf = max(influence_score.values())

# Normalizar PageRank
min_pr = min(pagerank.values())
max_pr = max(pagerank.values())

# Distribuir 27 cubos proporcionalmente
print("Distribuindo comunidades em 27 cubos proporcionalmente...")
cube_size = 3000
spacing = 1500

# Calcular tamanho de cada comunidade
community_sizes = [(i, len(comm)) for i, comm in enumerate(communities)]
community_sizes.sort(key=lambda x: x[1], reverse=True)

# Alocar cubos proporcionalmente
total_nodes = sum([size for _, size in community_sizes])
cubes_allocation = []
remaining_cubes = 27

for i, (comm_id, size) in enumerate(community_sizes):
    if i == len(community_sizes) - 1:
        num_cubes = remaining_cubes
    else:
        proportion = size / total_nodes
        num_cubes = max(1, round(proportion * 27))
        num_cubes = min(num_cubes, remaining_cubes - (len(community_sizes) - i - 1))
    
    cubes_allocation.append((comm_id, num_cubes))
    remaining_cubes -= num_cubes

print(f"Alocação de cubos por comunidade:")
for comm_id, num_cubes in cubes_allocation:
    print(f"  Comunidade {comm_id}: {num_cubes} cubos ({len(communities[comm_id])} personagens)")

# Posições dos 27 cubos (3x3x3)
cube_positions = []
for x in range(3):
    for y in range(3):
        for z in range(3):
            cube_positions.append({
                'x': (x - 1) * (cube_size + spacing),
                'y': (y - 1) * (cube_size + spacing),
                'z': (z - 1) * (cube_size + spacing)
            })

# Atribuir cubos às comunidades
community_cube_positions = {}
cube_idx = 0
for comm_id, num_cubes in cubes_allocation:
    community_cube_positions[comm_id] = []
    for _ in range(num_cubes):
        if cube_idx < 27:
            community_cube_positions[comm_id].append(cube_positions[cube_idx])
            cube_idx += 1

# Gerar posições dos nós
nodes_data = []
for comm_id, comm_nodes in enumerate(communities):
    if comm_id not in community_cube_positions or len(community_cube_positions[comm_id]) == 0:
        continue
    
    subG = G.subgraph(comm_nodes)
    if len(subG.nodes()) > 1:
        pos = nx.spring_layout(subG, k=3, iterations=50, seed=42)
    else:
        pos = {list(comm_nodes)[0]: [0, 0]}
    
    # Distribuir nós entre os cubos alocados
    nodes_list = list(comm_nodes)
    cubes_for_comm = community_cube_positions[comm_id]
    nodes_per_cube = len(nodes_list) // len(cubes_for_comm) + 1
    
    for cube_idx, center in enumerate(cubes_for_comm):
        start_idx = cube_idx * nodes_per_cube
        end_idx = min(start_idx + nodes_per_cube, len(nodes_list))
        
        for node in nodes_list[start_idx:end_idx]:
            local_x = pos[node][0] * cube_size * 0.8
            local_y = pos[node][1] * cube_size * 0.8
            local_z = (hash(node) % 2000 - 1000) * 1.5
            
            x = center['x'] + local_x
            y = center['y'] + local_y
            z = center['z'] + local_z
            
            # Normalizar tamanho entre 80 e 400 baseado no Influence Score
            normalized_size = 80 + ((influence_score[node] - min_inf) / (max_inf - min_inf)) * 320
            
            nodes_data.append({
                'id': node,
                'x': x,
                'y': y,
                'z': z,
                'community': comm_id,
                'pagerank': pagerank[node],
                'betweenness': betweenness[node],
                'weighted_degree': weighted_degree[node],
                'influence_score': influence_score[node],
                'connections': G.degree(node),
                'size': normalized_size
            })

# Preparar arestas
edges_data = []
for u, v, data in G.edges(data=True):
    if data['weight'] > 5:
        edges_data.append({
            'source': u,
            'target': v,
            'weight': data['weight']
        })

# Salvar JSON
output = {
    'nodes': nodes_data,
    'edges': edges_data
}

print("Salvando graph_data.json...")
with open('public/graph_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado com sucesso!")
print(f"   - {len(nodes_data)} personagens")
print(f"   - {len(edges_data)} conexões fortes")
print(f"   - {len(communities)} comunidades")
print(f"   - 27 cubos totalmente utilizados")
print(f"\nAbra 'visualizador.html' no navegador!")
