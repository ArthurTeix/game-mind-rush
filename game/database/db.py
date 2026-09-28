import sqlite3


def criar_tabela_pontuacao():
    connection = sqlite3.connect('./game/database/rank.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS partidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pontuacao INTEGER NOT NULL
    )
    """)

    connection.commit()
    connection.close()


def salvar_pontuacao(pontuacao):
    connection = sqlite3.connect('./game/database/rank.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO partidas (pontuacao) VALUES (?)", (pontuacao,)) # Os ? garantem que o sqlite3 trata o valor como dado, nunca como código SQL

    connection.commit()
    connection.close()


def get_top5_pontuacao():
    connection = sqlite3.connect('./game/database/rank.db')
    cursor = connection.cursor()

    cursor.execute(
    "SELECT pontuacao FROM partidas ORDER BY CAST(pontuacao AS INTEGER) DESC LIMIT 5"
)
    top5 = cursor.fetchall()

    rank = []
    for t in top5:
        rank.append(t[0])

    connection.close()
    return sorted(rank, reverse=True)
