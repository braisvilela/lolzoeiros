import requests
import os
from urllib3.exceptions import InsecureRequestWarning

# Desativa avisos de SSL por causa do certificado local da Riot
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Caminho do lockfile
LOCKFILE_PATH = r"C:\Riot Games\League of Legends\lockfile"

def ler_lockfile():
    with open(LOCKFILE_PATH, "r") as f:
        conteudo = f.read().split(":")
        return {
            "port": conteudo[2],
            "password": conteudo[3],
            "protocol": conteudo[4].strip()
        }

def get_friends(base_url, auth):
    resp = requests.get(f"{base_url}/lol-chat/v1/friends", auth=auth, verify=False)
    resp.raise_for_status()
    return resp.json()

def delete_friend(base_url, auth, friend_id):
    resp = requests.delete(f"{base_url}/lol-chat/v1/friends/{friend_id}", auth=auth, verify=False)
    return resp.status_code == 204

def deletar_todos_amigos():
    dados = ler_lockfile()
    port = dados["port"]
    password = dados["password"]
    protocol = dados["protocol"]

    base_url = f"{protocol}://127.0.0.1:{port}"
    auth = ("riot", password)

    amigos = get_friends(base_url, auth)
    print(f"🔍 {len(amigos)} amigos encontrados.")

    for amigo in amigos:
        nome = amigo.get("name")
        id_amigo = amigo.get("id")
        sucesso = delete_friend(base_url, auth, id_amigo)
        if sucesso:
            print(f"✅ Removido: {nome}")
        else:
            print(f"❌ Falha ao remover: {nome}")

if __name__ == "__main__":
    deletar_todos_amigos()
