# Guia de Inicialização - Site Público

Este documento descreve o passo a passo para gerar os arquivos necessários para o funcionamento do site na pasta `public/`.

## Pré-requisitos

Antes de executar os scripts desta seção, certifique-se de ter completado os passos do [initialize.md](../initialize.md) principal:
1. Extrair personagens
2. Identificar duplicados (dicionário)
3. Extrair interações

## Passo 0: Baixar Fotos dos Personagens (Opcional)

Baixa fotos dos personagens principais para exibição no site.

### Comando
```bash
python src\site\baixar_fotos.py
```

### O que faz
- Lê o dicionário de personagens
- Busca fotos dos personagens principais
- Salva as imagens em `public/resources/imagens/personagens/`

### Observação
Este passo é opcional e independente dos demais. O site funciona sem as fotos.

---

## Passo 1: Gerar Dados do Grafo

Gera o arquivo JSON com os dados do grafo de interações para visualização.

### Comando
```bash
python src\site\00_inicializar_site.py
```

Ou executar individualmente:
```bash
python src\site\01_gerar_dados_grafo.py
python src\site\02_gerar_interactions_index.py
python src\site\03_gerar_eventos.py
python src\site\04_gerar_timelapse.py
```

### O que faz
- Gera todos os arquivos JSON necessários para o site
- Calcula métricas de centralidade dos personagens
- Cria estrutura de nós e arestas para o grafo
- Indexa interações por episódio
- Identifica eventos importantes
- Gera dados para visualização temporal

### Arquivos de saída
- `public/resources/jsons/graph_data.json` - Dados do grafo para visualização D3.js
- `public/resources/jsons/interactions_index.json` - Índice de interações
- `public/resources/jsons/eventos_importantes.json` - Lista de eventos marcantes
- `public/resources/jsons/timelapse_data.json` - Dados para visualização temporal

---

## Executando o Site

Após gerar todos os arquivos, inicie o servidor local:

```bash
python src\site\servidor.py
```

Acesse: `http://localhost:8000`
