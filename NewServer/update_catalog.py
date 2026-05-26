import os
import json

# Configurações de caminhos relativos ao local do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_FOLDER = os.path.join(BASE_DIR, "games")
OUTPUT_FILE = os.path.join(BASE_DIR, "assets", "data", "games.json")
DEFAULT_THUMB = "assets/images/default_thumb.jpg"

def update_catalog():
    print("🔍 Iniciando Arqueologia Digital: Escaneando acervo PegaJogo...")
    
    if not os.path.exists(GAMES_FOLDER):
        print(f"❌ Erro: A pasta {GAMES_FOLDER} não existe.")
        return

    games_list = []
    
    # Varredura recursiva para suportar categorias por subpastas
    for root, dirs, files in os.walk(GAMES_FOLDER):
        for file in files:
            if file.lower().endswith('.swf'):
                # Caminho relativo para o JSON
                relative_path = os.path.relpath(os.path.join(root, file), BASE_DIR).replace("\\", "/")
                
                # Categoria baseada no nome da pasta pai
                category_name = os.path.basename(root)
                if category_name.lower() == "games":
                    category_name = "Geral"
                
                # Título limpo
                game_title = os.path.splitext(file)[0].replace("-", " ").replace("_", " ").title()
                
                # Busca por thumbnail (mesmo nome .jpg ou .png)
                thumb_name = os.path.splitext(file)[0] + ".jpg"
                thumb_path = os.path.join(os.path.relpath(root, BASE_DIR), thumb_name).replace("\\", "/")
                
                if not os.path.exists(os.path.join(root, thumb_name)):
                    thumb_path = DEFAULT_THUMB

                games_list.append({
                    "title": game_title,
                    "file": relative_path,
                    "thumb": thumb_path,
                    "category": category_name
                })
                print(f"✅ [Mapeado] {game_title} -> {category_name}")

    # Garante que a pasta assets/data exista
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Salva o arquivo JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(games_list, f, indent=2, ensure_ascii=False)
    
    print(f"\n🚀 Sucesso! {len(games_list)} jogos mapeados em {OUTPUT_FILE}")

if __name__ == "__main__":
    update_catalog()