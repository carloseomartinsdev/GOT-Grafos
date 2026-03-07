import pandas as pd
import json

print("Carregando dados...")
df = pd.read_csv('datasets/interacoes.csv', low_memory=False)
df_dicionario = pd.read_csv('datasets/personagens_dicionario.csv')

# Criar mapeamento de variações para nome oficial
nome_oficial_map = {}
for _, row in df_dicionario.iterrows():
    oficial = row['NOME_OFICIAL'].upper()
    nome_oficial_map[oficial] = oficial
    for var in str(row['VARIACOES']).split('|'):
        nome_oficial_map[var.strip().upper()] = oficial

# Normalizar nomes
df['falante'] = df['falante'].str.strip().str.upper().map(lambda x: nome_oficial_map.get(x, x))
df['ouvinte'] = df['ouvinte'].str.strip().str.upper().map(lambda x: nome_oficial_map.get(x, x))

print("Calculando personagens por episódio com tracking...")

episodios_data = []
ultimo_episodio_por_personagem = {}
episodio_index = 0

for (temp, ep), group in df.groupby(['NTemporada', 'NEpisodio']):
    personagens_episodio = set(group['falante'].unique()) | set(group['ouvinte'].dropna().unique())
    
    # Atualizar último episódio de cada personagem
    for p in personagens_episodio:
        ultimo_episodio_por_personagem[p] = episodio_index
    
    # Personagens visíveis = apareceram nos últimos 5 episódios
    personagens_visiveis = set()
    for p, last_ep in ultimo_episodio_por_personagem.items():
        if episodio_index - last_ep <= 5:
            personagens_visiveis.add(p)
    
    episodios_data.append({
        'temporada': int(temp),
        'episodio': int(ep),
        'personagens_ativos': list(personagens_episodio),
        'personagens_visiveis': list(personagens_visiveis),
        'todos_personagens': list(ultimo_episodio_por_personagem.keys())
    })
    
    episodio_index += 1

# Ordenar por temporada e episódio
episodios_data.sort(key=lambda x: (x['temporada'], x['episodio']))

# Salvar
output = {'episodios': episodios_data}

print("Salvando timelapse_data.json...")
with open('public/resources/jsons/timelapse_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado com sucesso!")
print(f"   - {len(episodios_data)} episódios processados")
print(f"   - Personagens somem após 5 episódios sem aparecer")
