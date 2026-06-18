import requests
import sqlite3
import os
from dotenv import load_dotenv

from extrair_partida import extrair_partida

load_dotenv()

chave = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer {chave}"
}

data = '2026-06-17'

resposta = requests.get(
    f"https://footballdata.io/api/v1/matches/date/{data}",
    headers = headers
)

dados = resposta.json()

conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

print(len(dados["data"]["matches"]))

for jogo in dados['data']['matches']:
    match_id = jogo['match_id']

    partidas = extrair_partida(match_id)

    for partida in partidas:
        cursor.execute("""
            INSERT OR IGNORE INTO partidas (
                match_id,
                data_partida,
                selecao,
                adversario,
                gols_feitos,
                gols_sofridos,
                finalizacoes_feitas,
                finalizacoes_sofridas,
                cartoes_amarelos,
                cartoes_vermelhos,
                escanteios,
                xg,
                resultado,
                placar
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                partida["match_id"],
                partida["data_partida"],
                partida["selecao"],
                partida["adversario"],
                partida["gols_feitos"],
                partida["gols_sofridos"],
                partida["finalizacoes_feitas"],
                partida["finalizacoes_sofridas"],
                partida["cartoes_amarelos"],
                partida["cartoes_vermelhos"],
                partida["escanteios"],
                partida["xg"],
                partida["resultado"],
                partida["placar"]
            ))

conn.commit()
conn.close()

print("Banco atualizado com sucesso!")

    