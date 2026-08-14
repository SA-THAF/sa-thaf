# Validações genéricas, reaproveitadas pelos utils/*_validacoes.py de cada
# feature. Ficam aqui para não repetir a mesma checagem em cada tabela.

def validar_campo_obrigatorio(valor, nome_campo):
    if valor is None or not str(valor).strip():
        raise ValueError(f"O campo '{nome_campo}' é obrigatório.")
    return str(valor).strip()


def validar_tamanho_maximo(valor, nome_campo, tamanho_maximo):
    if valor is not None and len(str(valor).strip()) > tamanho_maximo:
        raise ValueError(
            f"O campo '{nome_campo}' deve ter no máximo {tamanho_maximo} caracteres."
        )
    return valor


def validar_inteiro_positivo(valor, nome_campo):
    try:
        valor_int = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"O campo '{nome_campo}' deve ser um número inteiro.")

    if valor_int <= 0:
        raise ValueError(f"O campo '{nome_campo}' deve ser maior que zero.")

    return valor_int


def validar_opcao_valida(valor, nome_campo, opcoes_validas):
    validar_campo_obrigatorio(valor, nome_campo)
    valor_normalizado = valor.strip()

    # aceita comparação sem diferenciar maiúsculas/minúsculas, mas devolve
    # a grafia oficial (como está em opcoes_validas)
    for opcao in opcoes_validas:
        if valor_normalizado.lower() == opcao.lower():
            return opcao

    raise ValueError(
        f"{nome_campo} inválido: '{valor}'. Válidos: {', '.join(opcoes_validas)}."
    )
