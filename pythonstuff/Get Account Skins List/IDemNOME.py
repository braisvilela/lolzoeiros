import json

def main():
    # Carrega skin_names.json
    with open('skin_names.json', 'r', encoding='utf-8') as f:
        skin_dict = json.load(f)

    # Lê os IDs de skins.txt
    with open('skins.txt', 'r', encoding='utf-8') as f:
        skin_ids = [line.strip() for line in f if line.strip()]

    # Converte IDs para nomes
    skin_names = []
    for skin_id in skin_ids:
        name = skin_dict.get(skin_id, f"Unknown Skin {skin_id}")
        skin_names.append(name)

    # Escreve os nomes em skin_names.txt
    with open('skin_names.txt', 'w', encoding='utf-8') as f:
        for name in skin_names:
            f.write(name + '\n')

    print(f"{len(skin_names)} nomes de skins salvos em skin_names.txt")

if __name__ == "__main__":
    main()
