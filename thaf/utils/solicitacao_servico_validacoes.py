from models.solicitacao_servico import PRIORIDADES_VALIDAS, TIPOS_MANUTENCAO_VALIDOS, STATUS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio


def validar_descricao_problema(descricao):
    validar_campo_obrigatorio(descricao, "descrição do problema")
    return descricao.strip()


def _validar_valor_enum(valor, valores_validos, nome_campo, padrao):
    if not valor:
        return padrao
    valor = valor.strip()
    for valido in valores_validos:
        if valor.lower() == valido.lower():
            return valido
    raise ValueError(
        f"{nome_campo} inválido(a): '{valor}'. Válidos: {', '.join(valores_validos)}."
    )


def validar_prioridade_ss(prioridade):
    return _validar_valor_enum(prioridade, PRIORIDADES_VALIDAS, "Prioridade", "Média")


def validar_tipo_manutencao_ss(tipo):
    return _validar_valor_enum(tipo, TIPOS_MANUTENCAO_VALIDOS, "Tipo de manutenção", "Corretiva")


def validar_status_ss(status):
    return _validar_valor_enum(status, STATUS_VALIDOS, "Status", "Aberta")


def validar_id_referencia(valor, nome_campo, obrigatorio=True):
    valor = (valor or "").strip()
    if not valor:
        if obrigatorio:
            raise ValueError(f"O campo '{nome_campo}' é obrigatório.")
        return None
    try:
        return int(valor)
    except ValueError:
        raise ValueError(f"Código de '{nome_campo}' inválido.")