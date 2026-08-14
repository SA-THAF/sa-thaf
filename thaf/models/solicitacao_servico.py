PRIORIDADES_VALIDAS = ("Baixa", "Média", "Alta")
TIPOS_MANUTENCAO_VALIDOS = ("Corretiva", "Preventiva", "Preditiva")
STATUS_VALIDOS = ("Aberta", "Em Análise", "Aguardando Peças", "Execução", "Validação", "Concluída")


class SolicitacaoServico:
    def __init__(self, id_ss=None,
                 maquina_id=None,
                 solicitante_id=None,
                 responsavel_id=None,
                 professor_validador_id=None,
                 descricao_problema="",
                 prioridade_ss="Média",
                 tipo_manutencao="Corretiva",
                 status="Aberta",
                 criado_em=None,
                 atualizado_em=None,
                 deleted_at=None):
        self.id_ss = id_ss
        self.maquina_id = maquina_id
        self.solicitante_id = solicitante_id
        self.responsavel_id = responsavel_id
        self.professor_validador_id = professor_validador_id
        self.descricao_problema = descricao_problema
        self.prioridade_ss = prioridade_ss
        self.tipo_manutencao = tipo_manutencao
        self.status = status
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS SOLICITAÇÃO DE SERVIÇO ==={reset}\n"
            f"{c2}Código:{reset} {self.id_ss}\n"
            f"{c2}Máquina (id):{reset} {self.maquina_id}\n"
            f"{c2}Solicitante (id):{reset} {self.solicitante_id}\n"
            f"{c2}Responsável (id):{reset} {self.responsavel_id}\n"
            f"{c2}Prof. Validador (id):{reset} {self.professor_validador_id}\n"
            f"{c3}Descrição:{reset} {self.descricao_problema}\n"
            f"{c3}Prioridade:{reset} {self.prioridade_ss}\n"
            f"{c3}Tipo Manutenção:{reset} {self.tipo_manutencao}\n"
            f"{c3}Status:{reset} {self.status}\n"
            f"{c1}=========================={reset}"
        )