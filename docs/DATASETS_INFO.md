# Datasets de Game of Thrones - Análise de Redes

## 📁 Arquivos Criados

### 1. `dataset_personagens.csv`
**Descrição:** Lista de todos os personagens que falam nos scripts de GOT

**Colunas:**
- `personagem`: Nome do personagem
- `quantidade_falas`: Número total de vezes que o personagem fala

**Estatísticas:**
- Total de personagens: 513
- Top 5 personagens que mais falam:
  1. TYRION - 1,642 falas
  2. CERSEI - 917 falas
  3. DAENERYS - 914 falas
  4. JON - 913 falas
  5. JAIME - 907 falas

**Exemplo:**
```csv
personagem,quantidade_falas
TYRION,1642
CERSEI,917
DAENERYS,914
JON,913
JAIME,907
```

---

### 2. `dataset_interacoes.csv`
**Descrição:** Pares de personagens que interagem (falam em sequência) com contagem

**Colunas:**
- `personagem_1`: Primeiro personagem
- `personagem_2`: Segundo personagem
- `quantidade_interacoes`: Número de vezes que esses dois personagens falam em sequência

**Estatísticas:**
- Total de pares únicos: 2,279
- Total de interações: 19,987
- Top 5 pares que mais interagem:
  1. TYRION ↔ VARYS - 326 interações
  2. CERSEI ↔ JAIME - 292 interações
  3. CERSEI ↔ TYRION - 262 interações
  4. DAENERYS ↔ TYRION - 254 interações
  5. BRIENNE ↔ JAIME - 239 interações

**Exemplo:**
```csv
personagem_1,personagem_2,quantidade_interacoes
TYRION,VARYS,326
CERSEI,JAIME,292
CERSEI,TYRION,262
DAENERYS,TYRION,254
BRIENNE,JAIME,239
```

---

## 🔍 Como os Dados Foram Extraídos

### Metodologia

1. **Fonte de Dados:**
   - Scripts de todos os episódios de Game of Thrones (8 temporadas)
   - Pasta: `/genius/s01/` até `/genius/s08/`
   - Total: 73 episódios

2. **Extração de Personagens:**
   - Padrão regex: `^([A-Z][A-Z\s']+):\s`
   - Identifica linhas que começam com nome em MAIÚSCULAS seguido de ":"
   - Exemplo: `TYRION: I drink and I know things.`

3. **Contagem de Falas:**
   - Cada vez que um personagem aparece no formato `PERSONAGEM:` conta como 1 fala

4. **Extração de Interações:**
   - Quando dois personagens falam em sequência, é registrada uma interação
   - Exemplo:
     ```
     TYRION: Hello
     VARYS: Hello, my friend
     ```
     → Registra interação TYRION ↔ VARYS

5. **Agregação:**
   - Pares são ordenados alfabeticamente para evitar duplicatas
   - (TYRION, VARYS) e (VARYS, TYRION) são tratados como o mesmo par
   - Contagem acumulada de todas as interações ao longo das 8 temporadas

---

## 📊 Como Usar para Análise de Redes

### Construção do Grafo

```python
import pandas as pd
import networkx as nx

# Carregar dados
df_inter = pd.read_csv('dataset_interacoes.csv')

# Criar grafo
G = nx.Graph()

for _, row in df_inter.iterrows():
    G.add_edge(
        row['personagem_1'], 
        row['personagem_2'], 
        weight=row['quantidade_interacoes']
    )
```

### Métricas de Centralidade

**1. Degree Centrality (Grau)**
```python
degree = nx.degree_centrality(G)
# Quem tem mais conexões diretas?
```

**2. Betweenness Centrality (Intermediação)**
```python
betweenness = nx.betweenness_centrality(G, weight='weight')
# Quem conecta diferentes grupos?
```

**3. Closeness Centrality (Proximidade)**
```python
closeness = nx.closeness_centrality(G, distance='weight')
# Quem está mais próximo de todos?
```

**4. PageRank**
```python
pagerank = nx.pagerank(G, weight='weight')
# Quem é mais importante considerando a qualidade das conexões?
```

