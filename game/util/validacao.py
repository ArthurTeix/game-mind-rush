# Validações do cadastro (sem pygame, só regras)
# Cada função retorna uma mensagem de erro (str) ou None quando está tudo certo.

import re
from datetime import datetime, date

REGEX_USUARIO = re.compile(r"^[A-Za-z0-9_]{3,16}$")
REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


def validar_usuario(usuario):
    if not REGEX_USUARIO.match(usuario):
        return "Nome de usuário inválido: use de 3 a 16 caracteres (letras, números ou _)."
    return None


def validar_email(email):
    if not REGEX_EMAIL.match(email):
        return "E-mail inválido. Exemplo: nome@dominio.com"
    return None


def validar_senha(senha):
    faltando = []

    if len(senha) < 8:
        faltando.append("no mínimo 8 caracteres")
    if not any(c.isupper() for c in senha):
        faltando.append("uma letra maiúscula")
    if not any(c.isdigit() for c in senha):
        faltando.append("um número")

    if faltando:
        return "Senha inválida: falta " + ", ".join(faltando) + "."
    return None


def validar_data_nascimento(texto):
    """Retorna (erro, data_iso). Se houver erro, data_iso é None."""
    if len(texto) != 10:
        return "Data de nascimento inválida. Use o formato DD/MM/AAAA.", None

    try:
        data = datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        return "Data de nascimento inválida. Confira o dia, o mês e o ano.", None

    if data > date.today():
        return "A data de nascimento não pode estar no futuro.", None
    if data.year < 1900:
        return "Data de nascimento inválida. Confira o ano.", None

    return None, data.isoformat()
