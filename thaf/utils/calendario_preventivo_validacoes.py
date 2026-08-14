# utils/calendario_preventivo_validacoes.py

from datetime import datetime

from models.calendario_preventivo import FREQUENCIAS_VALIDAS, STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio


def validar_titulo_calendario(titulo):
    validar_campo_obrigatorio(titulo, "título")
    return titulo.strip()


def validar_frequencia_calendario(frequencia):
    validar_campo_obrigatorio(frequencia, "frequência")
    frequencia_normalizada = frequencia.strip().lower()

    for valida in FREQUENCIAS_VALIDAS:
        if valida.lower() == frequencia_normalizada:
            return valida

    raise ValueError(
        f"Frequência inválida: '{frequencia}'. Válidas: {', '.join(FREQUENCIAS_VALIDAS)}."
    )


def validar_status_calendario(status):
    validar_campo_obrigatorio(status, "status")
    status_normalizado = status.strip().lower()

    for valido in STATUS_VALIDOS:
        if valido.lower() == status_normalizado:
            return valido

    raise ValueError(
        f"Status inválido: '{status}'. Válidos: {', '.join(STATUS_VALIDOS)}."
    )


def validar_data_proxima_execucao(data_texto):
    validar_campo_obrigatorio(data_texto, "data da próxima execução")

    try:
        return datetime.strptime(data_texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Data inválida. Use o formato DD/MM/AAAA.")


def validar_id_referencia(valor, nome_campo, obrigatorio=True):
    valor = (valor or "").strip()

    if not valor:
        if obrigatorio:
            raise ValueError(f"{nome_campo} é obrigatório.")
        return None

    try:
        return int(valor)
    except ValueError:
        raise ValueError(f"{nome_campo} inválido.")