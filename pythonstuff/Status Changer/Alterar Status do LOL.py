import requests
from requests.auth import HTTPBasicAuth
import urllib3

def ler_lockfile(caminho):
    with open(caminho, "r") as f:
        content = f.read().strip()
    return content.split(":")

def alterar_status(port, token, mensagem, disponibilidade):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = f"https://127.0.0.1:{port}/lol-chat/v1/me"
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth('riot', token)

    json_data = {
        "statusMessage": mensagem,
        "availability": disponibilidade  # ex: "chat", "away", "busy", "offline"
    }

    response = requests.put(url, json=json_data, headers=headers, auth=auth, verify=False)
    if response.status_code in [200, 201, 204]:
        print("Status alterado com sucesso!")
    else:
        print(f"Erro ao alterar status: {response.status_code} - {response.text}")

if __name__ == "__main__":
    lockfile_path = r"C:\Riot Games\League of Legends\lockfile"
    process, pid, port, token, protocol = ler_lockfile(lockfile_path)

    print(f"Process: {process}")
    print(f"PID: {pid}")
    print(f"Port: {port}")
    print(f"Token: {token}")
    print(f"Protocol: {protocol}")

    capivara = '''
⠀⠀⢀⣀⠤⠿⢤⢖⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡔⢩⠂⠀⠒⠗⠈⠀⠉⠢⠄⣀⠠⠤⠄⠒⢖⡒⢒⠂⠤⢄⠀⠀⠀⠀
⠇⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠀⠈⠈⡨⢀⠡⡪⠢⡀⠀
⠈⠒⠀⠤⠤⣄⡆⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⠀⢕⠱⠀
⠀⠀⠀⠀⠀⠈⢳⣐⡐⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⠇
⠀⠀⠀⠀⠀⠀⠀⠑⢤⢁⠀⠆⠀⠀⠀⠀⠀⢀⢰⠀⠀⠀⡀⢄⡜⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⡦⠄⡷⠢⠤⠤⠤⠤⢬⢈⡇⢠⣈⣰⠎⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣃⢸⡇⠀⠀⠀⠀⠀⠈⢪⢀⣺⡅⢈⠆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠶⡿⠤⠚⠁⠀⠀⠀⢀⣠⡤⢺⣥⠟⢡⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀
'''

    alterar_status(port, token, capivara, "chat")
