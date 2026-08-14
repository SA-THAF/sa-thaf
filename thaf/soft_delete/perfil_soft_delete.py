from database.conexao import Conexao
from models.perfil import Perfil

class PerfilSoftDelete:
    """Operações sobre perfis EXCLUÍDOS (deleted_at IS NOT NULL).

    perfis usa soft delete IN-PLACE: o DELETE do PerfilRepository não
    apaga a linha, só marca deleted_at = now(). Esta classe é o lado
    "administrativo" disso — ver o que foi excluído e, se for o caso,
    restaurar. Fica em pasta separada de repositories/ de propósito: o
    CRUD normal (repositories/perfil_repository.py) nunca deveria
    enxergar registros excluídos, então essa consulta especial não
    entra lá.

    Não existe "excluir_definitivamente": o trigger trg_soft_delete_perfis
    intercepta TODO DELETE na tabela (mesmo um perfil já excluído) e
    converte em UPDATE deleted_at = now(). Isso é proposital — perfis é
    um catálogo pequeno e o schema garante que a linha nunca some
    fisicamente por essa via.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_perfil(self, registro):
        return Perfil(
            id_perfil=registro[0],
            nome_perfil=registro[1],
            descricao_perfil=registro[2],
            deleted_at=registro[3]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_perfil, nome_perfil, descricao_perfil, deleted_at
            FROM perfis
            WHERE deleted_at IS NOT NULL
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            perfis = []

            for registro in registros:
                perfis.append(self.criar_perfil(registro))
            return perfis

        except Exception as erro:
            print(f"Erro ao listar perfis excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_perfil):
        sql = """
            SELECT id_perfil, nome_perfil, descricao_perfil, deleted_at
            FROM perfis
            WHERE id_perfil = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_perfil(registro)

        except Exception as erro:
            print(f"Erro ao buscar perfil excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_perfil):
        if self.buscar_excluido_por_id(id_perfil) is None:
            print("Perfil excluído não encontrado!")
            return

        sql = """
            UPDATE perfis
            SET deleted_at = NULL
            WHERE id_perfil = %s AND deleted_at IS NOT NULL
        """
        try:
            self.db.cursor.execute(sql, (id_perfil,))
            self.db.commit()
            print("Perfil restaurado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar perfil: {erro}")

    def fechar(self):
        self.db.fechar()