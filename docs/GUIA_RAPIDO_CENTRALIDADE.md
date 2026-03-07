# ⚡ Guia Rápido - Análise de Centralidade

## 🎯 Objetivo
Responder matematicamente: **"Quem é o personagem mais importante e como os grupos se organizam?"**

---

## 📦 Instalação

```bash
# Instalar bibliotecas necessárias
pip install networkx pandas matplotlib python-louvain
```

---

## 🚀 Execução

### Opção 1: Script Python (Recomendado)
```bash
cd GOT-Grafos
python src/analise_centralidade.py
```

**Output:**
- Rankings de todas as métricas no console
- Visualização do grafo salva em `datasets/grafo_top_personagens.png`
- Comunidades detectadas

### Opção 2: Notebook Jupyter (Interativo)
```bash
cd GOT-Grafos
jupyter notebook notebooks/analise_centralidade.ipynb
```

**Vantagens:**
- Exploração interativa
- Visualizações inline
- Modificar parâmetros facilmente

---

## 📊 O que será calculado

### 1. Centralidade de Grau
- Quem tem mais conexões?
- Top 10 personagens

### 2. Centralidade de Intermediação
- Quem conecta grupos diferentes?
- Top 10 pontes

### 3. PageRank
- Quem é mais influente?
- Top 10 influenciadores

### 4. Centralidade de Proximidade
- Quem está mais próximo de todos?
- Top 10 centrais

### 5. Detecção de Comunidades
- Quantos grupos existem?
- Quem pertence a cada grupo?
- Top 5 maiores comunidades

### 6. Ranking Consolidado
- **RESPOSTA FINAL:** Top 15 personagens mais importantes
- Score combinado de todas as métricas

---

## 🎨 Visualização

O script gera automaticamente:
- Grafo dos top 20 personagens
- Tamanho do nó = importância
- Cor do nó = score (vermelho = mais importante)
- Espessura da aresta = frequência de interação

---

## ⏱️ Tempo de Execução

- **Script completo:** ~30-60 segundos
- **Notebook:** Depende da exploração

---

## 📁 Arquivos Necessários

```
GOT-Grafos/
├── datasets/
│   └── dataset_interacoes_personagens.csv  ← NECESSÁRIO
├── src/
│   └── analise_centralidade.py             ← EXECUTAR
└── notebooks/
    └── analise_centralidade.ipynb          ← ALTERNATIVA
```

---

## 🔧 Troubleshooting

### Erro: "No module named 'community'"
```bash
pip install python-louvain
```

### Erro: "File not found"
Certifique-se de estar na pasta `GOT-Grafos`:
```bash
cd GOT-Grafos
python src/analise_centralidade.py
```

### Erro: "KeyError: 'tipo_interacao'"
Verifique se o arquivo `dataset_interacoes_personagens.csv` existe e tem as colunas corretas.

---

## 📈 Exemplo de Output

```
======================================================================
  ANÁLISE DE CENTRALIDADE - GAME OF THRONES
  Quem é matematicamente o personagem mais importante?
======================================================================

📊 Carregando dataset de interações...
✅ Grafo criado: 159 personagens, 1247 conexões

🔗 CENTRALIDADE DE GRAU (Degree Centrality)
   → Mede quantas conexões diretas cada personagem tem

Top 10 personagens com mais conexões:
   1. TYRION LANNISTER        - 0.5696 (90 conexões)
   2. JON SNOW                - 0.4937 (78 conexões)
   3. CERSEI LANNISTER        - 0.4810 (76 conexões)
   ...

🏆 RANKING CONSOLIDADO - PERSONAGEM MAIS IMPORTANTE
   → Média normalizada de todas as métricas

Top 15 personagens MAIS IMPORTANTES matematicamente:

   1. TYRION LANNISTER        - Score: 0.6234
      Grau: 0.570 | Intermediação: 0.234 | PageRank: 0.045 | Proximidade: 0.445
   ...
```

---

## 🎯 Próximos Passos

1. Execute o script
2. Analise os resultados
3. Abra a visualização gerada
4. Explore o notebook para análises customizadas
5. Use os resultados para responder a pergunta de negócio

---

## 📚 Documentação Completa

- [ALGORITMOS_CENTRALIDADE.md](ALGORITMOS_CENTRALIDADE.md) - Teoria detalhada
- [README.md](../README.md) - Visão geral do projeto

---

**✅ Pronto para descobrir quem é o personagem mais importante!**
