from database.conexao import Conexao
from models.solicitacao_compra import SolicitacaoCompra

class SolicitacaoCompraSoftDelete:
    """Operações sobre solicitações de compra EXCLUÍDAS.

    solicitacoes_compras usa soft delete por HERANÇA: o DELETE do
    SolicitacaoCompraRepository dispara o trigger
    trg_soft_delete_solicitacoes_compras, que copia a linha para
    solicitacoes_compras_deletados (via fn_mover_para_historico) e
    deixa o DELETE físico concluir na tabela principal. Diferente de
    perfis (in-place), aqui o registro excluído mora numa tabela
    separada — não existe coluna deleted_at em solicitacoes_compras,
    só em solicitacoes_compras_deletados. Por isso esta classe lê
    direto da tabela de histórico, e não da tabela principal.

    "excluir_definitivamente" existe de fato aqui (diferente de
    perfis): um DELETE em solicitacoes_compras_deletados remove a
    linha do histórico de verdade, pois ela não tem tabela filha
    própria.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_solicitacao_compra(self, registro):
        return SolicitacaoCompra(
            id_solicitacao=registro[0],
            solicitante_id=registro[1],
            professor_responsavel_id=registro[2],
            turma_id=registro[3],
            maquina_id=registro[4],
            status=registro[5],
            especificacao_tecnica=registro[6],
            quantidade_solicitacao=registro[7],
            sap_solicitacao=registro[8],
            justificativa_solicitacao=registro[9],
            patrimonio=registro[10],
            equipamento=registro[11],
            conjunto_mecanico=registro[12],
            arquivos=registro[13],
            criado_em=registro[14],
            deleted_at=registro[15]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id,
                   turma_id, maquina_id, status, especificacao_tecnica,
                   quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento,
                   conjunto_mecanico, arquivos, criado_em, deleted_at
            FROM solicitacoes_compras_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao_compra(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações de compra excluídas: {erro}")
            return []

    def buscar_excluido_por_id(self, id_solicitacao):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id,
                   turma_id, maquina_id, status, especificacao_tecnica,
                   quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento,
                   conjunto_mecanico, arquivos, criado_em, deleted_at
            FROM solicitacoes_compras_deletados
            WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (id_solicitacao,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_solicitacao_compra(registro)

        except Exception as erro:
            print(f"Erro ao buscar solicitação de compra excluída pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_solicitacao):
        if self.buscar_excluido_por_id(id_solicitacao) is None:
            print("Solicitação de compra excluída não encontrada!")
            return

        sql_inserir = """
            INSERT INTO solicitacoes_compras
            (
                id_solicitacao, solicitante_id, professor_responsavel_id,
                turma_id, maquina_id, status, especificacao_tecnica,
                quantidade_solicitacao, sap_solicitacao,
                justificativa_solicitacao, patrimonio, equipamento,
                conjunto_mecanico, arquivos, criado_em
            )
            OVERRIDING SYSTEM VALUE
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id,
                   turma_id, maquina_id, status, especificacao_tecnica,
                   quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento,
                   conjunto_mecanico, arquivos, criado_em
            FROM solicitacoes_compras_deletados
            WHERE id_solicitacao = %s
        """
        sql_remover_historico = """
            DELETE FROM solicitacoes_compras_deletados
            WHERE id_solicitacao = %s
        """
        try:
            # id_solicitacao é GENERATED ALWAYS AS IDENTITY: OVERRIDING
            # SYSTEM VALUE é obrigatório para reinserir com o mesmo id
            # que a linha tinha antes de ser excluída.
            self.db.cursor.execute(sql_inserir, (id_solicitacao,))
            self.db.cursor.execute(sql_remover_historico, (id_solicitacao,))
            self.db.commit()
            print("Solicitação de compra restaurada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar solicitação de compra: {erro}")
            print("Verifique se o solicitante, professor, turma ou máquina vinculados ainda existem.")

    def excluir_definitivamente(self, id_solicitacao):
        if self.buscar_excluido_por_id(id_solicitacao) is None:
            print("Solicitação de compra excluída não encontrada!")
            return

        sql = """
            DELETE FROM solicitacoes_compras_deletados
            WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (id_solicitacao,))
            self.db.commit()
            print("Solicitação de compra removida definitivamente do histórico!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao remover definitivamente a solicitação de compra: {erro}")

    def fechar(self):
        self.db.fechar()
