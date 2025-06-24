import requests

API_KEY = "RGAPI-2dd3f803-2419-4508-885e-8390f6e64d0a"
PUUID = "4FM1SsVQ3G0iXyu50ee-UukdLYEHU5HHjADuY9Il26XNNNizOC6iP76HZ-VLLjDEAqJE4kOjZ-j_yQ"
REGION = "americas"  # Região continental (não use br1 aqui)

url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{PUUID}"
headers = {
    "X-Riot-Token": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Nome do jogador:", data["gameName"])
    print("Hashtag:", data["tagLine"])
    print("Riot ID completo:", f"{data['gameName']}#{data['tagLine']}")
else:
    print("Erro:", response.status_code)
    print(response.text)
