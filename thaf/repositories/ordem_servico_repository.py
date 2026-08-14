from database.conexao import Conexao
from models.ordem_servico import OrdemServico


class OrdemServicoRepository:
    """ordens_servico usa soft delete por HERANÇA: o DELETE aciona o
    trigger trg_soft_delete_ordens_servico (fn_mover_para_historico), que
    copia a linha inteira para ordens_servico_deletados e deixa o DELETE
    concluir normalmente na tabela principal. Diferente do padrão IN-PLACE
    (como em perfis), aqui o cursor.rowcount do DELETE é confiável.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_ordem_servico(self, registro):
        return OrdemServico(
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

    def salvar(self, ordem_servico):
        sql = """
        INSERT INTO ordens_servico
        (
            solicitacao_id,
            maquina_id,
            turma_id,
            tipo_manutencao,
            criticidade_os,
            descricao_execucao,
            pecas_usadas,
            data_execucao,
            hora_inicio,
            hora_fim,
            quantidade_pessoas
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            ordem_servico.solicitacao_id,
            ordem_servico.maquina_id,
            ordem_servico.turma_id,
            ordem_servico.tipo_manutencao,
            ordem_servico.criticidade_os,
            ordem_servico.descricao_execucao,
            ordem_servico.pecas_usadas,
            ordem_servico.data_execucao,
            ordem_servico.hora_inicio,
            ordem_servico.hora_fim,
            ordem_servico.quantidade_pessoas
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Ordem de serviço cadastrada com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar ordem de serviço. Erro: {erro}")

    def buscar_por_id(self, id_os):
        sql = """
        SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
               criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
               hora_inicio, hora_fim, quantidade_pessoas, criado_em
        FROM ordens_servico
        WHERE id_os = %s
        """
        try:
            self.db.cursor.execute(sql, (id_os,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_ordem_servico(registro)
        except Exception as erro:
            print(f"Erro ao buscar ordem de serviço pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
                   criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
                   hora_inicio, hora_fim, quantidade_pessoas, criado_em
            FROM ordens_servico
            ORDER BY data_execucao DESC, id_os DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            ordens = []
            for registro in registros:
                ordens.append(self.criar_ordem_servico(registro))
            return ordens
        except Exception as erro:
            print(f"Erro ao listar ordens de serviço: {erro}")
            return []

    def listar_por_maquina(self, maquina_id):
        sql = """
            SELECT id_os, solicitacao_id, maquina_id, turma_id, tipo_manutencao,
                   criticidade_os, descricao_execucao, pecas_usadas, data_execucao,
                   hora_inicio, hora_fim, quantidade_pessoas, criado_em
            FROM ordens_servico
            WHERE maquina_id = %s
            ORDER BY data_execucao DESC, id_os DESC
        """
        try:
            self.db.cursor.execute(sql, (maquina_id,))
            registros = self.db.cursor.fetchall()
            return [self.criar_ordem_servico(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar ordens de serviço da máquina: {erro}")
            return []

    def atualizar(self, ordem_servico):
        sql = """UPDATE ordens_servico
        SET
            turma_id = %s,
            tipo_manutencao = %s,
            criticidade_os = %s,
            descricao_execucao = %s,
            pecas_usadas = %s,
            data_execucao = %s,
            hora_inicio = %s,
            hora_fim = %s,
            quantidade_pessoas = %s
        WHERE id_os = %s
        """
        valores = (
            ordem_servico.turma_id,
            ordem_servico.tipo_manutencao,
            ordem_servico.criticidade_os,
            ordem_servico.descricao_execucao,
            ordem_servico.pecas_usadas,
            ordem_servico.data_execucao,
            ordem_servico.hora_inicio,
            ordem_servico.hora_fim,
            ordem_servico.quantidade_pessoas,
            ordem_servico.id_os
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Ordem de serviço não encontrada!")
            else:
                print("Ordem de serviço atualizada!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar ordem de serviço: {erro}")

    def excluir(self, id_os):
        """DELETE físico na tabela principal: o trigger
        trg_soft_delete_ordens_servico intercepta e copia a linha para
        ordens_servico_deletados antes de concluir a remoção aqui.
        """
        sql = """
            DELETE FROM ordens_servico
            WHERE id_os = %s
        """
        try:
            self.db.cursor.execute(sql, (id_os,))
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Ordem de serviço não encontrada!")
            else:
                print("Ordem de serviço excluída com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir ordem de serviço: {erro}")

    def fechar(self):
        self.db.fechar()