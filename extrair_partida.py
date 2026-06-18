import requests
import os
from dotenv import load_dotenv

load_dotenv()

chave = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer {chave}"
}

def calcular_resultado(gols_feitos, gols_sofridos):
    if gols_feitos > gols_sofridos:
        return 'Vitoria'
    elif gols_feitos < gols_sofridos:
        return 'Derrota'
    else:
        return 'Empate'

def extrair_partida(match_id):
    resposta = requests.get(
    f"https://footballdata.io/api/v1/matches/{match_id}/stats",
    headers=headers
)
    
    if resposta.status_code != 200:
            print("Erro ao consultar API")
            return []

    dados = resposta.json()

    gols_feitos_casa = dados["data"]["match"]["score"]["home"]
    gols_sofridos_casa = dados["data"]["match"]["score"]["away"]

    gols_feitos_visitante = dados["data"]["match"]["score"]["away"]
    gols_sofridos_visitante = dados["data"]["match"]["score"]["home"]

    resultado_casa = calcular_resultado(
        gols_feitos_casa,
        gols_sofridos_casa
    )

    resultado_visitante = calcular_resultado(
        gols_feitos_visitante,
        gols_sofridos_visitante
    )

    placar = f"{gols_feitos_casa}x{gols_sofridos_casa}"

    partida_casa = {
    "match_id": dados["data"]["match"]["match_id"],
    "data_partida": dados["data"]["match"]["match_date"],
    "selecao": dados['data']['match']['home_team']['team_name'],
    "adversario": dados['data']['match']['away_team']['team_name'],
    "gols_feitos": gols_feitos_casa,
    "gols_sofridos": gols_sofridos_casa,
    "finalizacoes_feitas": dados['data']['stats']['shots']['home'],
    "finalizacoes_sofridas": dados['data']['stats']['shots']['away'],
    "cartoes_amarelos": dados['data']['stats']['yellow_cards']['home'],
    "cartoes_vermelhos": dados['data']['stats']['red_cards']['home'],
    "escanteios": dados['data']['stats']['corners']['home'],
    "xg": dados['data']['stats']['xg']['home'],
    "resultado": resultado_casa,
    "placar": placar
}
    partida_visitante = {
    "match_id": dados["data"]["match"]["match_id"],
    "data_partida": dados["data"]["match"]["match_date"],
    "selecao": dados['data']['match']['away_team']['team_name'],
    "adversario": dados['data']['match']['home_team']['team_name'],
    "gols_feitos": gols_feitos_visitante,
    "gols_sofridos": gols_sofridos_visitante,
    "finalizacoes_feitas": dados['data']['stats']['shots']['away'],
    "finalizacoes_sofridas": dados['data']['stats']['shots']['home'],
    "cartoes_amarelos": dados['data']['stats']['yellow_cards']['away'],
    "cartoes_vermelhos": dados['data']['stats']['red_cards']['away'],
    "escanteios": dados['data']['stats']['corners']['away'],
    "xg": dados['data']['stats']['xg']['away'],
    "resultado": resultado_visitante,
    "placar": placar
}
    partidas = [partida_casa, partida_visitante]
    return partidas

