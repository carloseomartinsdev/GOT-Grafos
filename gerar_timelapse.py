import pandas as pd
import json

print("Carregando dados...")
df = pd.read_csv('dataset_interacoes_personagens.csv', low_memory=False)

# Filtrar personagens genéricos
excluir = ['ALL', 'Voice', 'Voices', 'GUARD', 'GUARDS', 'MAN', 'WOMAN', 'SOLDIER', 'SOLDIERS', 'CROWD']
df = df[~df['falante_oficial'].str.lower().str.contains('|'.join([e.lower() for e in excluir]), na=False)]
df = df[~df['ouvinte_oficial'].str.lower().str.contains('|'.join([e.lower() for e in excluir]), na=False)]

print("Calculando personagens por episódio com tracking...")

episodios_data = []
ultimo_episodio_por_personagem = {}
episodio_index = 0

for (temp, ep), group in df.groupby(['temporada', 'episodio']):
    personagens_episodio = set(group['falante_oficial'].unique()) | set(group['ouvinte_oficial'].dropna().unique())
    
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
with open('timelapse_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado com sucesso!")
print(f"   - {len(episodios_data)} episódios processados")
print(f"   - Personagens somem após 5 episódios sem aparecer")
