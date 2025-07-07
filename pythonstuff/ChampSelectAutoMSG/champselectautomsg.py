import requests
import base64
import time
import psutil
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_lcu_credentials():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == "LeagueClientUx.exe":
            cmdline = proc.info['cmdline']
            for arg in cmdline:
                if "--app-port=" in arg:
                    port = arg.split('=')[1]
                if "--remoting-auth-token=" in arg:
                    token = arg.split('=')[1]
            return port, token
    return None, None

def send_message(port, token, message):
    auth = base64.b64encode(f'riot:{token}'.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}"
    }
    
    url_conversations = f"https://127.0.0.1:{port}/lol-chat/v1/conversations"
    
    max_attempts = 10
    for attempt in range(max_attempts):
        response = requests.get(url_conversations, headers=headers, verify=False)
        
        if response.status_code != 200:
            print("Não foi possível obter as conversas. Tentando novamente...")
            time.sleep(1)
            continue
        
        conversations = response.json()
        
        for convo in conversations:
            if convo.get("type") == "championSelect":
                conversation_id = convo["id"]
                url_message = f"https://127.0.0.1:{port}/lol-chat/v1/conversations/{conversation_id}/messages"
                payload = {
                    "body": message
                }
                r = requests.post(url_message, json=payload, headers=headers, verify=False)
                if r.status_code == 200:
                    print("Mensagem enviada no chat do Champion Select.")
                else:
                    print(f"Falha ao enviar mensagem. Código: {r.status_code}")
                return
        
        print(f"Tentativa {attempt + 1}/{max_attempts}: Chat do Champion Select não encontrado. Tentando novamente...")
        time.sleep(1)

    print("Não foi possível encontrar o chat do Champion Select após várias tentativas.")

def is_in_champ_select(port, token):
    url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'riot:{token}'.encode()).decode()}"
    }
    response = requests.get(url, headers=headers, verify=False)
    return response.status_code == 200

print("Bot iniciado. Monitorando o cliente do LoL...")

message_sent = False

while True:
    port, token = get_lcu_credentials()
    if port and token:
        if is_in_champ_select(port, token):
            if not message_sent:
                print("Champion Select detectado!")
                send_message(port, token, "https://www.twitch.tv/loveastreamer")
                message_sent = True
        else:
            if message_sent:
                print("Saiu da Champion Select. Aguardando próximo lobby...")
            message_sent = False
    else:
        print("Cliente do LoL não encontrado. Abrindo cliente?")
        message_sent = False
    
    time.sleep(3)
