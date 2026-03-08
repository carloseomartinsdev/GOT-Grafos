# 🔍 POR QUE OS RANKINGS SÃO DIFERENTES?

## ❌ EU ESTAVA ERRADO! Os métodos NÃO dão o mesmo resultado!

## 🎯 Diferenças Críticas:

### 1️⃣ **FILTRO DE TIPO DE INTERAÇÃO**

#### Notebook:
```python
df_direct = df[df["tipo_interacao"] == "single"]  # ❌ FILTRA apenas "single"
df_grouped = df_direct.groupby(['falante', 'ouvinte']).size()
```
- ✅ Usa apenas interações tipo "single"
- ❌ Ignora outros tipos de interação

#### Script:
```python
interacoes = df_interacoes[['falante', 'ouvinte']].dropna()  # ✅ USA TODAS
```
- ✅ Usa TODAS as interações (single, group, etc.)
- ✅ Dataset completo

### 2️⃣ **FÓRMULA DO CONSOLIDATED SCORE**

#### Notebook:
```python
scores = {
    p: norm_pr[i]*0.4 + norm_bt[i]*0.3 + norm_wd[i]*0.2 + norm_ev[i]*0.1
    for i,p in enumerate(personagens)
}
```
- PageRank: 40%
- Betweenness: 30%
- Weighted Degree: 20%
- Eigenvector: 10%
- **NÃO usa Closeness**

#### Script:
```python
consolidated_score[node] = (
    degree_centrality[node] +
    betweenness[node] +
    pagerank[node] * 100 +        # ❌ MULTIPLICA por 100!
    closeness_centrality[node]
) / 4
```
- Degree: 25%
- Betweenness: 25%
- PageRank * 100: 25%  ← **PROBLEMA AQUI!**
- Closeness: 25%
- **NÃO normaliza antes de combinar!**

### 3️⃣ **NORMALIZAÇÃO**

#### Notebook:
```python
scaler = MinMaxScaler()
norm_pr = scaler.fit_transform(...)  # ✅ Normaliza CADA métrica
```
- ✅ Normaliza cada métrica entre 0-1
- ✅ Todas as métricas na mesma escala

#### Script:
```python
consolidated_score[node] = (
    degree_centrality[node] +      # já está 0-1
    betweenness[node] +            # já está 0-1
    pagerank[node] * 100 +         # ❌ 0.01 * 100 = 1-10
    closeness_centrality[node]     # já está 0-1
) / 4
```
- ❌ PageRank multiplicado por 100 domina o score!
- ❌ Escalas diferentes causam viés

## 📊 Impacto Real:

### Exemplo: Tyrion Lannister

#### Notebook (correto):
- PageRank: 0.0636 → normalizado: 1.0
- Betweenness: 0.1194 → normalizado: 0.83
- Score final: 0.40×1.0 + 0.30×0.83 + ... = **0.949**

#### Script (problemático):
- PageRank: 0.0636 × 100 = **6.36** ← DOMINA!
- Betweenness: 0.1194
- Degree: 0.4526
- Closeness: 0.5123
- Score: (6.36 + 0.12 + 0.45 + 0.51) / 4 = **1.86**

**PageRank domina 85% do score no script!**

## ✅ QUAL ESTÁ CORRETO?

### 🏆 **NOTEBOOK está CORRETO** porque:

1. ✅ **Normaliza corretamente** (MinMaxScaler)
2. ✅ **Pesos justificados** (40%, 30%, 20%, 10%)
3. ✅ **Todas métricas na mesma escala**
4. ✅ **Padrão acadêmico**

### ❌ **SCRIPT tem PROBLEMAS**:

1. ❌ **PageRank × 100 domina o score**
2. ❌ **Não normaliza antes de combinar**
3. ❌ **Pesos iguais (25% cada) sem justificativa**
4. ❌ **Mistura escalas diferentes**

## 🔧 Como CORRIGIR o Script:

```python
# ANTES (ERRADO):
consolidated_score[node] = (
    degree_centrality[node] +
    betweenness[node] +
    pagerank[node] * 100 +  # ❌ PROBLEMA!
    closeness_centrality[node]
) / 4

# DEPOIS (CORRETO):
from sklearn.preprocessing import MinMaxScaler

# Normalizar cada métrica
scaler = MinMaxScaler()
nodes_list = list(G.nodes())

norm_dc = scaler.fit_transform([[degree_centrality[n]] for n in nodes_list])
norm_bt = scaler.fit_transform([[betweenness[n]] for n in nodes_list])
norm_pr = scaler.fit_transform([[pagerank[n]] for n in nodes_list])
norm_cc = scaler.fit_transform([[closeness_centrality[n]] for n in nodes_list])

# Score consolidado correto
consolidated_score = {}
for i, node in enumerate(nodes_list):
    consolidated_score[node] = (
        norm_dc[i][0] * 0.25 +
        norm_bt[i][0] * 0.25 +
        norm_pr[i][0] * 0.30 +  # ✅ Normalizado!
        norm_cc[i][0] * 0.20
    )
```

## 🎓 Conclusão:

### Rankings diferentes porque:

1. **Notebook filtra tipo_interacao="single"** → menos dados
2. **Script usa TODAS as interações** → mais dados
3. **Script multiplica PageRank × 100** → viés enorme
4. **Script não normaliza** → escalas incompatíveis

### Para análise acadêmica:

✅ **Use o NOTEBOOK** (método correto)
❌ **NÃO use o Script** (tem bugs matemáticos)

### Para corrigir o Script:

1. Remover `× 100` do PageRank
2. Normalizar todas as métricas antes de combinar
3. Usar pesos justificados (não 25% igual para tudo)

## 📈 Teste Rápido:

Execute ambos e compare o Top 5:

**Notebook (correto):**
1. Tyrion Lannister
2. Joffrey Baratheon
3. Jaime Lannister
4. Catelyn Stark
5. Daenerys Targaryen

**Script (com bug):**
- Ordem diferente devido ao PageRank × 100 dominando

**Solução:** Use o método do notebook para análise acadêmica!
