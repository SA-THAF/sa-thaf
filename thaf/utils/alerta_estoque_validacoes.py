from models.alerta_estoque import STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

MENSAGEM_ALERTA_MAX_LEN = 255


def validar_item_id(item_id):
    validar_campo_obrigatorio(item_id, "item_id")
    try:
        item_id_int = int(item_id)
    except (TypeError, ValueError):
        raise ValueError("Código do item inválido.")

    if item_id_int <= 0:
        raise ValueError("Código do item deve ser um número positivo.")

    return item_id_int


def validar_mensagem_alerta(mensagem):
    validar_campo_obrigatorio(mensagem, "mensagem")
    mensagem_normalizada = mensagem.strip()

    if len(mensagem_normalizada) > MENSAGEM_ALERTA_MAX_LEN:
        raise ValueError(
            f"Mensagem excede o limite de {MENSAGEM_ALERTA_MAX_LEN} caracteres."
        )

    return mensagem_normalizada


def validar_status_alerta(status):
    validar_campo_obrigatorio(status, "status")
    status_normalizado = status.strip().capitalize()

    if status_normalizado not in STATUS_VALIDOS:
        raise ValueError(
            f"Status inválido: '{status}'. Válidos: {', '.join(STATUS_VALIDOS)}."
        )

    return status_normalizado