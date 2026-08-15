from database.conexao import Conexao
from models.solicitacao_servico import SolicitacaoServico


class SolicitacaoServicoRepository:
    """solicitacoes_servico usa soft delete por HERANÇA: o trigger
    trg_soft_delete_solicitacoes_servico (fn_mover_para_historico) copia a
    linha para solicitacoes_servico_deletados e deixa o DELETE concluir
    normalmente na tabela principal. Diferente do padrão IN-PLACE
    (perfis), aqui o cursor.rowcount do DELETE É confiável — não é
    necessário conferir existência antes de excluir().

    IMPORTANTE: como solicitacoes_servico_deletados é filha por herança
    de solicitacoes_servico, todo SELECT/UPDATE/DELETE aqui usa "ONLY
    solicitacoes_servico" — sem o ONLY, o Postgres também
    enxergaria/afetaria as solicitações já movidas para o histórico.
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
            atualizado_em=registro[10]
        )

    def salvar(self, solicitacao):
        sql = """
        INSERT INTO solicitacoes_servico
        (
            maquina_id,
            solicitante_id,
            responsavel_id,
            professor_validador_id,
            descricao_problema,
            prioridade_ss,
            tipo_manutencao,
            status
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            solicitacao.maquina_id,
            solicitacao.solicitante_id,
            solicitacao.responsavel_id,
            solicitacao.professor_validador_id,
            solicitacao.descricao_problema,
            solicitacao.prioridade_ss,
            solicitacao.tipo_manutencao,
            solicitacao.status
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Solicitação de serviço cadastrada com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar solicitação de serviço. Erro: {erro}")

    def buscar_por_id(self, id_ss):
        sql = """
        SELECT id_ss, maquina_id, solicitante_id, responsavel_id,
               professor_validador_id, descricao_problema, prioridade_ss,
               tipo_manutencao, status, criado_em, atualizado_em
        FROM ONLY solicitacoes_servico
        WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ss,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_solicitacao(registro)
        except Exception as erro:
            print(f"Erro ao buscar solicitação de serviço pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id,
                   professor_validador_id, descricao_problema, prioridade_ss,
                   tipo_manutencao, status, criado_em, atualizado_em
            FROM ONLY solicitacoes_servico
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            return [self.criar_solicitacao(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar solicitações de serviço: {erro}")
            return []

    def listar_por_status(self, status):
        sql = """
            SELECT id_ss, maquina_id, solicitante_id, responsavel_id,
                   professor_validador_id, descricao_problema, prioridade_ss,
                   tipo_manutencao, status, criado_em, atualizado_em
            FROM ONLY solicitacoes_servico
            WHERE status = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (status,))
            registros = self.db.cursor.fetchall()
            return [self.criar_solicitacao(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar solicitações de serviço por status: {erro}")
            return []

    def atualizar(self, solicitacao):
        sql = """UPDATE ONLY solicitacoes_servico
        SET
            maquina_id = %s,
            solicitante_id = %s,
            responsavel_id = %s,
            professor_validador_id = %s,
            descricao_problema = %s,
            prioridade_ss = %s,
            tipo_manutencao = %s,
            status = %s
        WHERE id_ss = %s
        """
        valores = (
            solicitacao.maquina_id,
            solicitacao.solicitante_id,
            solicitacao.responsavel_id,
            solicitacao.professor_validador_id,
            solicitacao.descricao_problema,
            solicitacao.prioridade_ss,
            solicitacao.tipo_manutencao,
            solicitacao.status,
            solicitacao.id_ss
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Solicitação de serviço não encontrada!")
            else:
                # atualizado_em é preenchido automaticamente pelo trigger
                # trg_touch_solicitacoes_servico
                print("Solicitação de serviço atualizada!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar solicitação de serviço: {erro}")

    def excluir(self, id_ss):
        sql = """
            DELETE FROM ONLY solicitacoes_servico
            WHERE id_ss = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ss,))
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Solicitação de serviço não encontrada!")
            else:
                print("Solicitação de serviço excluída com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir solicitação de serviço: {erro}")

    def fechar(self):
        self.db.fechar()