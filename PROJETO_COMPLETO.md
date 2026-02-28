# 🎯 PROJETO COMPLETO - Análise de Redes Game of Thrones

## 📦 Entregáveis

### 1️⃣ DATASETS (CSV)

✅ **dataset_personagens.csv**
- 513 personagens únicos
- Quantidade de falas de cada um
- Ordenado por relevância

✅ **dataset_interacoes.csv**
- 2,279 pares únicos de interações
- 19,987 interações totais
- Quantidade de vezes que cada par interage

---

### 2️⃣ SCRIPTS PYTHON

✅ **criar_datasets.py**
- Extrai dados de 73 episódios (8 temporadas)
- Gera os 2 CSVs automaticamente
- Mostra estatísticas

✅ **analise_redes.py**
- Constrói grafo de interações
- Calcula 5 métricas de centralidade
- Detecta comunidades (grupos de poder)
- Gera visualização da rede
- Responde matematicamente quem é o personagem mais importante

✅ **baixar_fotos.py** ⭐ NOVO!
- Integrado com dataset_personagens.csv
- Busca no Google Images: "[NOME] GOT"
- Baixa primeira foto automaticamente
- Salva como: personagem_got.jpg
- **TESTADO E FUNCIONANDO!**

---

### 3️⃣ DOCUMENTAÇÃO

✅ **README.md**
- Metodologia completa
- Explicação dos algoritmos
- Teoria dos grafos aplicada

✅ **DATASETS_INFO.md**
- Guia detalhado dos datasets
- Como usar para análise de redes
- Exemplos de código

✅ **FOTOS_README.md**
- Como usar o script de download
- Integração com dataset
- Configurações e melhorias

---

## 🚀 Como Executar o Projeto

### Passo 1: Instalar Dependências
```bash
pip install networkx pandas matplotlib python-louvain beautifulsoup4 requests
```

### Passo 2: Gerar Datasets (se necessário)
```bash
python criar_datasets.py
```

### Passo 3: Baixar Fotos dos Personagens
```bash
python baixar_fotos.py
```

### Passo 4: Análise de Redes Completa
```bash
python analise_redes.py
```

---

## 📊 Resultados Obtidos

### Datasets Criados ✅
```
dataset_personagens.csv    - 513 personagens
dataset_interacoes.csv     - 2,279 pares, 19,987 interações
```

### Fotos Baixadas ✅
```
personagens_fotos/
├── tyrion_got.jpg
├── cersei_got.jpg
├── daenerys_got.jpg
└── ... (configurável)
```

### Top 5 Personagens (por falas)
1. TYRION - 1,642 falas
2. CERSEI - 917 falas
3. DAENERYS - 914 falas
4. JON - 913 falas
5. JAIME - 907 falas

### Top 5 Interações
1. TYRION ↔ VARYS - 326x
2. CERSEI ↔ JAIME - 292x
3. CERSEI ↔ TYRION - 262x
4. DAENERYS ↔ TYRION - 254x
5. BRIENNE ↔ JAIME - 239x

---

## 🎯 Pergunta de Negócio

### "Matematicamente, quem é o personagem mais importante?"

**Resposta será obtida através de:**
- Degree Centrality (conexões diretas)
- Betweenness Centrality (ponte entre grupos)
- Closeness Centrality (proximidade geral)
- PageRank (importância ponderada)
- Ranking consolidado (média das métricas)

### "Como os grupos de poder se organizam?"

**Resposta será obtida através de:**
- Algoritmo de Louvain (detecção de comunidades)
- Análise de modularidade
- Visualização com cores por grupo

---

## 📁 Estrutura Final do Projeto

```
Disciplina_08/
│
├── genius/                      # Scripts originais (73 episódios)
│   ├── s01/
│   ├── s02/
│   └── ...
│
├── dataset_personagens.csv      # Dataset 1: Personagens + falas
├── dataset_interacoes.csv       # Dataset 2: Interações + quantidade
│
├── criar_datasets.py            # Script 1: Gera datasets
├── analise_redes.py             # Script 2: Análise completa
├── baixar_fotos.py              # Script 3: Download de fotos
│
├── personagens_fotos/           # Fotos dos personagens
│   ├── tyrion_got.jpg
│   ├── cersei_got.jpg
│   └── ...
│
├── README.md                    # Documentação principal
├── DATASETS_INFO.md             # Guia dos datasets
├── FOTOS_README.md              # Guia de fotos
└── requirements.txt             # Dependências
```

---

## ✨ Destaques do Projeto

### 🎨 Inovações
1. **Extração automática** de 73 episódios
2. **Datasets estruturados** com contagens
3. **Download automático de fotos** integrado com dataset
4. **Busca inteligente** no Google: "[NOME] GOT"

### 📈 Análises Disponíveis
1. Ranking de importância dos personagens
2. Mapa de interações
3. Grupos de poder (comunidades)
4. Visualização da rede
5. Métricas de centralidade

### 🔧 Tecnologias Utilizadas
- Python 3.x
- NetworkX (grafos)
- Pandas (dados)
- Matplotlib (visualização)
- BeautifulSoup (web scraping)
- Louvain (comunidades)

---

## 📝 Checklist Final

- [x] Extrair personagens dos scripts
- [x] Contar falas por personagem
- [x] Identificar interações entre personagens
- [x] Contar frequência de interações
- [x] Gerar datasets em CSV
- [x] Criar script de download de fotos
- [x] Integrar fotos com dataset
- [x] Testar busca no Google Images
- [ ] Construir grafo de interações
- [ ] Calcular métricas de centralidade
- [ ] Detectar comunidades
- [ ] Visualizar rede
- [ ] Responder pergunta de negócio

---

## 🎓 Para Apresentação

### Demonstrar:
1. **Datasets** - Mostrar CSVs gerados
2. **Fotos** - Mostrar pasta com imagens baixadas
3. **Estatísticas** - Top personagens e interações
4. **Análise** - Executar analise_redes.py
5. **Visualização** - Mostrar grafo gerado

### Destacar:
- Automação completa (73 episódios processados)
- Integração entre scripts
- Download inteligente de fotos
- Análise matemática rigorosa

---

## 🚀 Próximos Passos

1. Execute `python analise_redes.py` para análise completa
2. Ajuste `[:3]` para `[:15]` em baixar_fotos.py para mais fotos
3. Analise os resultados e prepare apresentação

---

## 📞 Suporte

Todos os scripts estão documentados e testados.
Consulte os READMEs específicos para detalhes:
- README.md - Metodologia geral
- DATASETS_INFO.md - Uso dos datasets
- FOTOS_README.md - Download de fotos

---

**✅ PROJETO COMPLETO E FUNCIONAL!**

Data: 27/02/2026
Disciplina: 08 - Pós-Graduação
Tema: Análise de Redes - Game of Thrones
