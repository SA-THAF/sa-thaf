from database.conexao import Conexao
from models.setor import Setor


class SetorSoftDelete:
    """Operações sobre setores EXCLUÍDOS (deleted_at IS NOT NULL).
    setores usa soft delete IN-PLACE: o DELETE do SetorRepository não
    apaga a linha, só marca deleted_at = now(). Esta classe é o lado
    "administrativo" disso — ver o que foi excluído e, se for o caso,
    restaurar. Fica em pasta separada de repositories/ de propósito: o
    CRUD normal (repositories/setor_repository.py) nunca deveria
    enxergar registros excluídos, então essa consulta especial não
    entra lá.

    Não existe "excluir_definitivamente": o trigger trg_soft_delete_setores
    intercepta TODO DELETE na tabela (mesmo um setor já excluído) e
    converte em UPDATE deleted_at = now(). Isso é proposital — setores é
    um catálogo pequeno e o schema garante que a linha nunca some
    fisicamente por essa via.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_setor(self, registro):
        return Setor(
            id_setor=registro[0],
            nome_setor=registro[1],
            descricao_setor=registro[2],
            deleted_at=registro[3]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_setor, nome_setor, descricao_setor, deleted_at
            FROM setores
            WHERE deleted_at IS NOT NULL
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            setores = []
            for registro in registros:
                setores.append(self.criar_setor(registro))
            return setores
        except Exception as erro:
            print(f"Erro ao listar setores excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_setor):
        sql = """
            SELECT id_setor, nome_setor, descricao_setor, deleted_at
            FROM setores
            WHERE id_setor = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_setor,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_setor(registro)
        except Exception as erro:
            print(f"Erro ao buscar setor excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_setor):
        if self.buscar_excluido_por_id(id_setor) is None:
            print("Setor excluído não encontrado!")
            return
        sql = """
            UPDATE setores
            SET deleted_at = NULL
            WHERE id_setor = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_setor,))
            self.db.commit()
            print("Setor restaurado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar setor: {erro}")

    def fechar(self):
        self.db.fechar()