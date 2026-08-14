from models.solicitacao_compra import STATUS_COMPRA_VALIDOS
from utils.validacoes_gerais import (
    validar_campo_obrigatorio,
    validar_tamanho_maximo,
    validar_inteiro_positivo,
    validar_opcao_valida,
)


def validar_status_compra(status):
    return validar_opcao_valida(status, "status", STATUS_COMPRA_VALIDOS)


def validar_especificacao_tecnica(especificacao_tecnica):
    return validar_campo_obrigatorio(especificacao_tecnica, "especificação técnica")


def validar_justificativa_solicitacao(justificativa_solicitacao):
    return validar_campo_obrigatorio(justificativa_solicitacao, "justificativa")


def validar_quantidade_solicitacao(quantidade_solicitacao):
    return validar_inteiro_positivo(quantidade_solicitacao, "quantidade")


def validar_sap_solicitacao(sap_solicitacao):
    return validar_tamanho_maximo(sap_solicitacao, "SAP", 50)


def validar_patrimonio(patrimonio):
    return validar_tamanho_maximo(patrimonio, "patrimônio", 50)


def validar_equipamento(equipamento):
    return validar_tamanho_maximo(equipamento, "equipamento", 100)


def validar_conjunto_mecanico(conjunto_mecanico):
    return validar_tamanho_maximo(conjunto_mecanico, "conjunto mecânico", 100)


def validar_arquivos(arquivos):
    return validar_tamanho_maximo(arquivos, "arquivos", 255)