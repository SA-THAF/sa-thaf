from database.conexao import Conexao
from models.ordem_servico import OrdemServico


class OrdemServicoSoftDelete:
    """ordens_servico usa soft delete por HERANÇA: os registros excluídos
    ficam fisicamente na tabela filha ordens_servico_deletados (criada com
    INHERITS (ordens_servico)). Restaurar significa copiar a linha de volta
    para ordens_servico e removê-la do histórico, dentro da mesma transação.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_ordem_servico(self, registro):
        ordem_servico = OrdemServico(
            id_os=registro[0],
            solicitacao_id=registro[1],
            maquina_id=registro[2],
            turma_id=registro[3],
            tipo_manutencao=registro[4],
            criticidade_os=registro[5],
            descricao_execucao=registro[6],
            pecas_usadas=registro[7],
            data_execucao=registro[8],
            hora_inicio=registro[9],
            hora_fim=registro[10],
            quantidade_pessoas=registro[11],
            criado_em=registro[12]
        )
        ordem_servico.deleted_at = registro[13]
        return ordem_servico

    def listar_excluidos(self):
        sql = """
            SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
                   criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
                   hora_inicio, hora_fim, quantidade_pessoas, criado_em, deleted_at
            FROM ordens_servico_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            return [self.criar_ordem_servico(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar ordens de serviço excluídas: {erro}")
            return []

    def buscar_excluido_por_id(self, id_os):
        sql = """
            SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
                   criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
                   hora_inicio, hora_fim, quantidade_pessoas, criado_em, deleted_at
            FROM ordens_servico_deletados
            WHERE id_os = %s
        """
        try:
            self.db.cursor.execute(sql, (id_os,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_ordem_servico(registro)
        except Exception as erro:
            print(f"Erro ao buscar ordem de serviço excluída pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_os):
        # OVERRIDING SYSTEM VALUE é necessário porque id_os é
        # GENERATED ALWAYS AS IDENTITY: sem isso o Postgres recusa reinserir
        # um valor explícito de id_os vindo do histórico.
        sql_inserir = """
            INSERT INTO ordens_servico
            (
                id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
                criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
                hora_inicio, hora_fim, quantidade_pessoas, criado_em
            )
            OVERRIDING SYSTEM VALUE
            SELECT
                id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
                criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
                hora_inicio, hora_fim, quantidade_pessoas, criado_em
            FROM ordens_servico_deletados
            WHERE id_os = %s
        """
        sql_remover_historico = """
            DELETE FROM ordens_servico_deletados
            WHERE id_os = %s
        """
        try:
            self.db.cursor.execute(sql_inserir, (id_os,))
            if self.db.cursor.rowcount == 0:
                self.db.rollback()
                print("Ordem de serviço excluída não encontrada!")
                return
            self.db.cursor.execute(sql_remover_historico, (id_os,))
            self.db.commit()
            print("Ordem de serviço restaurada com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar ordem de serviço: {erro}")

    def fechar(self):
        self.db.fechar()