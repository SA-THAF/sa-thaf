from utils.validacoes_gerais import validar_campo_obrigatorio


def validar_nome_setor(nome):
    validar_campo_obrigatorio(nome, "nome")
    nome_normalizado = nome.strip()

    if len(nome_normalizado) > 50:
        raise ValueError("Nome do setor deve ter no máximo 50 caracteres.")

    return nome_normalizado