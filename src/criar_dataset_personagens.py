import os
import re
import csv
from collections import Counter

def extrair_personagens_falas(genius_path):
    """Extrai personagens e conta suas falas"""
    contador_falas = Counter()
    
    for season_folder in sorted(os.listdir(genius_path)):
        season_path = os.path.join(genius_path, season_folder)
        if not os.path.isdir(season_path):
            continue
        
        for episode_file in sorted(os.listdir(season_path)):
            if not episode_file.endswith('.txt') or not episode_file.startswith('got_'):
                continue
            
            episode_path = os.path.join(season_path, episode_file)
            print(f'Processando {episode_file}...')
            
            with open(episode_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    match = re.match(r'^([A-Z][A-Z\s\'\-]+):', linha)
                    if match:
                        personagem = match.group(1).strip()
                        contador_falas[personagem] += 1
    
    return contador_falas

def main():
    genius_path = 'genius'
    
    print('Extraindo personagens e contando falas...\n')
    contador_falas = extrair_personagens_falas(genius_path)
    
    # Tenta carregar dicionário (opcional - só existe após passo 2)
    mapa_nomes = {}
    import os
    if os.path.exists('datasets/personagens_dicionario.csv'):
        print('\nDicionário encontrado! Normalizando nomes...')
        with open('datasets/personagens_dicionario.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                oficial = row['Nome']
                mapa_nomes[oficial] = oficial
                if row['Variações']:
                    for apelido in row['Variações'].split(', '):
                        mapa_nomes[apelido.strip()] = oficial
    else:
        print('\nDicionário não encontrado (será criado no passo 2)')
    
    # Agrupa falas por nome oficial (se dicionário existir)
    contador_oficial = Counter()
    for personagem, qtd in contador_falas.items():
        nome_oficial = mapa_nomes.get(personagem, personagem)
        contador_oficial[nome_oficial] += qtd
    
    # Cria pasta datasets se não existir
    os.makedirs('datasets', exist_ok=True)
    
    # Salva dataset
    with open('datasets/dataset_personagens.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['personagem', 'quantidade_falas'])
        for personagem, qtd in contador_oficial.most_common():
            writer.writerow([personagem, qtd])
    
    print(f'\nDataset criado com {len(contador_oficial)} personagens!')
    print(f'Total de falas: {sum(contador_oficial.values()):,}')
    print('\nTop 10 personagens:')
    for i, (pers, qtd) in enumerate(contador_oficial.most_common(10), 1):
        print(f'{i:2}. {pers:30} - {qtd:4} falas')

if __name__ == '__main__':
    main()
