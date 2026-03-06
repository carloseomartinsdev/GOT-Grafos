import pandas as pd

print("="*60)
print("CRIADOR DE DICIONÁRIO MANUAL - GoT")
print("="*60)

# Carrega dataset
df = pd.read_csv('dataset_personagens.csv')
exclude = ['CUT TO', 'INT', 'EXT', 'MAN', 'WOMAN', 'ALL', 'MEN', 'WOMEN', 'CROWD']
df_filtered = df[~df['personagem'].isin(exclude)]

# Dicionário pré-preenchido com personagens principais
dicionario = {
    'TYRION LANNISTER': {'variacoes': 'TYRION,IMP,HALFMAN', 'familia': 'Lannister'},
    'JON SNOW': {'variacoes': 'JON,SNOW', 'familia': 'Stark/Night\'s Watch'},
    'DAENERYS TARGARYEN': {'variacoes': 'DAENERYS,DANY,KHALEESI', 'familia': 'Targaryen'},
    'CERSEI LANNISTER': {'variacoes': 'CERSEI', 'familia': 'Lannister'},
    'ARYA STARK': {'variacoes': 'ARYA', 'familia': 'Stark'},
    'SANSA STARK': {'variacoes': 'SANSA', 'familia': 'Stark'},
    'JAIME LANNISTER': {'variacoes': 'JAIME', 'familia': 'Lannister'},
    'NED STARK': {'variacoes': 'NED,EDDARD,EDDARD STARK', 'familia': 'Stark'},
    'BRAN STARK': {'variacoes': 'BRAN,BRANDON', 'familia': 'Stark'},
    'CATELYN STARK': {'variacoes': 'CATELYN,CAT', 'familia': 'Stark'},
    'ROBB STARK': {'variacoes': 'ROBB', 'familia': 'Stark'},
    'THEON GREYJOY': {'variacoes': 'THEON', 'familia': 'Greyjoy'},
    'JOFFREY BARATHEON': {'variacoes': 'JOFFREY', 'familia': 'Baratheon'},
    'ROBERT BARATHEON': {'variacoes': 'ROBERT', 'familia': 'Baratheon'},
    'STANNIS BARATHEON': {'variacoes': 'STANNIS', 'familia': 'Baratheon'},
    'SANDOR CLEGANE': {'variacoes': 'SANDOR,HOUND,THE HOUND', 'familia': 'Clegane'},
    'PETYR BAELISH': {'variacoes': 'PETYR,LITTLEFINGER', 'familia': 'Baelish'},
    'VARYS': {'variacoes': 'SPIDER', 'familia': 'Independent'},
    'SAMWELL TARLY': {'variacoes': 'SAM,SAMWELL', 'familia': 'Night\'s Watch'},
    'JORAH MORMONT': {'variacoes': 'JORAH', 'familia': 'Mormont'},
    'BRIENNE OF TARTH': {'variacoes': 'BRIENNE', 'familia': 'Tarth'},
    'DAVOS SEAWORTH': {'variacoes': 'DAVOS', 'familia': 'Seaworth'},
    'MELISANDRE': {'variacoes': 'RED WOMAN', 'familia': 'Red Priestess'},
    'MARGAERY TYRELL': {'variacoes': 'MARGAERY', 'familia': 'Tyrell'},
    'TYWIN LANNISTER': {'variacoes': 'TYWIN', 'familia': 'Lannister'},
}

# Adiciona personagens restantes
for personagem in df_filtered['personagem']:
    if personagem not in dicionario:
        dicionario[personagem] = {'variacoes': '', 'familia': 'Unknown'}

# Salva CSV
with open('personagens_dicionario.csv', 'w', encoding='utf-8') as f:
    f.write('Nome,Variações,Familia\n')
    for nome, info in dicionario.items():
        f.write(f'"{nome}","{info["variacoes"]}","{info["familia"]}"\n')

print(f"\n✓ Dicionário criado com {len(dicionario)} personagens")
print("✓ Salvo em: personagens_dicionario.csv")
print("\nVocê pode editar o CSV manualmente para adicionar mais variações.")
