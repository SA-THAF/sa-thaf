STATUS_VALIDOS = ("Pendente", "Resolvido")


# class alerta_estoque
class AlertaEstoque:
    def __init__(self, id_alerta=None,
                 item_id=None,
                 mensagem_alerta="",
                 status="Pendente",
                 criado_em=None,
                 deleted_at=None):
        self.id_alerta = id_alerta
        self.item_id = item_id
        self.mensagem_alerta = mensagem_alerta
        self.status = status
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS ALERTA DE ESTOQUE ==={reset}\n"
            f"{c2}Item ID:{reset} {self.item_id}\n"
            f"{c3}Mensagem:{reset} {self.mensagem_alerta}\n"
            f"{c2}Status:{reset} {self.status}\n"
            f"{c3}Criado em:{reset} {self.criado_em}\n"
            f"{c1}=================================={reset}"
        )