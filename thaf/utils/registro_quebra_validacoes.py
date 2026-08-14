from utils.validacoes_gerais import validar_campo_obrigatorio


def validar_item_id(item_id_str):
    validar_campo_obrigatorio(item_id_str, "código do item")
    try:
        item_id = int(item_id_str)
    except ValueError:
        raise ValueError("Código do item inválido.")

    if item_id <= 0:
        raise ValueError("Código do item deve ser um número positivo.")

    return item_id


def validar_usuario_id(usuario_id_str):
    validar_campo_obrigatorio(usuario_id_str, "código do usuário")
    try:
        usuario_id = int(usuario_id_str)
    except ValueError:
        raise ValueError("Código do usuário inválido.")

    if usuario_id <= 0:
        raise ValueError("Código do usuário deve ser um número positivo.")

    return usuario_id


def validar_descricao_quebra(descricao):
    validar_campo_obrigatorio(descricao, "descrição")
    return descricao.strip()


def validar_foto_url(foto_url):
    if not foto_url:
        return None
    return foto_url.strip()