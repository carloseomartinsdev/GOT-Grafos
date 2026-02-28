import os
import re
import csv
from collections import Counter

def extrair_personagens(genius_path):
    """Extrai todos os personagens únicos dos scripts"""
    personagens = Counter()
    
    for season_folder in sorted(os.listdir(genius_path)):
        season_path = os.path.join(genius_path, season_folder)
        if not os.path.isdir(season_path):
            continue
        
        for episode_file in sorted(os.listdir(season_path)):
            if not episode_file.endswith('.txt') or not episode_file.startswith('got_'):
                continue
            
            episode_path = os.path.join(season_path, episode_file)
            
            with open(episode_path, 'r', encoding='utf-8') as f:
                for linha in f:
                    match = re.match(r'^([A-Z][A-Z\s\'\-]+):', linha)
                    if match:
                        personagem = match.group(1).strip()
                        personagens[personagem] += 1
    
    return personagens

def agrupar_variacoes(personagens):
    """Agrupa variações do mesmo personagem"""
    bloqueados = [
        'CUT TO', 'INT', 'EXT', 'FADE', 'CREDITS', 'MAIN CREDITS',
        'TITLE SEQUENCE', 'BLACKOUT', 'FADE OUT', 'FADE IN',
        'OPENING CREDITS', 'END CREDITS', 'SCENE', 'ACT'
    ]
    
    grupos = {}
    
    for personagem, qtd in personagens.most_common():
        if personagem in bloqueados:
            continue
        
        if re.match(r'^(GUARD|SOLDIER|MAN|WOMAN|BOY|GIRL|CHILD)\s*\d*$', personagem):
            continue
        
        # Procura por nome principal (mais longo ou mais frequente)
        encontrado = False
        for principal, variacoes in grupos.items():
            # Verifica se é variação
            if personagem in principal or principal in personagem:
                if len(personagem) > len(principal):
                    # Troca principal
                    grupos[personagem] = variacoes + [principal]
                    del grupos[principal]
                else:
                    grupos[principal].append(personagem)
                encontrado = True
                break
            
            # Verifica por palavras em comum
            palavras_pers = set(personagem.split())
            palavras_princ = set(principal.split())
            if palavras_pers & palavras_princ and len(palavras_pers & palavras_princ) > 0:
                # Tem palavras em comum
                if 'THE' not in palavras_pers and 'THE' not in palavras_princ:
                    if len(personagem) > len(principal):
                        grupos[personagem] = variacoes + [principal]
                        del grupos[principal]
                    else:
                        grupos[principal].append(personagem)
                    encontrado = True
                    break
        
        if not encontrado:
            grupos[personagem] = []
    
    return grupos

def main():
    genius_path = 'genius'
    
    print('Extraindo personagens dos scripts...')
    personagens = extrair_personagens(genius_path)
    print(f'Total de nomes encontrados: {len(personagens)}')
    
    print('\nAgrupando variações...')
    grupos = agrupar_variacoes(personagens)
    
    # Salva dicionário
    with open('personagens_dicionario.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['NOME_PRINCIPAL', 'APELIDOS'])
        
        for principal in sorted(grupos.keys()):
            variacoes = grupos[principal]
            if variacoes:
                apelidos = '|'.join(sorted(set(variacoes)))
                writer.writerow([principal, apelidos])
            else:
                writer.writerow([principal, principal])
    
    print(f'\nDicionário criado com {len(grupos)} personagens!')
    print('\nExemplos de agrupamentos:')
    count = 0
    for principal, variacoes in sorted(grupos.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        if variacoes:
            print(f'  {principal}: {", ".join(variacoes)}')
            count += 1

if __name__ == '__main__':
    main()
