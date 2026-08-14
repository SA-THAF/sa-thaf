class LogAuditoria:
    def __init__(self, id=None,
                 usuario_id=None,
                 acao="",
                 endereco_ip=None,
                 criado_em=None):
        self.id = id
        self.usuario_id = usuario_id
        self.acao = acao
        self.endereco_ip = endereco_ip
        self.criado_em = criado_em 
 
    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS LOG DE AUDITORIA ==={reset}\n"
            f"{c2}Usuário ID:{reset} {self.usuario_id}\n"
            f"{c3}Ação:{reset} {self.acao}\n"
            f"{c2}IP:{reset} {self.endereco_ip}\n"
            f"{c3}Criado em:{reset} {self.criado_em}\n"
            f"{c1}=============================={reset}"
        )