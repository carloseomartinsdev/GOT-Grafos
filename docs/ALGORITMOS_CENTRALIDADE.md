# 🎯 Algoritmos de Centralidade - Teoria e Aplicação

## 📚 Introdução

Este documento explica os algoritmos de teoria dos grafos aplicados para responder:
> **"Matematicamente, quem é o personagem mais importante da saga e como os grupos de poder se organizam?"**

---

## 🔍 Algoritmos Implementados

### 1️⃣ Centralidade de Grau (Degree Centrality)

**O que mede:** Quantas conexões diretas um personagem tem.

**Fórmula:**
```
C_D(v) = grau(v) / (n - 1)
```
Onde:
- `grau(v)` = número de conexões do nó v
- `n` = total de nós no grafo

**Interpretação em GOT:**
- Personagens com alta centralidade de grau interagem com muitos outros personagens
- Indica personagens "socialmente ativos"
- Exemplo: Tyrion interage com muitos personagens diferentes

**Quando usar:**
- Identificar personagens com muitas conexões diretas
- Medir popularidade/sociabilidade

---

### 2️⃣ Centralidade de Intermediação (Betweenness Centrality)

**O que mede:** Quantas vezes um personagem aparece no caminho mais curto entre outros personagens.

**Fórmula:**
```
C_B(v) = Σ (σ_st(v) / σ_st)
```
Onde:
- `σ_st` = número de caminhos mais curtos entre s e t
- `σ_st(v)` = número desses caminhos que passam por v

**Interpretação em GOT:**
- Personagens que conectam diferentes grupos/facções
- "Pontes" entre comunidades
- Exemplo: Personagens que transitam entre Stark e Lannister

**Quando usar:**
- Identificar mediadores e conectores
- Encontrar personagens que unem grupos diferentes
- Detectar "gargalos" na rede

---

### 3️⃣ PageRank

**O que mede:** Importância baseada na qualidade das conexões (não apenas quantidade).

**Conceito:**
- Algoritmo usado pelo Google para ranquear páginas web
- Uma conexão com um personagem importante vale mais que várias conexões com personagens secundários

**Fórmula simplificada:**
```
PR(v) = (1-d)/n + d * Σ (PR(u) / L(u))
```
Onde:
- `d` = fator de amortecimento (geralmente 0.85)
- `L(u)` = número de links saindo de u
- `n` = número total de nós

**Interpretação em GOT:**
- Personagens influentes conectados a outros personagens influentes
- Mede "prestígio" na rede
- Exemplo: Interagir com Cersei vale mais que interagir com um guarda

**Quando usar:**
- Identificar personagens verdadeiramente influentes
- Considerar qualidade sobre quantidade de conexões

---

### 4️⃣ Centralidade de Proximidade (Closeness Centrality)

**O que mede:** Quão próximo um personagem está de todos os outros.

**Fórmula:**
```
C_C(v) = (n - 1) / Σ d(v, u)
```
Onde:
- `d(v, u)` = distância (caminho mais curto) entre v e u
- `n` = número total de nós

**Interpretação em GOT:**
- Personagens que podem alcançar outros rapidamente
- Posição central na rede
- Exemplo: Personagens que estão "no meio de tudo"

**Quando usar:**
- Identificar personagens centrais na trama
- Medir acessibilidade na rede

---

### 5️⃣ Detecção de Comunidades (Louvain Algorithm)

**O que faz:** Identifica grupos naturais de personagens que interagem mais entre si.

**Conceito:**
- Maximiza a modularidade do grafo
- Agrupa nós que têm mais conexões internas que externas

**Modularidade:**
```
Q = 1/(2m) * Σ [A_ij - (k_i * k_j)/(2m)] * δ(c_i, c_j)
```
Onde:
- `m` = número de arestas
- `A_ij` = peso da aresta entre i e j
- `k_i` = grau do nó i
- `δ(c_i, c_j)` = 1 se i e j estão na mesma comunidade

**Interpretação em GOT:**
- Identifica facções/casas/grupos de poder
- Exemplo: Stark, Lannister, Targaryen, Night's Watch
- Mostra alianças naturais

**Quando usar:**
- Responder "como os grupos se organizam?"
- Identificar clusters e facções
- Visualizar estrutura social

---

## 🏆 Ranking Consolidado

Para determinar **O personagem mais importante**, combinamos todas as métricas:

```python
Score_Total = (Grau + Betweenness + PageRank*100 + Closeness) / 4
```

**Por que combinar?**
- Cada métrica captura um aspecto diferente de importância
- Grau = popularidade
- Betweenness = poder de conexão
- PageRank = influência
- Closeness = centralidade

**Resultado:**
Um ranking que considera múltiplas dimensões de importância.

---

## 📊 Aplicação no Projeto

### Estrutura do Grafo GOT:
- **Nós:** Personagens
- **Arestas:** Interações diretas (diálogos)
- **Pesos:** Número de interações

### Pipeline de Análise:
1. Carregar dataset de interações
2. Construir grafo não-direcionado ponderado
3. Calcular 4 métricas de centralidade
4. Detectar comunidades
5. Gerar ranking consolidado
6. Visualizar resultados

---

## 🎯 Respondendo as Perguntas

### "Quem é o personagem mais importante?"

**Critérios matemáticos:**
1. Alta centralidade de grau (muitas conexões)
2. Alta intermediação (conecta grupos)
3. Alto PageRank (conexões de qualidade)
4. Alta proximidade (central na rede)

**Resposta:** O personagem com maior Score_Total no ranking consolidado.

### "Como os grupos de poder se organizam?"

**Análise:**
1. Algoritmo de Louvain detecta comunidades
2. Comunidades representam grupos naturais
3. Modularidade mede qualidade da divisão

**Resposta:** Visualização das comunidades detectadas + lista de membros.

---

## 📚 Referências

- Newman, M. E. J. (2010). Networks: An Introduction. Oxford University Press.
- Blondel, V. D., et al. (2008). Fast unfolding of communities in large networks.
- Page, L., et al. (1999). The PageRank Citation Ranking.
- NetworkX Documentation: https://networkx.org/

---

## 🚀 Como Executar

### Script Python:
```bash
python src/analise_centralidade.py
```

### Notebook Jupyter:
```bash
jupyter notebook notebooks/analise_centralidade.ipynb
```

---

## 📈 Outputs Gerados

1. **Console:** Rankings de cada métrica
2. **Visualização:** Grafo dos top 20 personagens
3. **Arquivo:** `datasets/grafo_top_personagens.png`
4. **Comunidades:** Lista de grupos detectados

---

**✅ Análise completa e matematicamente fundamentada!**
