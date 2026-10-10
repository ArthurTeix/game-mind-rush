import sqlite3
import hashlib
import hmac
import os
from contextlib import closing

CAMINHO_DB = './game/database/rank.db'
ITERACOES_HASH = 200_000


def _conectar():
    return sqlite3.connect(CAMINHO_DB)


def _gerar_hash(senha, salt):
    # PBKDF2 com salt: a senha nunca é guardada em texto puro
    return hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, ITERACOES_HASH).hex()


def criar_tabelas():
    with closing(_conectar()) as conn, conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE COLLATE NOCASE,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            data_nascimento TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pontuacao INTEGER NOT NULL,
            jogador_id INTEGER REFERENCES jogadores(id)
        )
        """)

        # migração: bancos antigos não têm a coluna jogador_id
        colunas = [c[1] for c in conn.execute("PRAGMA table_info(partidas)").fetchall()]
        if "jogador_id" not in colunas:
            conn.execute("ALTER TABLE partidas ADD COLUMN jogador_id INTEGER")


# ---------------------------------------------------------------- jogadores

def usuario_existe(usuario):
    with closing(_conectar()) as conn:
        linha = conn.execute(
            "SELECT 1 FROM jogadores WHERE usuario = ? COLLATE NOCASE", (usuario,)
        ).fetchone()
    return linha is not None


def email_existe(email):
    with closing(_conectar()) as conn:
        linha = conn.execute(
            "SELECT 1 FROM jogadores WHERE email = ?", (email.lower(),)
        ).fetchone()
    return linha is not None


def inserir_jogador(usuario, email, senha, data_nascimento_iso):
    salt = os.urandom(16)
    senha_hash = _gerar_hash(senha, salt)

    with closing(_conectar()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO jogadores (usuario, email, senha_hash, salt, data_nascimento) "
            "VALUES (?, ?, ?, ?, ?)",
            (usuario, email.lower(), senha_hash, salt.hex(), data_nascimento_iso)
        )
        return cursor.lastrowid


def autenticar(usuario, senha):
    """Retorna {'id', 'usuario'} se usuário e senha batem, senão None."""
    with closing(_conectar()) as conn:
        linha = conn.execute(
            "SELECT id, usuario, senha_hash, salt FROM jogadores "
            "WHERE usuario = ? COLLATE NOCASE", (usuario,)
        ).fetchone()

    if linha is None:
        return None

    jogador_id, nome, senha_hash, salt_hex = linha
    hash_calculado = _gerar_hash(senha, bytes.fromhex(salt_hex))

    if hmac.compare_digest(hash_calculado, senha_hash):
        return {"id": jogador_id, "usuario": nome}
    return None


# ----------------------------------------------------------------- pontuação

def salvar_pontuacao(jogador_id, pontuacao):
    with closing(_conectar()) as conn, conn:
        # Os ? garantem que o sqlite3 trata o valor como dado, nunca como código SQL
        conn.execute(
            "INSERT INTO partidas (pontuacao, jogador_id) VALUES (?, ?)",
            (pontuacao, jogador_id)
        )


def get_top5_pontuacao(jogador_id):
    """Top 5 pontuações apenas do jogador informado."""
    with closing(_conectar()) as conn:
        linhas = conn.execute(
            "SELECT pontuacao FROM partidas WHERE jogador_id = ? "
            "ORDER BY CAST(pontuacao AS INTEGER) DESC LIMIT 5",
            (jogador_id,)
        ).fetchall()

    return [linha[0] for linha in linhas]
