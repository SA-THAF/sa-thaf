from database.conexao import Conexao
from models.alerta_estoque import AlertaEstoque


class AlertaEstoqueRepository:
    """alertas_estoque usa soft delete por HERANÇA: o DELETE é
    interceptado pelo trigger trg_soft_delete_alertas_estoque, que
    copia a linha para alertas_estoque_deletados e deixa o DELETE
    original concluir na tabela principal. Por isso todas as leituras
    aqui usam "FROM ONLY alertas_estoque" — sem o ONLY, o Postgres
    também devolveria as linhas já excluídas (herdadas pela tabela
    filha).
    """

    def __init__(self):
        self.db = Conexao()

    def criar_alerta(self, registro):
        return AlertaEstoque(
            id_alerta=registro[0],
            item_id=registro[1],
            mensagem_alerta=registro[2],
            status=registro[3],
            criado_em=registro[4]
        )

    def salvar(self, alerta):
        sql = """
        INSERT INTO alertas_estoque
        (
            item_id,
            mensagem_alerta,
            status
        )
        VALUES
        (
            %s, %s, %s
        )
        """
        valores = (
            alerta.item_id,
            alerta.mensagem_alerta,
            alerta.status
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Alerta de estoque cadastrado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar alerta de estoque. Erro: {erro}")

    def buscar_por_id(self, id_alerta):
        sql = """
        SELECT id_alerta, item_id, mensagem_alerta, status, criado_em
        FROM ONLY alertas_estoque
        WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_alerta,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_alerta(registro)
        except Exception as erro:
            print(f"Erro ao buscar alerta de estoque pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_alerta, item_id, mensagem_alerta, status, criado_em
            FROM ONLY alertas_estoque
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            alertas = []
            for registro in registros:
                alertas.append(self.criar_alerta(registro))
            return alertas
        except Exception as erro:
            print(f"Erro ao listar alertas de estoque: {erro}")
            return []

    def listar_por_item(self, item_id):
        sql = """
            SELECT id_alerta, item_id, mensagem_alerta, status, criado_em
            FROM ONLY alertas_estoque
            WHERE item_id = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (item_id,))
            registros = self.db.cursor.fetchall()
            alertas = []
            for registro in registros:
                alertas.append(self.criar_alerta(registro))
            return alertas
        except Exception as erro:
            print(f"Erro ao listar alertas de estoque por item: {erro}")
            return []

    def atualizar(self, alerta):
        sql = """UPDATE ONLY alertas_estoque
        SET
            mensagem_alerta = %s,
            status = %s
        WHERE id_alerta = %s
        """
        valores = (
            alerta.mensagem_alerta,
            alerta.status,
            alerta.id_alerta
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Alerta de estoque não encontrado!")
            else:
                print("Alerta de estoque atualizado!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar alerta de estoque: {erro}")

    def excluir(self, id_alerta):
        if self.buscar_por_id(id_alerta) is None:
            print("Alerta de estoque não encontrado!")
            return
        sql = """
            DELETE FROM ONLY alertas_estoque
            WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_alerta,))
            self.db.commit()
            print("Alerta de estoque excluído com sucesso! (movido para o histórico)")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir alerta de estoque: {erro}")

    def fechar(self):
        self.db.fechar()