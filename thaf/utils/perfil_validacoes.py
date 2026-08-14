from models.perfil import PERFIS_VALIDOS
from utils.validacoes_gerais import validar_campo_obrigatorio

def validar_nome_perfil(nome):
    validar_campo_obrigatorio(nome, "nome")
    nome_normalizado = nome.strip().lower()

    if nome_normalizado not in PERFIS_VALIDOS:
        raise ValueError(
            f"Perfil inválido: '{nome}'. Válidos: {', '.join(PERFIS_VALIDOS)}."
        )
    return nome_normalizado