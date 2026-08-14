from database.conexao import Conexao
from models.registro_quebra import RegistroQuebra


class RegistroQuebraRepository:
    """registros_quebra usa soft delete por HERANÇA: um DELETE aciona o
    trigger trg_soft_delete_registros_quebra (fn_mover_para_historico), que
    copia a linha para registros_quebra_deletados e deixa o DELETE original
    concluir na tabela principal. Por isso, ao contrário de perfis, o
    cursor.rowcount do DELETE aqui É confiável (a linha realmente some da
    tabela principal).

    Todas as consultas usam "FROM ONLY registros_quebra" / "UPDATE ONLY" /
    "DELETE FROM ONLY" para nunca enxergar ou afetar linhas que já estão em
    registros_quebra_deletados (por padrão, o Postgres inclui as tabelas
    filhas nas consultas ao pai).
    """

    def __init__(self):
        self.db = Conexao()

    def criar_registro(self, registro):
        return RegistroQuebra(
            id_quebra=registro[0],
            item_id=registro[1],
            usuario_id=registro[2],
            descricao_quebra=registro[3],
            foto_url=registro[4],
            criado_em=registro[5]
        )

    def salvar(self, registro_quebra):
        sql = """
        INSERT INTO registros_quebra
        (
            item_id,
            usuario_id,
            descricao_quebra,
            foto_url
        )
        VALUES
        (
            %s, %s, %s, %s
        )
        """
        valores = (
            registro_quebra.item_id,
            registro_quebra.usuario_id,
            registro_quebra.descricao_quebra,
            registro_quebra.foto_url
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Registro de quebra cadastrado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar registro de quebra. Erro: {erro}")

    def buscar_por_id(self, id_quebra):
        sql = """
        SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url, criado_em
        FROM ONLY registros_quebra
        WHERE id_quebra = %s
        """
        try:
            self.db.cursor.execute(sql, (id_quebra,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_registro(registro)
        except Exception as erro:
            print(f"Erro ao buscar registro de quebra pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url, criado_em
            FROM ONLY registros_quebra
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            quebras = []
            for registro in registros:
                quebras.append(self.criar_registro(registro))
            return quebras
        except Exception as erro:
            print(f"Erro ao listar registros de quebra: {erro}")
            return []

    def atualizar(self, registro_quebra):
        sql = """UPDATE ONLY registros_quebra
        SET
            descricao_quebra = %s,
            foto_url = %s
        WHERE id_quebra = %s
        """
        valores = (
            registro_quebra.descricao_quebra,
            registro_quebra.foto_url,
            registro_quebra.id_quebra
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Registro de quebra não encontrado!")
            else:
                print("Registro de quebra atualizado!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar registro de quebra: {erro}")

    def excluir(self, id_quebra):
        sql = """
            DELETE FROM ONLY registros_quebra
            WHERE id_quebra = %s
        """
        try:
            self.db.cursor.execute(sql, (id_quebra,))
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Registro de quebra não encontrado!")
            else:
                print("Registro de quebra excluído com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir registro de quebra: {erro}")

    def fechar(self):
        self.db.fechar()