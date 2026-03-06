# Guia de Inicialização - Datasets Game of Thrones

## Pré-requisitos
- Python 3.x instalado
- Bibliotecas: `pandas`, `requests`, `networkx`, `matplotlib`
- API Key do DeepSeek (https://platform.deepseek.com/)
- Scripts de Game of Thrones na pasta `genius/`

## Passo a Passo

### 1. Criar Dataset de Personagens
**Arquivo:** `src/criar_dataset_personagens.py`  
**Função:** Extrai todos os personagens e conta suas falas

```bash
python src/criar_dataset_personagens.py
```

**Saída:** `datasets/dataset_personagens.csv`
- Colunas: `personagem`, `quantidade_falas`

---

### 2. Identificar Duplicados e Famílias
**Arquivo:** `src/identificar_duplicados.py`  
**Função:** Usa DeepSeek AI para identificar variações de nomes e famílias

```bash
python src/identificar_duplicados.py
```

**Entrada necessária:**
- API Key do DeepSeek (será solicitada)
- Escolher formato de saída (CSV recomendado - opção 3)

**Saída:** `datasets/personagens_dicionario.csv`
- Colunas: `Nome`, `Variações`, `Familia`

---

### 3. Criar Dataset de Interações
**Arquivo:** `src/criar_dataset_interacoes.py`  
**Função:** Gera dataset completo de interações entre personagens

```bash
python src/criar_dataset_interacoes.py
```

**Requisito:** `datasets/personagens_dicionario.csv` deve existir

**Saída:** `datasets/dataset_interacoes_personagens.csv`
- Colunas:
  - `temporada`
  - `episodio`
  - `cena`
  - `descricao_cena`
  - `falante_oficial`
  - `ouvinte_oficial`
  - `fala`
  - `tamanho_fala`
  - `num_personagens_cena`
  - `tipo_interacao` (direct/group/scene_cooccurrence)

### 4. Criar e Visualizar Grafo
**Arquivo:** `src/criar_grafo.py`  
**Função:** Cria grafo de interações e gera visualização

```bash
python src/criar_grafo.py
```

**Requisito:** `datasets/dataset_interacoes_personagens.csv` deve existir

**Saída:** Visualização interativa do grafo (matplotlib)
- Nós: Personagens (tamanho = peso das interações)
- Arestas: Interações diretas (espessura = frequência)
- Cores: Gradiente de importância (amarelo → vermelho)

---

## Ordem de Execução Completa

```bash
# 1. Extrair personagens
python src/criar_dataset_personagens.py

# 2. Identificar duplicados e famílias (requer API Key)
python src/identificar_duplicados.py

# 3. Gerar interações
python src/criar_dataset_interacoes.py

# 4. Criar e visualizar grafo
python src/criar_grafo.py
```

---

## Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `datasets/dataset_personagens.csv` | Lista de personagens com contagem de falas |
| `datasets/personagens_dicionario.csv` | Mapeamento de nomes, variações e famílias |
| `datasets/dataset_interacoes_personagens.csv` | Dataset completo de interações |
| `resposta_deepseek.txt` | Resposta bruta da API (debug) |

---

## Tipos de Interação

- **direct**: Diálogo entre 2 personagens (1 falante + 1 ouvinte)
- **group**: Fala para múltiplos personagens (1 falante + vários ouvintes)
- **scene_cooccurrence**: Personagens na mesma cena sem interação direta

---

## Troubleshooting

### Erro de conexão com DeepSeek
- Verifique sua conexão com internet
- Confirme se a API Key está correta
- Tente usar DNS público (8.8.8.8)

### Arquivo não encontrado
- Certifique-se de executar os scripts na ordem correta
- Verifique se a pasta `genius/` existe com os scripts

### Encoding error
- Todos os arquivos usam UTF-8
- No Windows, use `chcp 65001` no CMD antes de executar
