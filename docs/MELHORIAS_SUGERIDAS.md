# Melhorias Sugeridas para Análise de Centralidade

## 1. Fundamentação Teórica dos Pesos
**Adicionar célula explicando:**
- Por que PageRank recebe 40%? (mede importância global na rede)
- Por que Betweenness 30%? (identifica pontes entre grupos)
- Por que Weighted Degree 20%? (volume de interações)
- Por que Eigenvector 10%? (conexões com personagens importantes)

## 2. Adicionar Closeness Centrality
```python
closeness_cent = nx.closeness_centrality(G, distance='weight')
```

## 3. Análise de Consistência
```python
# Correlação entre métricas
import seaborn as sns
correlation_matrix = df_final[['PageRank', 'Betweenness', 'W_Degree', 'Eigenvector']].corr()
sns.heatmap(correlation_matrix, annot=True)
```

## 4. Interpretação Narrativa
**Adicionar seção explicando:**
- **Degree**: Quantos personagens diferentes interagem com ele
- **Betweenness**: Personagens que conectam diferentes grupos/famílias
- **PageRank**: Importância considerando qualidade das conexões
- **Eigenvector**: Personagens conectados a outros importantes
- **Weighted Degree**: Volume total de interações

## 5. Análise de Comunidades
```python
from networkx.algorithms import community
communities = community.greedy_modularity_communities(G)
# Identificar famílias/grupos automaticamente
```

## 6. Análise Temporal
```python
# Criar grafos por temporada
for season in range(1, 9):
    G_season = criar_grafo_temporada(season)
    calcular_centralidades(G_season)
# Mostrar evolução de Tyrion, Jon, Daenerys ao longo das temporadas
```

## 7. Validação dos Dados
**Investigar:**
- Por que "DAISY" está no top 10?
- "BOWEN MARSH" é realmente tão relevante?
- Verificar se há problemas no dataset de personagens

## 8. Conclusão Acadêmica
**Adicionar seção final:**
- Qual métrica é mais adequada para GOT? (provavelmente PageRank + Betweenness)
- Tyrion é consistentemente #1 em quase todas as métricas
- Comparar com protagonismo percebido pelos fãs
- Limitações da análise (apenas interações diretas, não considera importância narrativa)

## 9. Testes Estatísticos
```python
# Teste de significância das diferenças
from scipy import stats
# Verificar se diferença entre Tyrion e Joffrey é estatisticamente significativa
```

## 10. Métricas Adicionais
- **Harmonic Centrality**: Alternativa à Closeness para grafos desconectados
- **Katz Centrality**: Similar ao Eigenvector mas mais robusta
- **Load Centrality**: Variação do Betweenness
