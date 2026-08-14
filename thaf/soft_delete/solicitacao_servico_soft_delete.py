from database.conexao import Conexao
from models.solicitacao_servico import SolicitacaoServico


class SolicitacaoServicoSoftDelete:
    """Operações sobre solicitações de serviço EXCLUÍDAS.
    solicitacoes_servico usa soft delete por HERANÇA: o trigger
    trg_soft_delete_solicitacoes_servico copia a linha para
    solicitacoes_servico_deletados e deixa o DELETE concluir na tabela
    principal — a linha realmente sai de solicitacoes_servico. Por isso
    "excluída" aqui significa "está em solicitacoes_servico_deletados",
    diferente da flag deleted_at usada em perfis.

    restaurar() reinsere a linha na tabela principal com o mesmo id_ss
    (via OVERRIDING SYSTEM VALUE, já que a coluna é
    GENERATED ALWAYS AS IDENTITY) e remove de _deletados. Se alguma FK
    referenciada (máquina, usuário) tiver sido removida nesse meio
    tempo, o INSERT falha e a operação é revertida.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_solicitacao(self, registro):
        return SolicitacaoServico(
            id_ss=registro[0],
            maquina_id=registro[1],
            solicitante_id=registro[2],
            responsavel_id=registro[3],
            professor_validador_id=registro[4],
            descricao_problema=registro[5],
            prioridade_ss=registro[6],
            tipo_manutencao=registro[7],
            status=registro[8],
            criado_em=registro[9],
            atualizado_em=registro[10],
            deleted_at=registro[11]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id,
                   professor_validador_id, descricao_problema, prioridade_ss,
                   tipo_manutencao, status, criado_em, atualizado_em, deleted_at
            FROM solicitacoes_servico_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            return [self.criar_solicitacao(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar solicitações de serviço excluídas: {erro}")
            return []

    def buscar_excluido_por_id(self, id_ss):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id,
                   professor_validador_id, descricao_problema, prioridade_ss,
                   tipo_manutencao, status, criado_em, atualizado_em, deleted_at
            FROM solicitacoes_servico_deletados
            WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ss,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_solicitacao(registro)
        except Exception as erro:
            print(f"Erro ao buscar solicitação de serviço excluída pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_ss):
        solicitacao = self.buscar_excluido_por_id(id_ss)
        if solicitacao is None:
            print("Solicitação de serviço excluída não encontrada!")
            return

        sql_inserir = """
            INSERT INTO solicitacoes_servico
            (
                id_ss, maquina_id, solicitante_id, responsavel_id,
                professor_validador_id, descricao_problema, prioridade_ss,
                tipo_manutencao, status, criado_em, atualizado_em
            )
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        sql_remover_historico = """
            DELETE FROM solicitacoes_servico_deletados
            WHERE id_ss = %s
        """
        valores = (
            solicitacao.id_ss,
            solicitacao.maquina_id,
            solicitacao.solicitante_id,
            solicitacao.responsavel_id,
            solicitacao.professor_validador_id,
            solicitacao.descricao_problema,
            solicitacao.prioridade_ss,
            solicitacao.tipo_manutencao,
            solicitacao.status,
            solicitacao.criado_em,
            solicitacao.atualizado_em
        )
        try:
            self.db.cursor.execute(sql_inserir, valores)
            self.db.cursor.execute(sql_remover_historico, (id_ss,))
            self.db.commit()
            print("Solicitação de serviço restaurada com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar solicitação de serviço: {erro}")

    def fechar(self):
        self.db.fechar()