STATUS_COMPRA_VALIDOS = (
    "Não Visualizado",
    "Em Análise",
    "Pedido em Andamento",
    "Entregue",
)

# class solicitacao_compra
class SolicitacaoCompra:
    def __init__(self, id_solicitacao = None,
                 solicitante_id = None,
                 professor_responsavel_id = None,
                 turma_id = None,
                 maquina_id = None,
                 status = "Não Visualizado",
                 especificacao_tecnica = "",
                 quantidade_solicitacao = 1,
                 sap_solicitacao = None,
                 justificativa_solicitacao = "",
                 patrimonio = None,
                 equipamento = None,
                 conjunto_mecanico = None,
                 arquivos = None,
                 criado_em = None,
                 deleted_at = None):

        self.id_solicitacao = id_solicitacao
        self.solicitante_id = solicitante_id
        self.professor_responsavel_id = professor_responsavel_id
        self.turma_id = turma_id
        self.maquina_id = maquina_id
        self.status = status
        self.especificacao_tecnica = especificacao_tecnica
        self.quantidade_solicitacao = quantidade_solicitacao
        self.sap_solicitacao = sap_solicitacao
        self.justificativa_solicitacao = justificativa_solicitacao
        self.patrimonio = patrimonio
        self.equipamento = equipamento
        self.conjunto_mecanico = conjunto_mecanico
        self.arquivos = arquivos
        self.criado_em = criado_em
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def __str__(self):
        c1  = "\033[38;5;17m"
        c2  = "\033[38;5;18m"
        c3  = "\033[38;5;19m"
        reset = "\033[0m"

        return (
            f"{c1}=== DADOS SOLICITAÇÃO DE COMPRA ==={reset}\n"
            f"{c2}Status:{reset} {self.status}\n"
            f"{c3}Especificação:{reset} {self.especificacao_tecnica}\n"
            f"{c2}Quantidade:{reset} {self.quantidade_solicitacao}\n"
            f"{c3}Justificativa:{reset} {self.justificativa_solicitacao}\n"
            f"{c1}===================================={reset}"
        )
