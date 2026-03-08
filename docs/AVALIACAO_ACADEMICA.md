# 📊 Avaliação Acadêmica - Análise de Centralidade GOT

## ✅ SATISFATÓRIO (Nota: 7.5/10)

### O que está BOM:
- ✅ Usa 5 métricas de centralidade (Degree, Betweenness, PageRank, Eigenvector, Weighted Degree)
- ✅ Normalização adequada (MinMaxScaler)
- ✅ Ranking consolidado com pesos
- ✅ Visualização clara
- ✅ Dados validados (personagens reais)

### O que FALTA para nota 10:

#### 1. **Justificativa Teórica dos Pesos** (CRÍTICO)
```markdown
**Adicionar célula explicando:**
- PageRank 40%: Mede importância global considerando qualidade das conexões
- Betweenness 30%: Identifica pontes entre grupos/famílias
- Weighted Degree 20%: Volume total de interações
- Eigenvector 10%: Conexões com personagens importantes

**Referências:**
- Newman, M. (2010). Networks: An Introduction
- Wasserman & Faust (1994). Social Network Analysis
```

#### 2. **Closeness Centrality** (IMPORTANTE)
```python
# Adicionar após Eigenvector
closeness_cent = nx.closeness_centrality(G, distance='weight')
```

#### 3. **Interpretação das Métricas** (CRÍTICO)
```markdown
**Adicionar seção:**

### O que cada métrica significa:
- **Degree**: Quantos personagens diferentes interagem com ele
- **Betweenness**: Personagens que conectam diferentes grupos (ex: Brienne conecta Starks e Lannisters)
- **PageRank**: Importância considerando com QUEM você interage (não só quantos)
- **Eigenvector**: Estar conectado a personagens importantes te torna importante
- **Weighted Degree**: Volume bruto de interações
```

#### 4. **Análise de Consistência** (RECOMENDADO)
```python
# Correlação entre métricas
import seaborn as sns
df_metrics = pd.DataFrame({
    'PageRank': [pagerank[p] for p in personagens],
    'Betweenness': [betweenness_cent[p] for p in personagens],
    'Degree': [degree_cent[p] for p in personagens]
})
sns.heatmap(df_metrics.corr(), annot=True, cmap='coolwarm')
plt.title('Correlação entre Métricas de Centralidade')
```

#### 5. **Conclusão Acadêmica** (CRÍTICO)
```markdown
## 🎯 Conclusão

**Tyrion Lannister** é matematicamente o personagem mais relevante de Game of Thrones:
- #1 em PageRank (0.0598) - Interage com personagens importantes
- #2 em Degree (0.4526) - Interage com muitos personagens diferentes
- #1 no Score Consolidado (0.9491)

**Interpretação Narrativa:**
Tyrion é central porque:
1. Transita entre múltiplas famílias (Lannister, Stark, Targaryen)
2. Participa de eventos-chave em múltiplas storylines
3. Interage com personagens de alto poder (reis, rainhas, lords)

**Limitações:**
- Análise baseada apenas em interações diretas (diálogos)
- Não considera importância narrativa (mortes, decisões políticas)
- Não pondera qualidade das interações (aliança vs conflito)
```

#### 6. **Comparação com Literatura** (OPCIONAL mas FORTE)
```markdown
### Comparação com Estudos Anteriores:
- Beveridge & Shan (2016): Network of Thrones - Tyrion também identificado como central
- Nossa análise confirma: Tyrion > Jon Snow > Daenerys em centralidade de rede
```

## 📝 Resumo das Melhorias Necessárias:

### CRÍTICAS (para nota 9+):
1. Justificar pesos escolhidos
2. Interpretar o que cada métrica significa
3. Conclusão acadêmica fundamentada

### IMPORTANTES (para nota 8+):
4. Adicionar Closeness Centrality
5. Análise de consistência entre métricas

### RECOMENDADAS (para nota 10):
6. Comparação com literatura existente
7. Discussão de limitações
8. Análise temporal (evolução por temporada)

## ✅ Veredicto Final:

**A análise está SATISFATÓRIA para nível acadêmico**, mas precisa de:
- **Fundamentação teórica** (por que esses pesos?)
- **Interpretação** (o que os números significam?)
- **Conclusão** (responder: quem é o mais importante e POR QUÊ?)

Com essas 3 adições, a análise estaria **EXCELENTE** (nota 9+).
