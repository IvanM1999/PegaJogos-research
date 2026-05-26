import re
import os

def triage_binary(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: {file_path} nao encontrado.")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    # 1. Verificacao de Packer (Heuristica simples)
    # Se tiver muitas secoes ou nomes como UPX0, UPX1, e packed.
    is_upx = b"UPX!" in data
    print(f"[*] Analise de Packer: {'UPX detectado' if is_upx else 'Packer desconhecido ou nativo'}")

    # 2. Extracao de Strings (UTF-8 e UTF-16/Wide chars comuns em VB6)
    # Filtramos strings com mais de 4 caracteres
    strings = re.findall(b"[\\x20-\\x7e]{4,}", data)
    
    decoded_strings = []
    for s in strings:
        try:
            decoded_strings.append(s.decode("utf-8"))
        except:
            continue

    # 3. Triagem de alvos especificos
    patterns = {
        "URLs": r"https?://[\w\.-]+",
        "Scripts PHP": r"[\w/-]+\.php",
        "Consultas SQL": r"(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)\s+",
        "Arquivos Firebird": r"[\w/-]+\.(fdb|gdb)",
        "Componentes OCX": r"[\w/-]+\.ocx"
    }

    results = {k: [] for k in patterns.keys()}

    for s in decoded_strings:
        for label, pattern in patterns.items():
            if re.search(pattern, s, re.IGNORECASE):
                results[label].append(s)

    # 4. Relatorio
    print("\n=== RELATORIO DE TRIAGEM LEGACY ===")
    for label, matches in results.items():
        unique_matches = sorted(list(set(matches)))
        print(f"\n[+] {label} encontrados ({len(unique_matches)}):")
        for m in unique_matches[:10]: # Mostra os top 10
            print(f"  - {m}")
        if len(unique_matches) > 10:
            print(f"  ... e mais {len(unique_matches)-10} itens.")

if __name__ == "__main__":
    triage_binary("../PegaJogo.exe") # Caminho presumido do binario