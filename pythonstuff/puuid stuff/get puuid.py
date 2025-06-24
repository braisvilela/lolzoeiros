import requests

API_KEY = "RGAPI-2dd3f803-2419-4508-885e-8390f6e64d0a"  # Cole aqui sua chave da Riot
GAME_NAME = "Siyana"
TAG_LINE = "BR1"
REGION = "americas"

url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"
headers = {
    "X-Riot-Token": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("PUUID:", data["puuid"])
else:
    print("Erro:", response.status_code)
    print(response.text)
