from datetime import datetime

from models.ordem_servico import TIPOS_MANUTENCAO_OS_VALIDOS, CRITICIDADES_OS_VALIDAS
from utils.validacoes_gerais import validar_campo_obrigatorio


def validar_tipo_manutencao_os(tipo):
    validar_campo_obrigatorio(tipo, "tipo de manutenção")
    tipo_normalizado = tipo.strip().lower()
    if tipo_normalizado not in TIPOS_MANUTENCAO_OS_VALIDOS:
        raise ValueError(
            f"Tipo de manutenção inválido: '{tipo}'. "
            f"Válidos: {', '.join(TIPOS_MANUTENCAO_OS_VALIDOS)}."
        )
    return tipo_normalizado.capitalize()


def validar_criticidade_os(criticidade):
    validar_campo_obrigatorio(criticidade, "criticidade")
    criticidade_normalizada = criticidade.strip().lower()
    if criticidade_normalizada not in CRITICIDADES_OS_VALIDAS:
        raise ValueError(
            f"Criticidade inválida: '{criticidade}'. "
            f"Válidos: {', '.join(CRITICIDADES_OS_VALIDAS)}."
        )
    return criticidade_normalizada.capitalize()


def validar_data_execucao(data_texto):
    validar_campo_obrigatorio(data_texto, "data de execução")
    try:
        data = datetime.strptime(data_texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Data inválida. Use o formato DD/MM/AAAA.")
    return data


def validar_hora(hora_texto, rotulo="hora"):
    validar_campo_obrigatorio(hora_texto, rotulo)
    try:
        hora = datetime.strptime(hora_texto.strip(), "%H:%M").time()
    except ValueError:
        raise ValueError(f"{rotulo.capitalize()} inválida. Use o formato HH:MM.")
    return hora


def validar_hora_inicio_fim(hora_inicio, hora_fim):
    if hora_fim <= hora_inicio:
        raise ValueError("A hora de fim deve ser posterior à hora de início.")


def validar_quantidade_pessoas(quantidade_texto):
    validar_campo_obrigatorio(quantidade_texto, "quantidade de pessoas")
    try:
        quantidade = int(quantidade_texto)
    except ValueError:
        raise ValueError("Quantidade de pessoas inválida. Informe um número inteiro.")
    if quantidade < 1:
        raise ValueError("A quantidade de pessoas deve ser maior ou igual a 1.")
    return quantidade


def validar_id_relacionado(id_texto, rotulo):
    validar_campo_obrigatorio(id_texto, rotulo)
    try:
        return int(id_texto)
    except ValueError:
        raise ValueError(f"Código de {rotulo} inválido.")