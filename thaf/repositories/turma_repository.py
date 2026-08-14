from database.conexao import Conexao
from models.turma import Turma


class TurmaRepository:
    """turmas usa soft delete IN-PLACE: o DELETE é convertido em
    UPDATE deleted_at pelo trigger trg_soft_delete_turmas. Por isso o
    cursor.rowcount do DELETE não é confiável — excluir() confere a
    existência antes, com buscar_por_id().
    """

    def __init__(self):
        self.db = Conexao()

    def criar_turma(self, registro):
        return Turma(
            id_turma=registro[0],
            codigo_turma=registro[1],
            periodo_turma=registro[2]
        )

    def salvar(self, turma):
        sql = """
        INSERT INTO turmas
        (
            codigo_turma,
            periodo_turma
        )
        VALUES
        (
            %s, %s
        )
        """
        valores = (
            turma.codigo_turma,
            turma.periodo_turma
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Turma cadastrada com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar turma. Erro: {erro}")

    def buscar_por_id(self, id_turma):
        sql = """
        SELECT id_turma, codigo_turma, periodo_turma
        FROM turmas
        WHERE id_turma = %s AND deleted_at IS NULL
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_turma(registro)
        except Exception as erro:
            print(f"Erro ao buscar turma pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_turma, codigo_turma, periodo_turma
            FROM turmas
            WHERE deleted_at IS NULL
            ORDER BY codigo_turma
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            turmas = []
            for registro in registros:
                turmas.append(self.criar_turma(registro))
            return turmas
        except Exception as erro:
            print(f"Erro ao listar turmas: {erro}")
            return []

    def atualizar(self, turma):
        sql = """UPDATE turmas
        SET
            codigo_turma = %s,
            periodo_turma = %s
        WHERE id_turma = %s AND deleted_at IS NULL
        """
        valores = (
            turma.codigo_turma,
            turma.periodo_turma,
            turma.id_turma
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Turma não encontrada!")
            else:
                print("Turma atualizada!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar turma: {erro}")

    def excluir(self, id_turma):
        if self.buscar_por_id(id_turma) is None:
            print("Turma não encontrada!")
            return
        sql = """
            DELETE FROM turmas
            WHERE id_turma = %s
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            self.db.commit()
            print("Turma excluída com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir turma: {erro}")

    def fechar(self):
        self.db.fechar()