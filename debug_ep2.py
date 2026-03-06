import re

with open('genius/s01/got_s01e02.txt', 'r', encoding='utf-8') as f:
    texto = f.read()

# Remove separadores
texto = re.sub(r'^[\s-]+$', '', texto, flags=re.MULTILINE)

linhas = texto.split('\n')
cenas = []
cena_atual = []
personagens_cena = set()
num_cena = 0
descricao_cena = ''

def extrair_personagem(linha):
    match = re.match(r'^([A-Z][A-Za-z\s\'\-]+):', linha)
    if not match:
        return None
    personagem = match.group(1).strip().upper()
    bloqueados = ['CUT TO', 'INT', 'EXT', 'FADE', 'CREDITS', 'MAIN CREDITS', 'TITLE SEQUENCE', 'BLACKOUT', 'FADE OUT', 'FADE IN', 'OPENING CREDITS', 'END CREDITS', 'SCENE', 'ACT']
    if personagem in bloqueados:
        return None
    if re.match(r'^(GUARD|SOLDIER|MAN|WOMAN|BOY|GIRL|CHILD)\s*\d*$', personagem):
        return None
    return personagem

for i, linha in enumerate(linhas):
    linha_stripped = linha.strip()
    if not linha_stripped:
        continue
    
    if linha_stripped.startswith('EPISODE'):
        print(f"Linha {i}: IGNORADO (título) - {linha_stripped[:50]}")
        continue
    
    if ':' in linha_stripped:
        personagem = extrair_personagem(linha_stripped)
        if personagem:
            personagens_cena.add(personagem)
            cena_atual.append((personagem, linha_stripped))
            print(f"Linha {i}: FALA - {personagem}")
        else:
            print(f"Linha {i}: FALA IGNORADA - {linha_stripped[:50]}")
    else:
        if cena_atual:
            cenas.append((num_cena, list(personagens_cena), cena_atual, descricao_cena))
            print(f"Linha {i}: NOVA CENA (salvou cena {num_cena} com {len(cena_atual)} falas)")
            num_cena += 1
        else:
            print(f"Linha {i}: NOVA CENA (descartou cena sem falas)")
        cena_atual = []
        personagens_cena = set()
        descricao_cena = linha_stripped
        print(f"         Descrição: {descricao_cena[:50]}")

if cena_atual:
    cenas.append((num_cena, list(personagens_cena), cena_atual, descricao_cena))
    print(f"FIM: Salvou última cena {num_cena} com {len(cena_atual)} falas")

print(f"\n=== TOTAL: {len(cenas)} cenas ===")
input('\nPressione ENTER para fechar...')
