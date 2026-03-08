import pandas as pd
import networkx as nx
import json
import os
from networkx.algorithms import community
from sklearn.preprocessing import MinMaxScaler

# Carregar dados
print("Carregando dados...")
df = pd.read_csv('datasets/interacoes.csv', low_memory=False)
df_dicionario = pd.read_csv('datasets/personagens_dicionario.csv')
df_dicionario.columns = df_dicionario.columns.str.strip()
familia_map = {}
for _, row in df_dicionario.iterrows():
    oficial = row['NOME_OFICIAL']
    familia = row['FAMILIA_GRUPO']
    familia_map[oficial.upper()] = familia
    for var in str(row['VARIACOES']).split('|'):
        familia_map[var.strip().upper()] = familia

# Construir grafo (apenas interações single como no notebook)
print("Construindo grafo...")
df_direct = df[df["tipo_interacao"] == "single"]
df_grouped = df_direct.groupby(['falante', 'ouvinte']).size().reset_index(name='weight')
G = nx.from_pandas_edgelist(df_grouped, 'falante', 'ouvinte', edge_attr='weight', create_using=nx.Graph())

print(f"Nós: {G.number_of_nodes()}, Arestas: {G.number_of_edges()}")

# Detectar comunidades
print("Detectando comunidades...")
communities = community.greedy_modularity_communities(G, weight='weight')
node_community = {}
for i, comm in enumerate(communities):
    for node in comm:
        node_community[node] = i

# Calcular métricas (exatamente como no notebook)
print("Calculando métricas...")
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, weight='weight')
pagerank = nx.pagerank(G, weight='weight')
closeness_centrality = nx.closeness_centrality(G, distance='weight')
weighted_degree = dict(G.degree(weight='weight'))

# Calcular Influence Score (mantido para compatibilidade)
print("Calculando Influence Score...")
fala_stats = df.groupby('falante')['tamanho_fala'].agg(['sum', 'mean', 'count']).to_dict('index')
influence_score = {}
for node in G.nodes():
    score = 0
    total_fala = fala_stats.get(node, {}).get('sum', 0)
    media_fala = fala_stats.get(node, {}).get('mean', 0)
    for neighbor in G.neighbors(node):
        peso_conexao = G[node][neighbor]['weight']
        importancia_vizinho = pagerank.get(neighbor, 0)
        score += peso_conexao * importancia_vizinho * (media_fala / 100)
    score += (total_fala / 10000)
    influence_score[node] = score

# Calcular ranking consolidado (igual ao notebook)
print("Calculando ranking consolidado...")
scaler = MinMaxScaler()
nodes_list = list(G.nodes())

norm_dc = scaler.fit_transform([[degree_centrality[n]] for n in nodes_list]).flatten()
norm_bt = scaler.fit_transform([[betweenness[n]] for n in nodes_list]).flatten()
norm_pr = scaler.fit_transform([[pagerank[n]] for n in nodes_list]).flatten()
norm_cc = scaler.fit_transform([[closeness_centrality[n]] for n in nodes_list]).flatten()

consolidated_score = {}
for i, node in enumerate(nodes_list):
    consolidated_score[node] = (
        norm_pr[i] * 0.30 +
        norm_bt[i] * 0.25 +
        norm_dc[i] * 0.25 +
        norm_cc[i] * 0.20
    )

# Normalizar scores
min_inf = min(influence_score.values())
max_inf = max(influence_score.values())
min_cons = min(consolidated_score.values())
max_cons = max(consolidated_score.values())

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
            
            # Normalizar tamanho entre 80 e 400 baseado no Consolidated Score
            normalized_size = 80 + ((consolidated_score[node] - min_cons) / (max_cons - min_cons)) * 320
            
            # Garantir que familia não seja NaN
            familia = familia_map.get(node, '')
            if pd.isna(familia):
                familia = ''
            
            nodes_data.append({
                'id': node,
                'x': float(x),
                'y': float(y),
                'z': float(z),
                'community': int(comm_id),
                'familia': str(familia),
                'pagerank': float(pagerank[node]),
                'betweenness': float(betweenness[node]),
                'degree_centrality': float(degree_centrality[node]),
                'closeness_centrality': float(closeness_centrality[node]),
                'weighted_degree': float(weighted_degree[node]),
                'influence_score': float(influence_score[node]),
                'consolidated_score': float(consolidated_score[node]),
                'connections': int(G.degree(node)),
                'size': float(normalized_size)
            })

# Preparar arestas
edges_data = []
for u, v, data in G.edges(data=True):
    if data['weight'] > 5:
        edges_data.append({
            'source': str(u),
            'target': str(v),
            'weight': int(data['weight'])
        })

# Salvar JSON
output = {
    'nodes': nodes_data,
    'edges': edges_data
}

os.makedirs('public/resources/jsons', exist_ok=True)
print("Salvando graph_data.json...")
with open('public/resources/jsons/graph_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado com sucesso!")
print(f"   - {len(nodes_data)} personagens")
print(f"   - {len(edges_data)} conexões fortes")
print(f"   - {len(communities)} comunidades")
print(f"   - 27 cubos totalmente utilizados")
print(f"\nAbra 'visualizador.html' no navegador!")
