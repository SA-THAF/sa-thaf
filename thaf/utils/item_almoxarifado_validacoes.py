from models.item_almoxarifado import UNIDADES_MEDIDA_PADRAO
from utils.validacoes_gerais import validar_campo_obrigatorio


def validar_nome_ferramenta(nome):
    validar_campo_obrigatorio(nome, "nome")

    nome_normalizado = nome.strip()

    if len(nome_normalizado) > 100:
        raise ValueError("Nome da ferramenta deve ter no máximo 100 caracteres.")

    return nome_normalizado


def validar_dimensao_ferramenta(dimensao):
    if dimensao is None:
        return None

    dimensao_normalizada = dimensao.strip()

    if dimensao_normalizada == "":
        return None

    if len(dimensao_normalizada) > 50:
        raise ValueError("Dimensão da ferramenta deve ter no máximo 50 caracteres.")

    return dimensao_normalizada


def validar_quantidade_atual(quantidade):
    validar_campo_obrigatorio(quantidade, "quantidade atual")

    try:
        quantidade_int = int(quantidade)
    except (TypeError, ValueError):
        raise ValueError("Quantidade atual deve ser um número inteiro.")

    if quantidade_int < 0:
        raise ValueError("Quantidade atual não pode ser negativa.")

    return quantidade_int


def validar_estoque_minimo(estoque_minimo):
    validar_campo_obrigatorio(estoque_minimo, "estoque mínimo")

    try:
        estoque_minimo_int = int(estoque_minimo)
    except (TypeError, ValueError):
        raise ValueError("Estoque mínimo deve ser um número inteiro.")

    if estoque_minimo_int < 0:
        raise ValueError("Estoque mínimo não pode ser negativo.")

    return estoque_minimo_int


def validar_unidade_medida(unidade):
    validar_campo_obrigatorio(unidade, "unidade de medida")

    unidade_normalizada = unidade.strip().upper()

    if unidade_normalizada not in UNIDADES_MEDIDA_PADRAO:
        raise ValueError(
            f"Unidade de medida inválida: '{unidade}'. "
            f"Válidas: {', '.join(UNIDADES_MEDIDA_PADRAO)}."
        )

    return unidade_normalizada


def validar_localizacao_gaveta(localizacao):
    if localizacao is None:
        return None

    localizacao_normalizada = localizacao.strip()

    if localizacao_normalizada == "":
        return None

    if len(localizacao_normalizada) > 50:
        raise ValueError("Localização (gaveta) deve ter no máximo 50 caracteres.")

    return localizacao_normalizada