import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
import time

def download_from_google(char_name):
    """Busca '[nome] GOT' no Google Images e baixa primeira foto"""
    
    # Verifica se foto já existe
    filename = f"personagens_fotos/{char_name.replace(' ', '_').replace('/', '_')}.jpg"
    if os.path.exists(filename):
        return 'exists'
    
    try:
        # Monta URL de busca do Google Images
        search_query = f"{char_name} GOT"
        url = f"https://www.google.com/search?q={search_query}&tbm=isch"
        
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Faz requisição
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procura primeira imagem
            img_tags = soup.find_all('img')
            
            for img in img_tags[1:]:  # Pula logo do Google
                img_url = img.get('src') or img.get('data-src')
                
                if img_url and img_url.startswith('http'):
                    # Baixa imagem
                    img_data = requests.get(img_url, timeout=10).content
                    
                    # Salva
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    
                    return 'success'
        
        return 'failed'
    
    except Exception as e:
        return 'failed'

def main():
    # Carrega personagens do grafo
    import json
    with open('graph_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    characters = [node['id'] for node in data['nodes']]
    
    # Cria pasta
    os.makedirs('personagens_fotos', exist_ok=True)
    
    print(f"Buscando fotos no Google Images...")
    print("="*60)
    print(f"Total de personagens: {len(characters)}")
    print("="*60)
    
    success = 0
    exists = 0
    failed = 0
    
    for i, char in enumerate(characters, 1):
        print(f"[{i}/{len(characters)}] {char}...", end=' ')
        
        result = download_from_google(char)
        
        if result == 'success':
            print("OK")
            success += 1
        elif result == 'exists':
            print("JA EXISTE")
            exists += 1
        else:
            print("FALHOU")
            failed += 1
        
        time.sleep(2)
    
    print("="*60)
    print(f"Concluido!")
    print(f"  Baixadas: {success}")
    print(f"  Ja existiam: {exists}")
    print(f"  Falharam: {failed}")
    print(f"  Total: {success + exists}/{len(characters)}")
    print(f"Pasta: personagens_fotos/")

if __name__ == '__main__':
    main()
