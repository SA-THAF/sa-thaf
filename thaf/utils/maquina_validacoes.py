from models.maquina import STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_tag_maquina(tag):
    validar_campo_obrigatorio(tag, "tag")
    tag_normalizada = tag.strip().upper()

    if len(tag_normalizada) > 20:
        raise ValueError("Tag inválida: máximo de 20 caracteres.")

    return tag_normalizada

def validar_status_vivo(status):
    validar_campo_obrigatorio(status, "status")
    status_normalizado = status.strip().capitalize()

    if status_normalizado not in STATUS_VALIDOS:
        raise ValueError(
            f"Status inválido: '{status}'. Válidos: {', '.join(STATUS_VALIDOS)}."
        )
    return status_normalizado

def validar_setor_id(setor_id):
    try:
        setor_id_int = int(setor_id)
    except (TypeError, ValueError):
        raise ValueError("Código de setor inválido.")

    if setor_id_int <= 0:
        raise ValueError("Código de setor inválido.")

    return setor_id_int