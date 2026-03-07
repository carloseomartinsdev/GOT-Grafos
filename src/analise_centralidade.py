import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from criar_grafo import criar_grafo  # Reutilizar função existente

def calcular_centralidade_grau(G, top_n=10):
    """Centralidade de Grau: Quem tem mais conexões diretas?"""
    print("[1] CENTRALIDADE DE GRAU (Degree Centrality)")
    print("    Mede quantas conexoes diretas cada personagem tem\n")
    
    degree_cent = nx.degree_centrality(G)
    top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    print(f"Top {top_n} personagens com mais conexões:")
    for i, (personagem, score) in enumerate(top_degree, 1):
        num_conexoes = G.degree(personagem)
        print(f"  {i:2d}. {personagem:25s} - {score:.4f} ({num_conexoes} conexoes)")
    
    return degree_cent

def calcular_centralidade_intermediacao(G, top_n=10):
    """Centralidade de Intermediação: Quem conecta diferentes grupos?"""
    print("\n[2] CENTRALIDADE DE INTERMEDIACAO (Betweenness Centrality)")
    print("    Mede quem serve de ponte entre diferentes grupos\n")
    
    betweenness_cent = nx.betweenness_centrality(G, weight='weight')
    top_betweenness = sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    print(f"Top {top_n} personagens que conectam grupos:")
    for i, (personagem, score) in enumerate(top_betweenness, 1):
        print(f"  {i:2d}. {personagem:25s} - {score:.4f}")
    
    return betweenness_cent

def calcular_pagerank(G, top_n=10):
    """PageRank: Quem é mais influente considerando a rede toda?"""
    print("\n[3] PAGERANK (Influencia)")
    print("    Mede a importancia considerando conexoes de qualidade\n")
    
    pagerank = nx.pagerank(G, weight='weight')
    top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    print(f"Top {top_n} personagens mais influentes:")
    for i, (personagem, score) in enumerate(top_pagerank, 1):
        print(f"  {i:2d}. {personagem:25s} - {score:.4f}")
    
    return pagerank

