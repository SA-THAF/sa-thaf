class RegistroQuebra:
    def __init__(self, id_quebra=None,
                 item_id=None,
                 usuario_id=None,
                 descricao_quebra="",
                 foto_url=None,
                 criado_em=None,
                 deleted_at=None):
        self.id_quebra = id_quebra
        self.item_id = item_id
        self.usuario_id = usuario_id
        self.descricao_quebra = descricao_quebra
        self.foto_url = foto_url
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS REGISTRO DE QUEBRA ==={reset}\n"
            f"{c2}Item.......:{reset} {self.item_id}\n"
            f"{c2}Usuário....:{reset} {self.usuario_id}\n"
            f"{c3}Descrição..:{reset} {self.descricao_quebra}\n"
            f"{c3}Foto.......:{reset} {self.foto_url or '-'}\n"
            f"{c1}==================================={reset}"
        )