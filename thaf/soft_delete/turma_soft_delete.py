from database.conexao import Conexao
from models.turma import Turma


class TurmaSoftDelete:
    """Operações sobre turmas EXCLUÍDAS (deleted_at IS NOT NULL).

    turmas usa soft delete IN-PLACE: o DELETE do TurmaRepository não
    apaga a linha, só marca deleted_at = now(). Esta classe é o lado
    "administrativo" disso — ver o que foi excluído e, se for o caso,
    restaurar. Fica em pasta separada de repositories/ de propósito: o
    CRUD normal (repositories/turma_repository.py) nunca deveria
    enxergar registros excluídos, então essa consulta especial não
    entra lá.

    Não existe "excluir_definitivamente": o trigger trg_soft_delete_turmas
    intercepta TODO DELETE na tabela (mesmo uma turma já excluída) e
    converte em UPDATE deleted_at = now(). Isso é proposital — turmas é
    um catálogo pequeno e o schema garante que a linha nunca some
    fisicamente por essa via.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_turma(self, registro):
        return Turma(
            id_turma=registro[0],
            codigo_turma=registro[1],
            periodo_turma=registro[2],
            deleted_at=registro[3]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_turma, codigo_turma, periodo_turma, deleted_at
            FROM turmas
            WHERE deleted_at IS NOT NULL
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            turmas = []

            for registro in registros:
                turmas.append(self.criar_turma(registro))
            return turmas

        except Exception as erro:
            print(f"Erro ao listar turmas excluídas: {erro}")
            return []

    def buscar_excluido_por_id(self, id_turma):
        sql = """
            SELECT id_turma, codigo_turma, periodo_turma, deleted_at
            FROM turmas
            WHERE id_turma = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_turma(registro)

        except Exception as erro:
            print(f"Erro ao buscar turma excluída pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_turma):
        if self.buscar_excluido_por_id(id_turma) is None:
            print("Turma excluída não encontrada!")
            return

        sql = """
            UPDATE turmas
            SET deleted_at = NULL
            WHERE id_turma = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_turma,))
            self.db.commit()
            print("Turma restaurada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar turma: {erro}")

    def fechar(self):
        self.db.fechar()