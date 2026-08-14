from database.conexao import Conexao
from models.maquina import Maquina

class MaquinaRepository:
    """maquinas usa soft delete por HERANÇA: o trigger
    trg_soft_delete_maquinas copia a linha pra maquinas_deletados ANTES
    do DELETE e deixa o DELETE físico terminar na tabela principal.
    Diferente de perfis, aqui o DELETE realmente acontece na tabela
    "maquinas" (só que a linha já foi salva no histórico antes) — então
    cursor.rowcount É confiável.

    IMPORTANTE: como "maquinas" tem uma tabela filha (maquinas_deletados)
    por herança, todo SELECT/UPDATE/DELETE daqui usa "ONLY maquinas".
    Sem o ONLY, o Postgres também enxerga as linhas já excluídas
    (histórico), o que quebraria o CRUD normal.
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
            ultima_manutencao=registro[5]
        )

    def salvar(self, maquina):
        sql = """
        INSERT INTO maquinas
        (
            setor_id,
            tag_maquina,
            nome_maquina,
            status_vivo
        )
        VALUES
        (
            %s, %s, %s, %s
        )
        """
        valores = (
            maquina.setor_id,
            maquina.tag_maquina,
            maquina.nome_maquina,
            maquina.status_vivo
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Máquina cadastrada com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar máquina. Erro: {erro}")

    def buscar_por_id(self, id_maquina):
        sql = """
        SELECT id_maquina, setor_id, tag_maquina, nome_maquina, status_vivo, ultima_manutencao
        FROM ONLY maquinas
        WHERE id_maquina = %s
        """
        try:
            self.db.cursor.execute(sql, (id_maquina,))
            registro = self.db.cursor.fetchone()

            if registro is None:
                return None

            return self.criar_maquina(registro)

        except Exception as erro:
            print(f"Erro ao buscar máquina pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_maquina, setor_id, tag_maquina, nome_maquina, status_vivo, ultima_manutencao
            FROM ONLY maquinas
            ORDER BY tag_maquina
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            maquinas = []

            for registro in registros:
                maquinas.append(self.criar_maquina(registro))
            return maquinas

        except Exception as erro:
            print(f"Erro ao listar máquinas: {erro}")
            return []

    def atualizar(self, maquina):
        sql = """UPDATE ONLY maquinas
        SET
            setor_id = %s,
            tag_maquina = %s,
            nome_maquina = %s,
            status_vivo = %s
        WHERE id_maquina = %s
        """
        valores = (
            maquina.setor_id,
            maquina.tag_maquina,
            maquina.nome_maquina,
            maquina.status_vivo,
            maquina.id_maquina
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Máquina não encontrada!")

            else:
                print("Máquina atualizada!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar máquina: {erro}")

    def excluir(self, id_maquina):
        sql = """
            DELETE FROM ONLY maquinas
            WHERE id_maquina = %s
        """
        try:
            self.db.cursor.execute(sql, (id_maquina,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Máquina não encontrada!")
            else:
                print("Máquina excluída com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir máquina: {erro}")

    def fechar(self):
        self.db.fechar()