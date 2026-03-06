# Game of Thrones - Análise de Interações entre Personagens

Projeto de análise de dados dos scripts de Game of Thrones, gerando datasets de personagens e suas interações ao longo das 8 temporadas.

## 📋 Descrição

Este projeto processa os scripts completos de Game of Thrones para:
- Identificar todos os personagens e contar suas falas
- Mapear variações de nomes e famílias usando IA
- Gerar dataset completo de interações entre personagens
- Classificar tipos de interação (direta, grupo, co-ocorrência)

## 🚀 Início Rápido

### Pré-requisitos
```bash
# Bibliotecas básicas
pip install pandas requests

# Para visualização de grafos
pip install networkx matplotlib
```

### Execução
```bash
# 1. Extrair personagens
python criar_dataset_personagens.py

# 2. Identificar duplicados e famílias (requer API Key DeepSeek)
python identificar_duplicados.py

# 3. Gerar interações
python criar_dataset_interacoes.py

# 4. Criar e visualizar grafo de interações
python criar_grafo.py
```

## 📊 Datasets Gerados

### 1. dataset_personagens.csv
Lista de personagens com contagem de falas
- `personagem`: Nome do personagem
- `quantidade_falas`: Número total de falas

### 2. personagens_dicionario.csv
Mapeamento de nomes, variações e famílias
- `Nome`: Nome principal completo
- `Variações`: Apelidos/variações separados por vírgula
- `Familia`: Família ou grupo (Stark, Lannister, etc)

### 3. dataset_interacoes_personagens.csv
Dataset completo de interações (500k+ registros)
- `temporada`: Temporada (1-8)
- `episodio`: Número do episódio
- `cena`: Número da cena
- `descricao_cena`: Descrição da cena
- `falante_oficial`: Quem fala
- `ouvinte_oficial`: Quem ouve
- `fala`: Texto da fala
- `tamanho_fala`: Comprimento da fala
- `num_personagens_cena`: Personagens na cena
- `tipo_interacao`: Tipo (direct/group/scene_cooccurrence)

## 🔍 Tipos de Interação

- **direct**: Diálogo direto entre 2 personagens
- **group**: Fala para múltiplos personagens
- **scene_cooccurrence**: Co-ocorrência na mesma cena

## 📁 Estrutura do Projeto

```
Disciplina_08/
├── genius/                          # Scripts originais (s01-s08)
├── criar_dataset_personagens.py     # Extrai personagens
├── identificar_duplicados.py        # Identifica variações (IA)
├── criar_dataset_interacoes.py      # Gera interações
├── criar_grafo.py                   # Cria e visualiza grafo
├── converter_dicionario.py          # Utilitário de conversão
├── dataset_personagens.csv          # Output 1
├── personagens_dicionario.csv       # Output 2
├── dataset_interacoes_personagens.csv # Output 3
├── GUIA_INICIALIZACAO.md           # Guia detalhado
└── README.md                        # Este arquivo
```

## 🤖 IA - DeepSeek

O projeto usa a API do DeepSeek para:
- Identificar variações de nomes automaticamente
- Classificar personagens por família/grupo
- Reduzir duplicatas e inconsistências

**Obtenha sua API Key:** https://platform.deepseek.com/

## 📖 Documentação Adicional

- [GUIA_INICIALIZACAO.md](GUIA_INICIALIZACAO.md) - Passo a passo detalhado
- [DATASETS_INFO.md](DATASETS_INFO.md) - Informações sobre os datasets
- [DATASET_INTERACOES.md](DATASET_INTERACOES.md) - Detalhes das interações

## 🛠️ Troubleshooting

### Erro de conexão DeepSeek
- Verifique conexão com internet
- Confirme API Key válida
- Use DNS público (8.8.8.8)

### KeyError em colunas
- Execute os scripts na ordem correta
- Certifique-se que `personagens_dicionario.csv` tem colunas: Nome, Variações, Familia

### Encoding error
- Use UTF-8 em todos os arquivos
- Windows: execute `chcp 65001` no CMD

## 📊 Estatísticas

- **Personagens únicos**: ~375
- **Total de interações**: ~500.000
- **Temporadas**: 8
- **Episódios**: 73

## 🎯 Casos de Uso

- Análise de redes sociais
- Visualização de grafos de personagens
- Análise de sentimento
- Estudo de protagonismo
- Machine Learning em narrativas

## 📊 Visualização do Grafo

O script `criar_grafo.py` gera uma visualização interativa mostrando:
- **Nós**: Personagens (tamanho = importância por peso de interações)
- **Arestas**: Interações diretas (espessura = frequência)
- **Cores**: Gradiente de importância (amarelo → vermelho)
- **Top 20 personagens** com interações mais significativas

Personalize a visualização editando os parâmetros:
```python
G_top = subgrafo_top_personagens(G, 30)  # Top 30 ao invés de 20
visualizar_grafo(G_top, peso_minimo_label=50)  # Mostrar apenas pesos ≥ 50
```

## 📝 Licença

Projeto acadêmico - Disciplina 08

## 👥 Contribuições

Sugestões e melhorias são bem-vindas!
