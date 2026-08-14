from database.conexao import Conexao
from models.perfil import Perfil

class PerfilRepository:
    """perfis usa soft delete IN-PLACE: o DELETE é convertido em
    UPDATE deleted_at pelo trigger trg_soft_delete_perfis. Por isso o
    cursor.rowcount do DELETE não é confiável — excluir() confere a
    existência antes, com buscar_por_id().
    """

    def __init__(self):
        self.db = Conexao()

    def criar_perfil(self, registro):
        return Perfil(
            id_perfil=registro[0],
            nome_perfil=registro[1],
            descricao_perfil=registro[2]
        )

    def salvar(self, perfil):
        sql = """
        INSERT INTO perfis
        (
            nome_perfil,
            descricao_perfil
        )
        VALUES
        (
            %s, %s
        )
        """
        valores = (
            perfil.nome_perfil,
            perfil.descricao_perfil
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Perfil cadastrado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar perfil. Erro: {erro}")

    def buscar_por_id(self, id_perfil):
        sql = """
        SELECT id_perfil, nome_perfil, descricao_perfil
        FROM perfis
        WHERE id_perfil = %s AND deleted_at IS NULL
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_perfil(registro)

        except Exception as erro:
            print(f"Erro ao buscar perfil pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_perfil, nome_perfil, descricao_perfil
            FROM perfis
            WHERE deleted_at IS NULL
            ORDER BY nome_perfil
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            perfis = []

            for registro in registros:
                perfis.append(self.criar_perfil(registro))
            return perfis

        except Exception as erro:
            print(f"Erro ao listar perfis: {erro}")
            return []

    def atualizar(self, perfil):
        sql = """UPDATE perfis
        SET
            nome_perfil = %s,
            descricao_perfil = %s
        WHERE id_perfil = %s AND deleted_at IS NULL
        """
        valores = (
            perfil.nome_perfil,
            perfil.descricao_perfil,
            perfil.id_perfil
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Perfil não encontrado!")

            else:
                print("Perfil atualizado!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar perfil: {erro}")

    def excluir(self, id_perfil):
        if self.buscar_por_id(id_perfil) is None:
            print("Perfil não encontrado!")
            return

        sql = """
            DELETE FROM perfis
            WHERE id_perfil = %s
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            self.db.commit()
            print("Perfil excluído com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir perfil: {erro}")

    def fechar(self):
        self.db.fechar()