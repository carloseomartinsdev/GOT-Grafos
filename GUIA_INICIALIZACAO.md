# Guia de Inicialização - Datasets Game of Thrones

## Pré-requisitos
- Python 3.x instalado
- Bibliotecas: `pandas`, `requests`
- API Key do DeepSeek (https://platform.deepseek.com/)
- Scripts de Game of Thrones na pasta `genius/`

## Passo a Passo

### 1. Criar Dataset de Personagens
**Arquivo:** `criar_dataset_personagens.py`  
**Função:** Extrai todos os personagens e conta suas falas

```bash
python criar_dataset_personagens.py
```

**Saída:** `dataset_personagens.csv`
- Colunas: `personagem`, `quantidade_falas`

---

### 2. Identificar Duplicados e Famílias
**Arquivo:** `identificar_duplicados.py`  
**Função:** Usa DeepSeek AI para identificar variações de nomes e famílias

```bash
python identificar_duplicados.py
```

**Entrada necessária:**
- API Key do DeepSeek (será solicitada)
- Escolher formato de saída (CSV recomendado - opção 3)

**Saída:** `personagens_dicionario.csv`
- Colunas: `Nome`, `Variações`, `Familia`

---

### 3. Criar Dataset de Interações
**Arquivo:** `criar_dataset_interacoes.py`  
**Função:** Gera dataset completo de interações entre personagens

```bash
python criar_dataset_interacoes.py
```

**Requisito:** `personagens_dicionario.csv` deve existir

**Saída:** `dataset_interacoes_personagens.csv`
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

---

## Ordem de Execução Completa

```bash
# 1. Extrair personagens
python criar_dataset_personagens.py

# 2. Identificar duplicados e famílias (requer API Key)
python identificar_duplicados.py

# 3. Gerar interações
python criar_dataset_interacoes.py
```

---

## Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `dataset_personagens.csv` | Lista de personagens com contagem de falas |
| `personagens_dicionario.csv` | Mapeamento de nomes, variações e famílias |
| `dataset_interacoes_personagens.csv` | Dataset completo de interações |
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