def calcular_centralidade_proximidade(G, top_n=10):
    """Centralidade de Proximidade: Quem está mais próximo de todos?"""
    print("\n[4] CENTRALIDADE DE PROXIMIDADE (Closeness Centrality)")
    print("    Mede quao proximo um personagem esta de todos os outros\n")
    
    closeness_cent = nx.closeness_centrality(G, distance='weight')
    top_closeness = sorted(closeness_cent.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    print(f"Top {top_n} personagens mais centrais:")
    for i, (personagem, score) in enumerate(top_closeness, 1):
        print(f"  {i:2d}. {personagem:25s} - {score:.4f}")
    
    return closeness_cent

def detectar_comunidades(G, top_n=5):
    """Detecção de Comunidades: Identifica grupos de poder"""
    print("\n[5] DETECCAO DE COMUNIDADES (Grupos de Poder)")
    print("    Identifica clusters naturais na rede\n")
    
    # Usar algoritmo de Louvain
    try:
        import community as community_louvain
        communities = community_louvain.best_partition(G, weight='weight')
    except ImportError:
        print("[!] Instalando python-louvain...")
        import os
        os.system("pip install python-louvain")
        import community as community_louvain
        communities = community_louvain.best_partition(G, weight='weight')
    
    # Contar personagens por comunidade
    community_counts = Counter(communities.values())
    
    print(f"Total de comunidades detectadas: {len(community_counts)}\n")
    
    # Mostrar maiores comunidades
    for comm_id, count in community_counts.most_common(top_n):
        membros = [p for p, c in communities.items() if c == comm_id]
        print(f"Comunidade {comm_id + 1} ({count} membros):")
        print(f"  {', '.join(membros[:10])}")
        if count > 10:
            print(f"  ... e mais {count - 10} personagens")
        print()
    
    return communities

def ranking_consolidado(degree, betweenness, pagerank, closeness, top_n=15):
    """Cria ranking consolidado normalizando todas as métricas"""
    print("\n[6] RANKING CONSOLIDADO - PERSONAGEM MAIS IMPORTANTE")
    print("    Media normalizada de todas as metricas\n")
    
    # Normalizar métricas (0-1)
    personagens = set(degree.keys())
    
    scores = {}
    for p in personagens:
        score = (
            degree.get(p, 0) +
            betweenness.get(p, 0) +
            pagerank.get(p, 0) * 100 +  # PageRank é muito pequeno, multiplicar
            closeness.get(p, 0)
        ) / 4
        scores[p] = score
    
    top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    print(f"Top {top_n} personagens MAIS IMPORTANTES matematicamente:\n")
    for i, (personagem, score) in enumerate(top_scores, 1):
        print(f"  {i:2d}. {personagem:25s} - Score: {score:.4f}")
        print(f"      Grau: {degree[personagem]:.3f} | "
              f"Intermediacao: {betweenness[personagem]:.3f} | "
              f"PageRank: {pagerank[personagem]:.3f} | "
              f"Proximidade: {closeness[personagem]:.3f}")
    
    return scores

def visualizar_top_personagens(G, scores, top_n=20):
    """Visualiza os top personagens com suas métricas"""
    print(f"\n[*] Gerando visualizacao dos top {top_n} personagens...")
    
    # Selecionar top personagens
    top_personagens = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_nodes = [p for p, _ in top_personagens]
    
    # Criar subgrafo
    G_top = G.subgraph(top_nodes).copy()
    
    plt.figure(figsize=(18, 12))
    
    # Layout
    pos = nx.spring_layout(G_top, k=2, iterations=50, seed=42)
    
    # Tamanho dos nós baseado no score
    node_sizes = [scores[n] * 5000 for n in G_top.nodes()]
    
    # Cores baseadas no score
    node_colors = [scores[n] for n in G_top.nodes()]
    
    # Desenhar nós
    nx.draw_networkx_nodes(
        G_top, pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.Reds,
        alpha=0.9,
        edgecolors='black',
        linewidths=2
    )
    
    # Desenhar arestas
    widths = [G_top[u][v]['weight'] / 15 for u, v in G_top.edges()]
    nx.draw_networkx_edges(
        G_top, pos,
        width=widths,
        alpha=0.3,
        edge_color='gray'
    )
    
    # Labels
    nx.draw_networkx_labels(
        G_top, pos,
        font_size=10,
        font_weight='bold',
        font_family='sans-serif'
    )
    
    plt.title(f"Top {top_n} Personagens Mais Importantes - Game of Thrones", 
              fontsize=18, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('datasets/grafo_top_personagens.png', dpi=300, bbox_inches='tight')
    print("[OK] Visualizacao salva em: datasets/grafo_top_personagens.png")
    plt.show()

def main():
    print("="*70)
    print("  ANALISE DE CENTRALIDADE - GAME OF THRONES")
    print("  Quem e matematicamente o personagem mais importante?")
    print("="*70 + "\n")
    
    # 1. Criar grafo (reutilizando funcao existente)
    print("[*] Carregando dataset e criando grafo...\n")
    G = criar_grafo()
    print()
    
    # 2. Calcular métricas
    degree = calcular_centralidade_grau(G, top_n=10)
    betweenness = calcular_centralidade_intermediacao(G, top_n=10)
    pagerank = calcular_pagerank(G, top_n=10)
    closeness = calcular_centralidade_proximidade(G, top_n=10)
    
    # 3. Detectar comunidades
    communities = detectar_comunidades(G, top_n=5)
    
    # 4. Ranking consolidado
    scores = ranking_consolidado(degree, betweenness, pagerank, closeness, top_n=15)
    
    # 5. Visualizar
    visualizar_top_personagens(G, scores, top_n=20)
    
    print("\n" + "="*70)
    print("[OK] ANALISE COMPLETA!")
    print("="*70)

if __name__ == "__main__":
    main()
