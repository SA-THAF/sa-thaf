PERFIS_VALIDOS = ("coordenador", "gestor", "professor", "aluno")

#class perfil
class Perfil:
    def __init__(self, id_perfil = None,
                 nome_perfil = "",
                 descricao_perfil = "",
                 deleted_at = None):

        self.id_perfil = id_perfil
        self.nome_perfil = nome_perfil
        self.descricao_perfil = descricao_perfil
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1  = "\033[38;5;17m"
        c2  = "\033[38;5;18m"
        c3  = "\033[38;5;19m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS PERFIL ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome_perfil}\n"
            f"{c3}Descrição:{reset} {self.descricao_perfil}\n"
            f"{c1}=========================={reset}"
        )