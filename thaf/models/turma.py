PERIODOS_VALIDOS = ("primeiro turno", "segundo turno")

class Turma:
    def __init__(self, id_turma = None,
                 codigo_turma = "",
                 periodo_turma = "",
                 deleted_at = None):

        self.id_turma = id_turma
        self.codigo_turma = codigo_turma
        self.periodo_turma = periodo_turma
        self.deleted_at = deleted_at

    def __str__(self):
        c1   = "\033[38;5;17m"
        c2   = "\033[38;5;18m"
        c3   = "\033[38;5;19m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS TURMA ==={reset}\n"
            f"{c2}Código:{reset} {self.codigo_turma}\n"
            f"{c3}Período:{reset} {self.periodo_turma}\n"
            f"{c1}================================={reset}"
        )