# ✅ CORREÇÃO APLICADA: Removido filtro de tipo_interacao

## Mudança no Notebook:

### ❌ ANTES (linha 2 da célula de carregamento):
```python
df = pd.read_csv("../datasets/interacoes.csv")
df_direct = df[df["tipo_interacao"] == "single"]  # ❌ Filtro desnecessário
df_grouped = df_direct.groupby(['falante', 'ouvinte']).size().reset_index(name='weight')
```

### ✅ DEPOIS (correto):
```python
df = pd.read_csv("../datasets/interacoes.csv")
df_grouped = df.groupby(['falante', 'ouvinte']).size().reset_index(name='weight')
```

## Resultado:
- Agora usa TODAS as 27K interações
- Grafo completo e mais representativo
- Rankings mais precisos

Execute o notebook novamente para ver os resultados com o dataset completo!
