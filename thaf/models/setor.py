class Setor:
    def __init__(self, id_setor=None,
                 nome_setor="",
                 descricao_setor="",
                 deleted_at=None):
        self.id_setor = id_setor
        self.nome_setor = nome_setor
        self.descricao_setor = descricao_setor
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS SETOR ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome_setor}\n"
            f"{c3}Descrição:{reset} {self.descricao_setor}\n"
            f"{c1}=========================={reset}"
        )