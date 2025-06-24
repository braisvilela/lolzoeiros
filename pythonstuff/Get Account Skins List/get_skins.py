import requests
import base64
import json
import os
import psutil

def get_lcu_credentials():
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['name'] and "LeagueClientUx.exe" in proc.info['name']:
            for arg in proc.info['cmdline']:
                if "--remoting-auth-token=" in arg:
                    token = arg.split("--remoting-auth-token=")[1]
                if "--app-port=" in arg:
                    port = arg.split("--app-port=")[1]
            return token, port
    return None, None

def main():
    token, port = get_lcu_credentials()
    if not token or not port:
        print("Não foi possível encontrar o cliente do LoL.")
        return

    url = f"https://127.0.0.1:{port}/lol-inventory/v2/inventory/CHAMPION_SKIN"
    auth = base64.b64encode(f"riot:{token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()

        skin_ids = []
        for skin in data:
            item_id = skin.get("itemId")
            if item_id is not None:
                skin_ids.append(str(item_id))

        with open("skins.txt", "w") as file:
            file.write("\n".join(skin_ids))

        print(f"{len(skin_ids)} skins salvas em skins.txt")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com o cliente LCU: {e}")

if __name__ == "__main__":
    main()
