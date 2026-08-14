import re

from utils.validacoes_gerais import validar_campo_obrigatorio

PADRAO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_nome_usuario(nome):
    validar_campo_obrigatorio(nome, "nome")
    nome = nome.strip()
    if len(nome) < 3:
        raise ValueError("Nome deve ter ao menos 3 caracteres.")
    return nome


def validar_email_usuario(email):
    validar_campo_obrigatorio(email, "email")
    email = email.strip().lower()
    if not PADRAO_EMAIL.match(email):
        raise ValueError(f"Email inválido: '{email}'.")
    return email


def validar_senha_usuario(senha):
    validar_campo_obrigatorio(senha, "senha")
    if len(senha) < 6:
        raise ValueError("Senha deve ter ao menos 6 caracteres.")
    return senha