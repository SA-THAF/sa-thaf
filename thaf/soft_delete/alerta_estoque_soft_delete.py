from database.conexao import Conexao
from models.alerta_estoque import AlertaEstoque


class AlertaEstoqueSoftDelete:
    """Operações sobre alertas de estoque EXCLUÍDOS.

    Diferente de perfis (soft delete IN-PLACE), alertas_estoque usa o
    padrão de HERANÇA: o trigger trg_soft_delete_alertas_estoque copia
    a linha para alertas_estoque_deletados e conclui o DELETE físico na
    tabela principal. Por isso esta classe consulta a tabela filha
    diretamente, e não uma coluna deleted_at na tabela principal.

    Como PRIMARY KEY/UNIQUE não são herdadas pela tabela filha, e
    id_alerta é GENERATED ALWAYS AS IDENTITY na tabela pai, restaurar()
    precisa de OVERRIDING SYSTEM VALUE para reinserir a linha com o
    mesmo id_alerta que ela tinha antes de ser excluída.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_alerta(self, registro):
        return AlertaEstoque(
            id_alerta=registro[0],
            item_id=registro[1],
            mensagem_alerta=registro[2],
            status=registro[3],
            criado_em=registro[4],
            deleted_at=registro[5]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_alerta, item_id, mensagem_alerta, status, criado_em, deleted_at
            FROM alertas_estoque_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            alertas = []
            for registro in registros:
                alertas.append(self.criar_alerta(registro))
            return alertas
        except Exception as erro:
            print(f"Erro ao listar alertas de estoque excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_alerta):
        sql = """
            SELECT id_alerta, item_id, mensagem_alerta, status, criado_em, deleted_at
            FROM alertas_estoque_deletados
            WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_alerta,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_alerta(registro)
        except Exception as erro:
            print(f"Erro ao buscar alerta de estoque excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_alerta):
        alerta = self.buscar_excluido_por_id(id_alerta)
        if alerta is None:
            print("Alerta de estoque excluído não encontrado!")
            return

        sql_insert = """
            INSERT INTO alertas_estoque
            (id_alerta, item_id, mensagem_alerta, status, criado_em)
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s)
        """
        sql_delete = """
            DELETE FROM alertas_estoque_deletados
            WHERE id_alerta = %s
        """
        try:
            self.db.cursor.execute(sql_insert, (
                alerta.id_alerta,
                alerta.item_id,
                alerta.mensagem_alerta,
                alerta.status,
                alerta.criado_em
            ))
            self.db.cursor.execute(sql_delete, (id_alerta,))
            self.db.commit()
            print("Alerta de estoque restaurado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar alerta de estoque: {erro}")

    def fechar(self):
        self.db.fechar()