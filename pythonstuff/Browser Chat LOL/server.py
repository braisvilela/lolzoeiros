from flask import Flask, jsonify, request, send_from_directory
from requests.auth import HTTPBasicAuth
import requests
import urllib3
import uuid
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__, static_folder='static')

lockfile_path = r"C:\Riot Games\League of Legends\lockfile"

API_KEY = "RGAPI-2dd3f803-2419-4508-885e-8390f6e64d0a"
cache_puuid_nome = {}

def ler_lockfile(caminho):
    with open(caminho, "r") as f:
        content = f.read().strip()
    return content.split(":")

def uuid_to_puuid(uuid_str):
    try:
        u = uuid.UUID(uuid_str)
        puuid_bytes = u.bytes
        puuid = base64.urlsafe_b64encode(puuid_bytes).rstrip(b'=').decode('utf-8')
        return puuid
    except Exception as e:
        print(f"Erro convertendo UUID para PUUID: {e}")
        return None

def base_auth():
    process, pid, port, token, protocol = ler_lockfile(lockfile_path)
    base_url = f"https://127.0.0.1:{port}"
    auth = HTTPBasicAuth('riot', token)
    return base_url, auth

def buscar_riot_id_por_puuid(puuid):
    if not puuid:
        return None
    if puuid in cache_puuid_nome:
        return cache_puuid_nome[puuid]

    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        nome = f"{data['gameName']}#{data['tagLine']}"
        cache_puuid_nome[puuid] = nome
        return nome
    else:
        print(f"Erro ao buscar nome para PUUID {puuid}: {r.status_code} - {r.text}")
        return None

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/conversas')
def conversas():
    base_url, auth = base_auth()
    r = requests.get(base_url + "/lol-chat/v1/conversations", auth=auth, verify=False)
    if r.status_code != 200:
        return jsonify({"erro": "Não foi possível obter conversas"}), 500

    conversas = r.json()
    resultado = []
    meu_puuid = None

    summoner_info = requests.get(base_url + "/lol-summoner/v1/current-summoner", auth=auth, verify=False)
    if summoner_info.status_code == 200:
        meu_puuid = summoner_info.json().get("puuid")
        print(f"Meu PUUID: {meu_puuid}")
    else:
        print("Erro ao obter info do summoner atual")

    for convo in conversas:
        print(f"Conversa: {convo}")
        convo_id = convo.get("id", "")
        tipo = convo.get("type", "")
        nome_destinatario = ""

        # Se tiver gameName + gameTag, use para mostrar nome
        if convo.get("gameName") and convo.get("gameTag"):
            nome_destinatario = f"{convo['gameName']}#{convo['gameTag']}"
        else:
            # fallback para o tipo
            nome_destinatario = tipo

        resultado.append({
            "id_conversa": convo_id,
            "titulo": nome_destinatario,
            "detalhes": convo
        })

    return jsonify(resultado)



@app.route('/amigos')
def amigos():
    base_url, auth = base_auth()
    r = requests.get(base_url + "/lol-chat/v1/friends", auth=auth, verify=False)
    if r.status_code != 200:
        return jsonify({"erro": "Não foi possível obter amigos"}), 500

    amigos = r.json()
    resultado = []

    for amigo in amigos:
        puuid = amigo.get("puuid", "")
        nome_invocador = buscar_riot_id_por_puuid(puuid)
        resultado.append({
            "name": amigo.get("name", ""),
            "puuid": puuid,
            "riotId": nome_invocador if nome_invocador else amigo.get("name", "")
        })

    return jsonify(resultado)

@app.route('/conversas/<convo_id>/mensagens')
def mensagens(convo_id):
    base_url, auth = base_auth()
    r = requests.get(base_url + f"/lol-chat/v1/conversations/{convo_id}/messages", auth=auth, verify=False)
    if r.status_code == 200:
        return jsonify(r.json())
    else:
        return jsonify({"erro": "Não foi possível obter mensagens"}), r.status_code

@app.route('/conversas/<convo_id>/mensagens', methods=['POST'])
def enviar(convo_id):
    base_url, auth = base_auth()
    data = request.json
    mensagem = data.get("mensagem", "")
    payload = {
        "body": mensagem,
        "type": "chat"
    }
    r = requests.post(base_url + f"/lol-chat/v1/conversations/{convo_id}/messages", json=payload, auth=auth, verify=False)
    if r.status_code == 201:
        return jsonify({"status": "ok"}), 201
    else:
        return jsonify({"status": "erro", "detalhes": r.text}), r.status_code

if __name__ == '__main__':
    app.run(port=5000)
