import subprocess
import sys

scripts = [
    '01_gerar_dados_grafo.py',
    '02_gerar_interactions_index.py',
    '03_gerar_eventos.py',
    '04_gerar_timelapse.py'
]

print("="*60)
print("INICIALIZANDO ARQUIVOS DO SITE")
print("="*60)

for i, script in enumerate(scripts, 1):
    print(f"\n[{i}/{len(scripts)}] Executando {script}...")
    print("-"*60)
    
    result = subprocess.run([sys.executable, f'src/site/{script}'], capture_output=False)
    
    if result.returncode != 0:
        print(f"\nERRO ao executar {script}")
        sys.exit(1)
    
    print("-"*60)

print("\n" + "="*60)
print("TODOS OS ARQUIVOS FORAM GERADOS COM SUCESSO!")
print("="*60)
print("\nArquivos gerados em public/resources/jsons/:")
print("  - graph_data.json")
print("  - interactions_index.json")
print("  - eventos_importantes.json")
print("  - timelapse_data.json")
