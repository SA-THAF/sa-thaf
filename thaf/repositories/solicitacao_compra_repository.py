from database.conexao import Conexao
from models.solicitacao_compra import SolicitacaoCompra

class SolicitacaoCompraRepository:
    """solicitacoes_compras usa soft delete por HERANÇA: o trigger
    trg_soft_delete_solicitacoes_compras copia a linha para
    solicitacoes_compras_deletados (fn_mover_para_historico) e deixa o
    DELETE concluir normalmente na tabela principal. Diferente de
    perfis (soft delete in-place), aqui não existe coluna deleted_at
    na tabela principal, e o DELETE físico realmente remove a linha
    dela — o histórico fica só na tabela filha.

    IMPORTANTE: no Postgres, "SELECT * FROM solicitacoes_compras" por
    padrão também devolve as linhas da tabela filha
    (solicitacoes_compras_deletados), por causa da herança. Por isso
    todas as consultas abaixo usam "FROM ONLY solicitacoes_compras" —
    sem o ONLY, registros já excluídos voltariam a aparecer no CRUD
    normal.
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
            criado_em=registro[14]
        )

    def salvar(self, solicitacao_compra):
        sql = """
        INSERT INTO solicitacoes_compras
        (
            solicitante_id,
            professor_responsavel_id,
            turma_id,
            maquina_id,
            status,
            especificacao_tecnica,
            quantidade_solicitacao,
            sap_solicitacao,
            justificativa_solicitacao,
            patrimonio,
            equipamento,
            conjunto_mecanico,
            arquivos
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            solicitacao_compra.solicitante_id,
            solicitacao_compra.professor_responsavel_id,
            solicitacao_compra.turma_id,
            solicitacao_compra.maquina_id,
            solicitacao_compra.status,
            solicitacao_compra.especificacao_tecnica,
            solicitacao_compra.quantidade_solicitacao,
            solicitacao_compra.sap_solicitacao,
            solicitacao_compra.justificativa_solicitacao,
            solicitacao_compra.patrimonio,
            solicitacao_compra.equipamento,
            solicitacao_compra.conjunto_mecanico,
            solicitacao_compra.arquivos
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Solicitação de compra cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar solicitação de compra. Erro: {erro}")

    def buscar_por_id(self, id_solicitacao):
        sql = """
        SELECT id_solicitacao, solicitante_id, professor_responsavel_id,
               turma_id, maquina_id, status, especificacao_tecnica,
               quantidade_solicitacao, sap_solicitacao,
               justificativa_solicitacao, patrimonio, equipamento,
               conjunto_mecanico, arquivos, criado_em
        FROM ONLY solicitacoes_compras
        WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (id_solicitacao,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_solicitacao_compra(registro)

        except Exception as erro:
            print(f"Erro ao buscar solicitação de compra pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id,
                   turma_id, maquina_id, status, especificacao_tecnica,
                   quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento,
                   conjunto_mecanico, arquivos, criado_em
            FROM ONLY solicitacoes_compras
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao_compra(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações de compra: {erro}")
            return []

    def listar_por_status(self, status):
        sql = """
            SELECT id_solicitacao, solicitante_id, professor_responsavel_id,
                   turma_id, maquina_id, status, especificacao_tecnica,
                   quantidade_solicitacao, sap_solicitacao,
                   justificativa_solicitacao, patrimonio, equipamento,
                   conjunto_mecanico, arquivos, criado_em
            FROM ONLY solicitacoes_compras
            WHERE status = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (status,))
            registros = self.db.cursor.fetchall()
            solicitacoes = []

            for registro in registros:
                solicitacoes.append(self.criar_solicitacao_compra(registro))
            return solicitacoes

        except Exception as erro:
            print(f"Erro ao listar solicitações de compra por status: {erro}")
            return []

    def atualizar(self, solicitacao_compra):
        sql = """UPDATE ONLY solicitacoes_compras
        SET
            turma_id = %s,
            maquina_id = %s,
            status = %s,
            especificacao_tecnica = %s,
            quantidade_solicitacao = %s,
            sap_solicitacao = %s,
            justificativa_solicitacao = %s,
            patrimonio = %s,
            equipamento = %s,
            conjunto_mecanico = %s,
            arquivos = %s
        WHERE id_solicitacao = %s
        """
        valores = (
            solicitacao_compra.turma_id,
            solicitacao_compra.maquina_id,
            solicitacao_compra.status,
            solicitacao_compra.especificacao_tecnica,
            solicitacao_compra.quantidade_solicitacao,
            solicitacao_compra.sap_solicitacao,
            solicitacao_compra.justificativa_solicitacao,
            solicitacao_compra.patrimonio,
            solicitacao_compra.equipamento,
            solicitacao_compra.conjunto_mecanico,
            solicitacao_compra.arquivos,
            solicitacao_compra.id_solicitacao
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Solicitação de compra não encontrada!")

            else:
                print("Solicitação de compra atualizada!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar solicitação de compra: {erro}")

    def excluir(self, id_solicitacao):
        if self.buscar_por_id(id_solicitacao) is None:
            print("Solicitação de compra não encontrada!")
            return

        sql = """
            DELETE FROM ONLY solicitacoes_compras
            WHERE id_solicitacao = %s
        """
        try:
            self.db.cursor.execute(sql, (id_solicitacao,))
            self.db.commit()
            print("Solicitação de compra excluída com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir solicitação de compra: {erro}")

    def fechar(self):
        self.db.fechar()