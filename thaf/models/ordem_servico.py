TIPOS_MANUTENCAO_OS_VALIDOS = ("corretiva", "preventiva", "preditiva", "melhoria")
CRITICIDADES_OS_VALIDAS = ("baixa", "média", "alta", "crítica")


# class ordem de serviço
class OrdemServico:
    def __init__(self, id_os=None,
                 solicitacao_id=None,
                 maquina_id=None,
                 turma_id=None,
                 tipo_manutencao="",
                 criticidade_os="",
                 descricao_execucao="",
                 pecas_usadas=None,
                 data_execucao=None,
                 hora_inicio=None,
                 hora_fim=None,
                 quantidade_pessoas=1,
                 criado_em=None,
                 deleted_at=None):
        self.id_os = id_os
        self.solicitacao_id = solicitacao_id
        self.maquina_id = maquina_id
        self.turma_id = turma_id
        self.tipo_manutencao = tipo_manutencao
        self.criticidade_os = criticidade_os
        self.descricao_execucao = descricao_execucao
        self.pecas_usadas = pecas_usadas
        self.data_execucao = data_execucao
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.quantidade_pessoas = quantidade_pessoas
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS ORDEM DE SERVIÇO ==={reset}\n"
            f"{c2}Código..............:{reset} {self.id_os}\n"
            f"{c2}Solicitação (SS)....:{reset} {self.solicitacao_id}\n"
            f"{c2}Máquina.............:{reset} {self.maquina_id}\n"
            f"{c2}Turma...............:{reset} {self.turma_id}\n"
            f"{c3}Tipo de manutenção..:{reset} {self.tipo_manutencao}\n"
            f"{c3}Criticidade.........:{reset} {self.criticidade_os}\n"
            f"{c3}Descrição execução..:{reset} {self.descricao_execucao}\n"
            f"{c3}Peças usadas........:{reset} {self.pecas_usadas}\n"
            f"{c3}Data de execução....:{reset} {self.data_execucao}\n"
            f"{c3}Hora início / fim...:{reset} {self.hora_inicio} - {self.hora_fim}\n"
            f"{c3}Quantidade pessoas..:{reset} {self.quantidade_pessoas}\n"
            f"{c1}================================={reset}"
        )