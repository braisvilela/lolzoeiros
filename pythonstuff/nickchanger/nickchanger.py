from lcu_driver import Connector
import json
import os

connector = Connector()

def ler_nick_do_arquivo(caminho='nick.txt'):
    """
    Lê o nome e a hashtag de um arquivo de texto.
    Espera que a primeira linha seja o nome e a segunda linha seja a tag.
    """
    if not os.path.exists(caminho):
        print(f"Arquivo '{caminho}' não encontrado.")
        return None, None

    with open(caminho, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.read().splitlines()

    if len(linhas) < 2:
        print("Arquivo deve conter pelo menos duas linhas: nick e hashtag.")
        return None, None

    name = linhas[0].strip()[:16]
    tag = linhas[1].strip()[:5]
    return name, tag

async def change(connection):
    name, tag = ler_nick_do_arquivo()
    if not name or not tag:
        print("Erro ao ler nick e tag do arquivo.")
        return

    data = {"gameName": name, "tagLine": tag}
    request = await connection.request('post', '/lol-summoner/v1/save-alias', json=data)
    response = await request.json()
    print("Resposta da API:")
    print(response)

@connector.ready
async def connect(connection):
    print('Nick Changer do Goiano')
    await change(connection)

connector.start()
input()
