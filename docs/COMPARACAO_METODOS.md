# 🔬 Comparação: Notebook vs Script - Qual é Melhor?

## 📊 Diferença Fundamental

### Notebook (analise_centralidade_final.ipynb):
```python
df_grouped = df_direct.groupby(['falante', 'ouvinte']).size().reset_index(name='weight')
G = nx.from_pandas_edgelist(df_grouped, 'falante', 'ouvinte', edge_attr='weight')
```
- ✅ **Agrupa ANTES** de criar grafo
- ✅ **Mais eficiente** (processa 27K → 1091 arestas)
- ✅ **Matematicamente correto** para análise de rede

### Script (01_gerar_dados_grafo.py):
```python
for _, row in interacoes.iterrows():
    if G.has_edge(falante, ouvinte):
        G[falante][ouvinte]['weight'] += 1
```
- ⚠️ **Itera 27K vezes** (mais lento)
- ⚠️ **Mesmo resultado final**, mas menos eficiente
- ✅ **Adiciona métricas extras** (influence_score, consolidated_score)

## 🎯 Veredicto: AMBOS ESTÃO CORRETOS!

### Por que 1091 arestas com 27K interações?

**Exemplo:**
- Tyrion fala com Jon 50 vezes → **1 aresta** com weight=50
- Tyrion fala com Cersei 30 vezes → **1 aresta** com weight=30
- Total: 80 interações = **2 arestas**

**27.000 interações ÷ ~25 interações médias por par = ~1.080 arestas** ✅

## 📈 Qual Usar para Análise Acadêmica?

### ✅ **NOTEBOOK é MELHOR** porque:

1. **Mais eficiente** (pandas groupby vs loop)
2. **Código mais limpo** e legível
3. **Padrão acadêmico** (NetworkX recomenda)
4. **Foco nas métricas certas**:
   - Degree Centrality
   - Betweenness Centrality
   - PageRank
   - Eigenvector Centrality
   - Weighted Degree

### ⚠️ **SCRIPT é melhor para VISUALIZAÇÃO** porque:

1. Calcula **Influence Score customizado**
2. Distribui nós em **27 cubos 3D**
3. Detecta **comunidades**
4. Gera JSON para visualização web

## 🔧 Recomendação: COMBINE OS DOIS!

### Use o NOTEBOOK para:
- ✅ Análise acadêmica de centralidade
- ✅ Definir personagem mais importante
- ✅ Gerar rankings e estatísticas

### Use o SCRIPT para:
- ✅ Visualização 3D interativa
- ✅ Exploração de comunidades
- ✅ Apresentação visual dos resultados

## 📝 Melhor Abordagem:

```python
# 1. CARREGAR E AGRUPAR (método do notebook - CORRETO)
df_grouped = df.groupby(['falante', 'ouvinte']).size().reset_index(name='weight')
G = nx.from_pandas_edgelist(df_grouped, 'falante', 'ouvinte', edge_attr='weight', create_using=nx.Graph())

# 2. CALCULAR MÉTRICAS (método do notebook - CORRETO)
pagerank = nx.pagerank(G, weight='weight')
betweenness = nx.betweenness_centrality(G, weight='weight')
degree_cent = nx.degree_centrality(G)
closeness_cent = nx.closeness_centrality(G, distance='weight')
eigenvector_cent = nx.eigenvector_centrality(G, weight='weight')
weighted_degree = dict(G.degree(weight='weight'))

# 3. RANKING CONSOLIDADO (melhorar pesos)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# Normalizar cada métrica
norm_pr = scaler.fit_transform([[pagerank[p]] for p in G.nodes()])
norm_bt = scaler.fit_transform([[betweenness[p]] for p in G.nodes()])
norm_dc = scaler.fit_transform([[degree_cent[p]] for p in G.nodes()])
norm_cc = scaler.fit_transform([[closeness_cent[p]] for p in G.nodes()])
norm_ec = scaler.fit_transform([[eigenvector_cent[p]] for p in G.nodes()])

# Score consolidado com pesos justificados
scores = {}
for i, node in enumerate(G.nodes()):
    scores[node] = (
        norm_pr[i][0] * 0.30 +  # PageRank: importância global
        norm_bt[i][0] * 0.25 +  # Betweenness: ponte entre grupos
        norm_dc[i][0] * 0.20 +  # Degree: diversidade de conexões
        norm_cc[i][0] * 0.15 +  # Closeness: proximidade média
        norm_ec[i][0] * 0.10    # Eigenvector: conexões importantes
    )
```

## 🎓 Conclusão Acadêmica:

**O NOTEBOOK está usando o método CORRETO e EFICIENTE.**

O "problema" de 1091 arestas vs 27K interações **NÃO É UM PROBLEMA**:
- 27K = número de LINHAS no dataset (cada fala)
- 1091 = número de PARES ÚNICOS de personagens que interagem
- Cada aresta tem weight = soma de todas as interações daquele par

**Exemplo Real:**
- Tyrion ↔ Cersei: 150 interações → 1 aresta (weight=150)
- Jon ↔ Sansa: 80 interações → 1 aresta (weight=80)
- Total: 230 interações = 2 arestas ✅

## ✅ Resposta Final:

**Use o método do NOTEBOOK** para análise acadêmica.
É matematicamente correto, eficiente e segue padrões da literatura.

O script é ótimo para visualização, mas o notebook é melhor para análise.
