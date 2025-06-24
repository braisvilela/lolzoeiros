import requests
from requests.auth import HTTPBasicAuth
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Palavras proibidas, pode deixar vazio se quiser
proibidas = []

def ler_lockfile(caminho):
    with open(caminho, "r") as f:
        content = f.read().strip()
    return content.split(":")

def obter_conversas(base_url, auth):
    url = base_url + "/lol-chat/v1/conversations"
    r = requests.get(url, auth=auth, verify=False)
    return r.json()

def obter_mensagens(base_url, auth, convo_id):
    url = base_url + f"/lol-chat/v1/conversations/{convo_id}/messages"
    r = requests.get(url, auth=auth, verify=False)
    return r.json()

def enviar_mensagem(base_url, auth, convo_id, mensagem):
    url = base_url + f"/lol-chat/v1/conversations/{convo_id}/messages"
    payload = {
        "body": mensagem,
        "type": "chat"
    }
    r = requests.post(url, json=payload, auth=auth, verify=False)
    return r.status_code == 201

def filtrar_palavras(texto):
    texto_lower = texto.lower()
    for p in proibidas:
        if p in texto_lower:
            return True
    return False

def processar_mensagem(base_url, auth, convo_id, mensagem):
    corpo = mensagem.get("body", "")
    autor = mensagem.get("fromSummoner", {}).get("displayName", "")
    
    # Ignora mensagens do próprio bot
    if autor == "GiiH-Bot":
        return

    # Filtro de palavrões
    if filtrar_palavras(corpo):
        enviar_mensagem(base_url, auth, convo_id, "Por favor, evite usar palavrões!")
        return

    # Comandos customizados
    if corpo.lower().startswith("!elo"):
        # Aqui você pode integrar com API oficial para buscar elo e PDL reais
        elo = "Bronze I"
        pdls = 42
        resposta = f"Seu elo atual é {elo} e você tem {pdls} PDLs."
        enviar_mensagem(base_url, auth, convo_id, resposta)
    elif corpo.lower().startswith("!oi"):
        resposta = f"Oi {autor}!"
        enviar_mensagem(base_url, auth, convo_id, resposta)

def main():
    lockfile_path = r"C:\Riot Games\League of Legends\lockfile"
    process, pid, port, token, protocol = ler_lockfile(lockfile_path)
    base_url = f"https://127.0.0.1:{port}"
    auth = HTTPBasicAuth('riot', token)
    
    print("Bot iniciado. Monitorando chat...")
    
    ja_vistos = set()
    
    while True:
        try:
            conversas = obter_conversas(base_url, auth)
            for convo in conversas:
                convo_id = convo.get("id")
                mensagens = obter_mensagens(base_url, auth, convo_id)
                
                for msg in mensagens:
                    msg_id = msg.get("id")
                    if msg_id not in ja_vistos:
                        processar_mensagem(base_url, auth, convo_id, msg)
                        ja_vistos.add(msg_id)
            
            time.sleep(3)
            
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