### Detecção de Comunidades

```python
import community.community_louvain as community_louvain

partition = community_louvain.best_partition(G, weight='weight')
# Identifica grupos de poder (Starks, Lannisters, etc.)
```

---

## 🎯 Respondendo a Pergunta de Negócio

### "Matematicamente, quem é o personagem mais importante?"

**Abordagem:**

1. **Calcular múltiplas métricas de centralidade**
   - Degree: popularidade
   - Betweenness: papel de conector
   - Closeness: alcance rápido
   - PageRank: importância ponderada

2. **Criar ranking consolidado**
   - Média das métricas normalizadas
   - Personagem com maior score médio = mais importante

3. **Validar com dados**
   - Quantidade de falas (dataset_personagens.csv)
   - Número de conexões (dataset_interacoes.csv)

### "Como os grupos de poder se organizam?"

**Abordagem:**

1. **Detecção de comunidades (Louvain)**
   - Agrupa personagens que interagem mais entre si
   - Identifica casas/facções

2. **Análise de modularidade**
   - Quão bem definidos são os grupos?
   - Existem personagens que transitam entre grupos?

3. **Visualização**
   - Cores diferentes para cada comunidade
   - Tamanho dos nós = importância
   - Espessura das arestas = frequência de interação

---

## 🚀 Scripts Disponíveis

### `criar_datasets.py`
- Extrai dados dos scripts
- Gera os 2 CSVs
- Mostra estatísticas básicas

**Executar:**
```bash
python criar_datasets.py
```

### `analise_redes.py`
- Carrega os datasets
- Constrói o grafo
- Calcula centralidades
- Detecta comunidades
- Gera visualização
- Responde a pergunta de negócio

**Executar:**
```bash
python analise_redes.py
```

---

## 📈 Insights Esperados

### Personagem Mais Importante
Baseado nas estatísticas preliminares, espera-se que **TYRION** seja o personagem mais importante porque:
- Maior número de falas (1,642)
- Maior número de interações únicas
- Interage com personagens de diferentes grupos (Lannisters, Daenerys, Starks)
- Alto betweenness (conecta diferentes facções)

### Grupos de Poder Esperados
1. **Casa Lannister**: Cersei, Jaime, Tyrion, Tywin
2. **Casa Stark**: Jon, Sansa, Arya, Bran, Robb
3. **Daenerys e Aliados**: Daenerys, Jorah, Missandei, Grey Worm
4. **Guarda da Noite**: Jon, Sam, Aemon, Alliser
5. **Outros**: Stannis, Davos, Melisandre

---

## 🔧 Requisitos

```bash
pip install networkx pandas matplotlib python-louvain
```

---

## 📝 Notas Importantes

1. **Limpeza de Dados:**
   - Alguns "personagens" são na verdade marcações de cena (CUT TO, INT, EXT)
   - Podem ser filtrados se necessário

2. **Variações de Nomes:**
   - Alguns personagens têm variações (HOUND vs THE HOUND)
   - Pode ser necessário normalização adicional

3. **Peso das Arestas:**
   - Representa frequência de interação
   - Não considera duração ou importância do diálogo

4. **Limitações:**
   - Apenas diálogos são considerados
   - Cenas sem diálogo não são capturadas
   - Interações não-verbais não são incluídas

---

## 📚 Referências Teóricas

- **Teoria dos Grafos**: Diestel, R. (2017)
- **Análise de Redes Sociais**: Wasserman & Faust (1994)
- **Algoritmo de Louvain**: Blondel et al. (2008)
- **PageRank**: Page & Brin (1998)

---

## ✅ Checklist de Análise

- [x] Extrair personagens dos scripts
- [x] Contar falas por personagem
- [x] Identificar interações entre personagens
- [x] Contar frequência de interações
- [x] Gerar datasets em CSV
- [ ] Construir grafo de interações
- [ ] Calcular métricas de centralidade
- [ ] Detectar comunidades
- [ ] Visualizar rede
- [ ] Responder pergunta de negócio

---

**Próximo Passo:** Execute `python analise_redes.py` para realizar a análise completa!
