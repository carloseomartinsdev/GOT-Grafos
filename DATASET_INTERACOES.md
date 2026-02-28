# Dataset de Interações entre Personagens - Game of Thrones

## Descrição

Script Python que processa os roteiros de Game of Thrones (formato Genius) e gera um dataset estruturado de interações entre personagens.

## Arquivo

`criar_dataset_interacoes.py`

## Funcionamento

### 1. Extração de Personagens
- Identifica personagens através de padrões `NOME:` no início das linhas
- Agrupa diálogos por cenas (detectadas por marcadores `[...]` ou "Scene")

### 2. Mapeamento de Nomes
- Carrega o dicionário de personagens (`personagens_dicionario.csv`)
- Normaliza variações de nomes para o nome oficial
- Exemplo: `JON`, `JOHN` → `JON SNOW`

### 3. Geração de Interações
Para cada fala em uma cena:
- **Falante**: quem está falando
- **Ouvintes**: todos os outros personagens presentes na cena
- **Bidirecional**: Se A fala com B e B responde, gera duas entradas (A→B e B→A)

### 4. Métricas Calculadas
- `tamanho_fala`: número de caracteres da fala
- `num_personagens_cena`: quantidade de personagens presentes

## Estrutura do Dataset

```csv
temporada,episodio,cena,falante_oficial,ouvinte_oficial,tamanho_fala,num_personagens_cena
01,01,0,WAYMAR ROYCE,WILL,136,4
01,01,0,WAYMAR ROYCE,YOHN ROYCE,136,4
```

### Colunas

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `temporada` | string | Número da temporada (01-08) |
| `episodio` | string | Número do episódio (01-10) |
| `cena` | int | Número sequencial da cena no episódio |
| `falante_oficial` | string | Nome oficial do personagem que fala |
| `ouvinte_oficial` | string | Nome oficial do personagem que ouve |
| `tamanho_fala` | int | Quantidade de caracteres da fala |
| `num_personagens_cena` | int | Total de personagens na cena |

## Estatísticas

- **Total de interações**: 750.527
- **Personagens únicos**: 389
- **Temporadas**: 8 (73 episódios)
- **Fonte**: Roteiros do Genius

## Uso

```bash
python criar_dataset_interacoes.py
```

### Saída
`dataset_interacoes_personagens.csv`

## Aplicações

- Análise de redes sociais
- Identificação de personagens centrais
- Evolução de relacionamentos ao longo das temporadas
- Análise de comunidades e grupos
- Métricas de centralidade (degree, betweenness, closeness)
