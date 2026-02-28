import os
import re
import pandas as pd
from collections import Counter, defaultdict

def extract_characters(genius_path):
    """Extrai todos os personagens únicos que falam"""
    characters = set()
    
    for season_folder in sorted(os.listdir(genius_path)):
        season_path = os.path.join(genius_path, season_folder)
        if not os.path.isdir(season_path) or not season_folder.startswith('s'):
            continue
        
        for episode_file in sorted(os.listdir(season_path)):
            if not episode_file.endswith('.txt'):
                continue
            
            episode_path = os.path.join(season_path, episode_file)
            
            with open(episode_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Padrão: PERSONAGEM:
            pattern = r'^([A-Z][A-Z\s\']+):\s'
            matches = re.findall(pattern, content, re.MULTILINE)
            
            for char in matches:
                char = char.strip()
                if len(char) > 1:  # Evita iniciais soltas
                    characters.add(char)
    
    return sorted(characters)

def main():
    genius_path = 'genius'
    
    print("=" * 80)
    print("EXTRACAO DE DATASETS - GAME OF THRONES")
    print("=" * 80)
    
    # Dataset 1: Personagens com contagem de falas
    print("\n[1] Extraindo personagens e contando falas...")
    characters = extract_characters(genius_path)
    speech_counts = count_character_speeches(genius_path)
    
    df_characters = pd.DataFrame([
        {'personagem': char, 'quantidade_falas': speech_counts[char]}
        for char in characters
    ])
    
    # Ordena por quantidade de falas
    df_characters = df_characters.sort_values('quantidade_falas', ascending=False).reset_index(drop=True)
    
    df_characters.to_csv('dataset_personagens.csv', index=False, encoding='utf-8')
    print(f"   [OK] {len(characters)} personagens encontrados")
    print(f"   Salvo em: dataset_personagens.csv")
    
    # Mostra top 10
    print("\n   Top 10 personagens que mais falam:")
    for i, row in df_characters.head(10).iterrows():
        print(f"      {i+1:2}. {row['personagem']:30} - {row['quantidade_falas']:4} falas")
    
    # Dataset 2: Interações com contagem
    print("\n[2] Extraindo interacoes e contando...")
    interactions = extract_interactions_with_count(genius_path)
    
    df_interactions = pd.DataFrame(interactions)
    
    # Ordena por quantidade de interações
    df_interactions = df_interactions.sort_values('quantidade_interacoes', ascending=False).reset_index(drop=True)
    
    df_interactions.to_csv('dataset_interacoes.csv', index=False, encoding='utf-8')
    print(f"   [OK] {len(interactions)} pares de interacao encontrados")
    print(f"   Total de interacoes: {df_interactions['quantidade_interacoes'].sum()}")
    print(f"   Salvo em: dataset_interacoes.csv")
    
    # Estatísticas
    print("\n" + "=" * 80)
    print("ESTATISTICAS")
    print("=" * 80)
    
    # Top 10 pares de interação
    print("\nTop 10 pares de interacao (quem fala mais com quem):")
    for i, row in df_interactions.head(10).iterrows():
        print(f"   {i+1:2}. {row['personagem_1']:20} <-> {row['personagem_2']:20} - {row['quantidade_interacoes']:4}x")
    
    # Amostra do dataset de interações
    print("\nAmostra do dataset de interacoes (primeiras 5 linhas):")
    print(df_interactions.head().to_string(index=False))
    
    print("\n" + "=" * 80)
    print("DATASETS CRIADOS COM SUCESSO!")
    print("=" * 80)
    print("\nArquivos gerados:")
    print("  1. dataset_personagens.csv  - Lista de personagens com quantidade de falas")
    print("  2. dataset_interacoes.csv   - Pares de interacoes com quantidade")

if __name__ == '__main__':
    main()
