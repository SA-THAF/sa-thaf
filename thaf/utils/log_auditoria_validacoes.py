import ipaddress
 
from utils.validacoes_gerais import validar_campo_obrigatorio
 
TAMANHO_MAX_ACAO = 255          
TAMANHO_MAX_ENDERECO_IP = 45    
 
 
def validar_acao(acao):
    validar_campo_obrigatorio(acao, "ação")
    acao_normalizada = acao.strip()
 
    if len(acao_normalizada) > TAMANHO_MAX_ACAO:
        raise ValueError(
            f"Ação inválida: deve ter no máximo {TAMANHO_MAX_ACAO} caracteres."
        )
    return acao_normalizada
 
 
def validar_usuario_id(usuario_id):
    if usuario_id is None:
        raise ValueError("Usuário é obrigatório para registrar o log de auditoria.")
 
    if not isinstance(usuario_id, int) or usuario_id <= 0:
        raise ValueError("Usuário inválido: id deve ser um inteiro positivo.")
    return usuario_id
 
 
def validar_endereco_ip(endereco_ip):
    
    if endereco_ip is None or endereco_ip.strip() == "":
        return None
 
    endereco_ip_normalizado = endereco_ip.strip()
 
    if len(endereco_ip_normalizado) > TAMANHO_MAX_ENDERECO_IP:
        raise ValueError(
            f"Endereço IP inválido: deve ter no máximo {TAMANHO_MAX_ENDERECO_IP} caracteres."
        )
 
    try:
        ipaddress.ip_address(endereco_ip_normalizado)
    except ValueError:
        raise ValueError(f"Endereço IP inválido: '{endereco_ip}'.")
 
    return endereco_ip_normalizado