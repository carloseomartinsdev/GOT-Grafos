import os
import re
import csv

def extrair_personagem(linha):
    match = re.match(r'^([A-Z][A-Za-z\s\'\-]+):', linha)
    if not match:
        return None
    
    personagem = match.group(1).strip().upper()
    
    # Lista de termos que não são personagens
    bloqueados = [
        'CUT TO', 'INT', 'EXT', 'FADE', 'CREDITS', 'MAIN CREDITS',
        'TITLE SEQUENCE', 'BLACKOUT', 'FADE OUT', 'FADE IN',
        'OPENING CREDITS', 'END CREDITS', 'SCENE', 'ACT'
    ]
    
    if personagem in bloqueados:
        return None
    
    # Bloqueia padrões genéricos
    if re.match(r'^(GUARD|SOLDIER|MAN|WOMAN|BOY|GIRL|CHILD)\s*\d*$', personagem):
        return None
    
    return personagem

def extrair_cena_personagens(texto):
    linhas = texto.split('\n')
    cenas = []
    cena_atual = []
    personagens_cena = set()
    num_cena = 0
    descricao_cena = ''
    
    for linha in linhas:
        linha_stripped = linha.strip()
        if not linha_stripped:
            continue
        
        # Ignora título do episódio
        if linha_stripped.startswith('EPISODE'):
            continue
        
        # Detecta fala (tem ':')
        if ':' in linha_stripped:
            personagem = extrair_personagem(linha_stripped)
            if personagem:
                personagens_cena.add(personagem)
                cena_atual.append((personagem, linha_stripped))
        else:
            # Texto sem ':' = nova cena
            if cena_atual:  # Só salva se teve falas
                cenas.append((num_cena, list(personagens_cena), cena_atual, descricao_cena))
                num_cena += 1
            cena_atual = []
            personagens_cena = set()
            descricao_cena = linha_stripped
    
    if cena_atual:
        cenas.append((num_cena, list(personagens_cena), cena_atual, descricao_cena))
    
    return cenas

def processar_episodio(caminho_arquivo, mapa_nomes, personagens_validos):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    # Remove separadores visuais
    texto = re.sub(r'^[\s-]+$', '', texto, flags=re.MULTILINE)
    
    nome_arquivo = os.path.basename(caminho_arquivo)
    match = re.match(r'got_s(\d+)e(\d+)', nome_arquivo)
    temporada = match.group(1) if match else '00'
    episodio = match.group(2) if match else '00'
    
    cenas = extrair_cena_personagens(texto)
    interacoes = []
    
    for num_cena, personagens_cena, dialogos, descricao_cena in cenas:
        personagens_oficiais = []
        for p in personagens_cena:
            p_oficial = mapa_nomes.get(p, p)
            if p_oficial in personagens_validos:
                personagens_oficiais.append(p_oficial)
        
        personagens_oficiais = list(set(personagens_oficiais))
        
        for i, (falante, fala_completa) in enumerate(dialogos):
            fala_texto = fala_completa.split(':', 1)[1].strip() if ':' in fala_completa else ''
            tamanho_fala = len(fala_texto)
            
            falante_oficial = mapa_nomes.get(falante, falante)
            if falante_oficial not in personagens_validos:
                continue
            
            ouvintes_oficiais = [p for p in personagens_oficiais if p != falante_oficial]
            
            # Classificar tipo de interação
            tipo_interacao = 'scene_cooccurrence'
            if len(ouvintes_oficiais) == 1:
                tipo_interacao = 'direct'
            elif len(ouvintes_oficiais) > 1:
                tipo_interacao = 'group'
            
            for ouvinte_oficial in ouvintes_oficiais:
                interacoes.append({
                    'temporada': temporada,
                    'episodio': episodio,
                    'cena': num_cena,
                    'descricao_cena': descricao_cena,
                    'falante_oficial': falante_oficial,
                    'ouvinte_oficial': ouvinte_oficial,
                    'fala': fala_texto,
                    'tamanho_fala': tamanho_fala,
                    'num_personagens_cena': len(personagens_oficiais),
                    'tipo_interacao': tipo_interacao
                })
    
    return interacoes, len(cenas)

def main():
    mapa_nomes = {}
    personagens_validos = set()
    
    # Carrega dicionário - mapeia variações para nome oficial
    with open('datasets/personagens_dicionario.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            oficial = row['Nome'].upper()
            personagens_validos.add(oficial)
            
            # Mapeia cada variação para o nome oficial
            if row['Variações']:
                for variacao in row['Variações'].split(', '):
                    mapa_nomes[variacao.strip()] = oficial
    
    # Adiciona personagens do dataset que não estão no dicionário
    with open('datasets/dataset_personagens.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            personagem = row['personagem']
            if personagem not in mapa_nomes:
                personagens_validos.add(personagem)
                mapa_nomes[personagem] = personagem
    
    pasta_genius = 'genius'
    todas_interacoes = []
    total_cenas = 0
    total_episodios = 0
    
    for temporada in sorted(os.listdir(pasta_genius)):
        caminho_temp = os.path.join(pasta_genius, temporada)
        if not os.path.isdir(caminho_temp):
            continue
        
        for arquivo in sorted(os.listdir(caminho_temp)):
            if arquivo.endswith('.txt') and arquivo.startswith('got_'):
                caminho_completo = os.path.join(caminho_temp, arquivo)
                print(f'Processando {arquivo}...')
                interacoes, num_cenas = processar_episodio(caminho_completo, mapa_nomes, personagens_validos)
                todas_interacoes.extend(interacoes)
                total_cenas += num_cenas
                total_episodios += 1
                print(f'  -> {num_cenas} cenas, {len(interacoes)} interações')
    
    with open('datasets/dataset_interacoes_personagens.csv', 'w', newline='', encoding='utf-8') as f:
        campos = ['temporada', 'episodio', 'cena', 'descricao_cena', 'falante_oficial', 'ouvinte_oficial', 'fala', 'tamanho_fala', 'num_personagens_cena', 'tipo_interacao']
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(todas_interacoes)
    
    print(f'\n=== RESUMO ===')
    print(f'Episódios processados: {total_episodios}')
    print(f'Total de cenas: {total_cenas}')
    print(f'Total de interações: {len(todas_interacoes)}')
    print(f'\nDataset salvo em: datasets/dataset_interacoes_personagens.csv')
    input('\nPressione ENTER para fechar...')

if __name__ == '__main__':
    main()
