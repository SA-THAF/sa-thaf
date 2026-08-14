# repositories/calendario_preventivo_repository.py

from database.conexao import Conexao
from models.calendario_preventivo import CalendarioPreventivo


class CalendarioPreventivoRepository:
    """calendario_preventivo usa soft delete por HERANÇA: o DELETE aciona
    o trigger trg_soft_delete_calendario_preventivo (fn_mover_para_historico),
    que copia a linha inteira para calendario_preventivo_deletados e deixa
    o DELETE original concluir na tabela principal. Diferente do padrão
    IN-PLACE (ex.: perfis), aqui a linha realmente é removida da tabela
    principal, então o cursor.rowcount do DELETE é confiável.

    IMPORTANTE: tabelas filhas de herança no Postgres também aparecem em
    "SELECT * FROM tabela". Por isso todas as consultas abaixo usam
    "FROM ONLY calendario_preventivo", garantindo que apenas registros
    ativos sejam retornados/afetados.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_calendario(self, registro):
        return CalendarioPreventivo(
            id_calendario=registro[0],
            maquina_id=registro[1],
            turma_id=registro[2],
            responsavel_id=registro[3],
            titulo_calendario=registro[4],
            descricao_calendario=registro[5],
            frequencia_calendario=registro[6],
            data_proxima_execucao=registro[7],
            status=registro[8],
            criado_em=registro[9]
        )

    def salvar(self, calendario):
        sql = """
        INSERT INTO calendario_preventivo
        (
            maquina_id,
            turma_id,
            responsavel_id,
            titulo_calendario,
            descricao_calendario,
            frequencia_calendario,
            data_proxima_execucao,
            status
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        valores = (
            calendario.maquina_id,
            calendario.turma_id,
            calendario.responsavel_id,
            calendario.titulo_calendario,
            calendario.descricao_calendario,
            calendario.frequencia_calendario,
            calendario.data_proxima_execucao,
            calendario.status
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Calendário preventivo cadastrado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar calendário preventivo. Erro: {erro}")

    def buscar_por_id(self, id_calendario):
        sql = """
        SELECT id_calendario, maquina_id, turma_id, responsavel_id,
               titulo_calendario, descricao_calendario, frequencia_calendario,
               data_proxima_execucao, status, criado_em
        FROM ONLY calendario_preventivo
        WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_calendario,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_calendario(registro)
        except Exception as erro:
            print(f"Erro ao buscar calendário preventivo pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_calendario, maquina_id, turma_id, responsavel_id,
                   titulo_calendario, descricao_calendario, frequencia_calendario,
                   data_proxima_execucao, status, criado_em
            FROM ONLY calendario_preventivo
            ORDER BY data_proxima_execucao
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            calendarios = []
            for registro in registros:
                calendarios.append(self.criar_calendario(registro))
            return calendarios
        except Exception as erro:
            print(f"Erro ao listar calendários preventivos: {erro}")
            return []

    def atualizar(self, calendario):
        sql = """UPDATE ONLY calendario_preventivo
        SET
            maquina_id = %s,
            turma_id = %s,
            responsavel_id = %s,
            titulo_calendario = %s,
            descricao_calendario = %s,
            frequencia_calendario = %s,
            data_proxima_execucao = %s,
            status = %s
        WHERE id_calendario = %s
        """
        valores = (
            calendario.maquina_id,
            calendario.turma_id,
            calendario.responsavel_id,
            calendario.titulo_calendario,
            calendario.descricao_calendario,
            calendario.frequencia_calendario,
            calendario.data_proxima_execucao,
            calendario.status,
            calendario.id_calendario
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Calendário preventivo não encontrado!")
            else:
                print("Calendário preventivo atualizado!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar calendário preventivo: {erro}")

    def excluir(self, id_calendario):
        sql = """
            DELETE FROM ONLY calendario_preventivo
            WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_calendario,))
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Calendário preventivo não encontrado!")
            else:
                print("Calendário preventivo excluído com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir calendário preventivo: {erro}")

    def fechar(self):
        self.db.fechar()