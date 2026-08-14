from models.turma import PERIODOS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_codigo_turma(codigo):
    validar_campo_obrigatorio(codigo, "código da turma")
    codigo_normalizado = codigo.strip().upper()

    if len(codigo_normalizado) > 20:
        raise ValueError(
            "Código da turma inválido: máximo de 20 caracteres."
        )
    return codigo_normalizado


def validar_periodo_turma(periodo):
    validar_campo_obrigatorio(periodo, "período")
    periodo_normalizado = periodo.strip().lower()

    if periodo_normalizado not in PERIODOS_VALIDOS:
        raise ValueError(
            f"Período inválido: '{periodo}'. Válidos: {', '.join(PERIODOS_VALIDOS)}."
        )
    return periodo_normalizado.title()