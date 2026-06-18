import sqlite3
conn = sqlite3.connect("banco.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS partidas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        data_partida TEXT,
        selecao VARCHAR(100),
        adversario VARCHAR(100),
        gols_feitos INTEGER,
        gols_sofridos INTEGER,
        finalizacoes_feitas INTEGER,
        finalizacoes_sofridas INTEGER,
        cartoes_amarelos INTEGER,
        cartoes_vermelhos INTEGER,
        escanteios INTEGER,
        xg REAL,             
        resultado VARCHAR(100),
        placar TEXT,
               
        UNIQUE(match_id, selecao)
     );
""")

conn.commit()
cursor.close()
conn.close()

print('tabela criada')