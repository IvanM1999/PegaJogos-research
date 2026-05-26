import os
import json
import logging
from lxml import etree

# Configurações de caminhos
FLASH_ROOT = "../Reference-Flash/flash/"
OUTPUT_FILE = "assets/data/games.json"

# Configura logging para arquivo
logging.basicConfig(filename='generator.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_print(msg):
    print(msg)
    logging.info(msg)

def scan_games():
    games_list = []
    game_id = 1

    if not os.path.exists(FLASH_ROOT):
        print(f"Erro: Pasta {FLASH_ROOT} não encontrada.")
        return

    # Ordenar para manter consistência
    for folder_name in sorted(os.listdir(FLASH_ROOT)):
        folder_path = os.path.join(FLASH_ROOT, folder_name)
        
        if os.path.isdir(folder_path):
            # Procura por arquivos SWF dentro da pasta do jogo
            files = os.listdir(folder_path)
            swf_files = [f for f in files if f.lower().endswith('.swf')]
            
            if swf_files:
                # Priorizamos o SWF que tenha o nome da pasta ou simplesmente o primeiro
                swf_file = swf_files[0]
                
                # Tenta encontrar uma imagem para thumb (png, jpg, jpeg)
                thumb = "assets/images/thumbs/default.png"
                img_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if img_files:
                    thumb = f"../Reference-Flash/flash/{folder_name}/{img_files[0]}"
                
                games_list.append({
                    "id": game_id,
                    "title": folder_name,
                    "category": "Geral", # Pode ser expandido lendo os XMLs de config
                    "file": f"../Reference-Flash/flash/{folder_name}/{swf_file}",
                    "thumb": thumb
                })
                game_id += 1

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(games_list, f, indent=4, ensure_ascii=False)
    print(f"🚀 Sucesso! {len(games_list)} jogos catalogados em {OUTPUT_FILE}")

if __name__ == "__main__":
    scan_games()