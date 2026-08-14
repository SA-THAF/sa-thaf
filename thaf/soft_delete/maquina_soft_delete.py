from database.conexao import Conexao
from models.maquina import Maquina

class MaquinaSoftDelete:
    """Operações sobre máquinas EXCLUÍDAS.

    maquinas usa soft delete por HERANÇA: trg_soft_delete_maquinas
    (BEFORE DELETE em maquinas) copia a linha pra maquinas_deletados e
    deixa o DELETE físico terminar na tabela principal. Ou seja, a
    linha some de "maquinas" de verdade e passa a existir só em
    "maquinas_deletados" — diferente de perfis (soft delete in-place,
    mesma tabela, só marcando deleted_at).

    Por isso:
    - listar_excluidos()/buscar_excluido_por_id() leem direto de
      maquinas_deletados.
    - restaurar() precisa fazer o caminho inverso na mão: INSERT de
      volta em "maquinas" (com OVERRIDING SYSTEM VALUE, já que
      id_maquina é GENERATED ALWAYS AS IDENTITY) e DELETE da linha em
      maquinas_deletados, tudo na mesma transação.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_maquina(self, registro):
        return Maquina(
            id_maquina=registro[0],
            setor_id=registro[1],
            tag_maquina=registro[2],
            nome_maquina=registro[3],
            status_vivo=registro[4],
            ultima_manutencao=registro[5],
            deleted_at=registro[6]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_maquina, setor_id, tag_maquina, nome_maquina, status_vivo, ultima_manutencao, deleted_at
            FROM maquinas_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            maquinas = []

            for registro in registros:
                maquinas.append(self.criar_maquina(registro))
            return maquinas

        except Exception as erro:
            print(f"Erro ao listar máquinas excluídas: {erro}")
            return []

    def buscar_excluido_por_id(self, id_maquina):
        sql = """
            SELECT id_maquina, setor_id, tag_maquina, nome_maquina, status_vivo, ultima_manutencao, deleted_at
            FROM maquinas_deletados
            WHERE id_maquina = %s
        """
        try:
            self.db.cursor.execute(sql, (id_maquina,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_maquina(registro)

        except Exception as erro:
            print(f"Erro ao buscar máquina excluída pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_maquina):
        if self.buscar_excluido_por_id(id_maquina) is None:
            print("Máquina excluída não encontrada!")
            return

        sql_insert = """
            INSERT INTO maquinas
            (id_maquina, setor_id, tag_maquina, nome_maquina, status_vivo, ultima_manutencao)
            OVERRIDING SYSTEM VALUE
            SELECT id_maquina, setor_id, tag_maquina, nome_maquina, status_vivo, ultima_manutencao
            FROM maquinas_deletados
            WHERE id_maquina = %s
        """
        sql_delete = """
            DELETE FROM maquinas_deletados
            WHERE id_maquina = %s
        """
        try:
            self.db.cursor.execute(sql_insert, (id_maquina,))
            self.db.cursor.execute(sql_delete, (id_maquina,))
            self.db.commit()
            print("Máquina restaurada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar máquina: {erro}")

    def fechar(self):
        self.db.fechar()