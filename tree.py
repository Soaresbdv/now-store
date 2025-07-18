import os
from pathlib import Path

def generate_project_tree(root_dir='.', output_file='project_tree.txt', excluded=None):
    if excluded is None:
        excluded = {'venv', '__pycache__', '.git', '.env', '.vscode', 'instance', '.idea'}
    
    root_path = Path(root_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{root_path.name}/\n")
        _generate_tree(root_path, f, excluded, indent=1)

def _generate_tree(path, file, excluded, indent):
    for item in sorted(path.iterdir()):
        if item.name in excluded:
            continue
            
        prefix = '    ' * indent + '├── '
        if item.is_dir():
            file.write(f"{prefix}{item.name}/\n")
            _generate_tree(item, file, excluded, indent + 1)
        else:
            file.write(f"{prefix}{item.name}\n")

if __name__ == '__main__':
    # Configurações personalizáveis
    PROJECT_ROOT = '.'  # Raiz do projeto (mude se necessário)
    OUTPUT_FILE = 'project_tree.txt'
    EXCLUDED_ITEMS = {'venv', '__pycache__', '.git', '.env', '.vscode', 'instance', '.idea', '*.pyc'}
    
    print(f"Gerando árvore do projeto em {OUTPUT_FILE}...")
    generate_project_tree(PROJECT_ROOT, OUTPUT_FILE, EXCLUDED_ITEMS)
    print(f"Árvore gerada com sucesso! Verifique o arquivo {OUTPUT_FILE}")