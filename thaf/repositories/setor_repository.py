from database.conexao import Conexao
from models.setor import Setor


class SetorRepository:
    """setores usa soft delete IN-PLACE: o DELETE é convertido em
    UPDATE deleted_at pelo trigger trg_soft_delete_setores. Por isso o
    cursor.rowcount do DELETE não é confiável — excluir() confere a
    existência antes, com buscar_por_id().
    """

    def __init__(self):
        self.db = Conexao()

    def criar_setor(self, registro):
        return Setor(
            id_setor=registro[0],
            nome_setor=registro[1],
            descricao_setor=registro[2]
        )

    def salvar(self, setor):
        sql = """
        INSERT INTO setores
        (
            nome_setor,
            descricao_setor
        )
        VALUES
        (
            %s, %s
        )
        """
        valores = (
            setor.nome_setor,
            setor.descricao_setor
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Setor cadastrado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar setor. Erro: {erro}")

    def buscar_por_id(self, id_setor):
        sql = """
        SELECT id_setor, nome_setor, descricao_setor
        FROM setores
        WHERE id_setor = %s AND deleted_at IS NULL
        """
        try:
            self.db.cursor.execute(sql, (id_setor,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_setor(registro)
        except Exception as erro:
            print(f"Erro ao buscar setor pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_setor, nome_setor, descricao_setor
            FROM setores
            WHERE deleted_at IS NULL
            ORDER BY nome_setor
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            setores = []
            for registro in registros:
                setores.append(self.criar_setor(registro))
            return setores
        except Exception as erro:
            print(f"Erro ao listar setores: {erro}")
            return []

    def atualizar(self, setor):
        sql = """UPDATE setores
        SET
            nome_setor = %s,
            descricao_setor = %s
        WHERE id_setor = %s AND deleted_at IS NULL
        """
        valores = (
            setor.nome_setor,
            setor.descricao_setor,
            setor.id_setor
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Setor não encontrado!")
            else:
                print("Setor atualizado!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar setor: {erro}")

    def excluir(self, id_setor):
        if self.buscar_por_id(id_setor) is None:
            print("Setor não encontrado!")
            return
        sql = """
            DELETE FROM setores
            WHERE id_setor = %s
        """
        try:
            self.db.cursor.execute(sql, (id_setor,))
            self.db.commit()
            print("Setor excluído com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir setor: {erro}")

    def fechar(self):
        self.db.fechar()