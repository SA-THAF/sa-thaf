from database.conexao import Conexao


class LogAuditoriaSoftDelete:
    """Suporte ao padrão de soft delete por HERANÇA de logs_auditoria.

    Quando um registro é excluído, o trigger trg_soft_delete_logs_auditoria
    (fn_mover_para_historico) copia a linha para logs_auditoria_deletados
    e deixa o DELETE concluir na tabela principal. A partir daí, este
    módulo é quem sabe operar sobre logs_auditoria_deletados:

    - listar_excluidos(): lista o que está no histórico.
    - restaurar(id): reinsere o registro em logs_auditoria e remove de
      logs_auditoria_deletados (a linha volta a existir "ativa").
    - expurgar(id): apaga em definitivo o registro do histórico
      (irreversível — usar com cautela, tipicamente só por política de
      retenção de auditoria).
    """

    def __init__(self):
        self.db = Conexao()

    def listar_excluidos(self):
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em, deleted_at
            FROM logs_auditoria_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            return self.db.cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar logs de auditoria excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_log):
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em, deleted_at
            FROM logs_auditoria_deletados
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_log,))
            return self.db.cursor.fetchone()

        except Exception as erro:
            print(f"Erro ao buscar log de auditoria excluído pelo id: {erro}")
            return None

    def restaurar(self, id_log):
        registro = self.buscar_excluido_por_id(id_log)
        if registro is None:
            print("Log de auditoria excluído não encontrado!")
            return

        sql_inserir = """
            INSERT INTO logs_auditoria (id, usuario_id, acao, endereco_ip, criado_em)
            VALUES (%s, %s, %s, %s, %s)
        """
        sql_remover_historico = """
            DELETE FROM logs_auditoria_deletados
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(
                sql_inserir,
                (registro[0], registro[1], registro[2], registro[3], registro[4])
            )
            self.db.cursor.execute(sql_remover_historico, (id_log,))
            self.db.commit()
            print("Log de auditoria restaurado com sucesso!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar log de auditoria: {erro}")

    def expurgar(self, id_log):
        sql = """
            DELETE FROM logs_auditoria_deletados
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_log,))
            self.db.commit()

            if self.db.cursor.rowcount == 0:
                print("Log de auditoria excluído não encontrado!")
            else:
                print("Log de auditoria expurgado do histórico (ação irreversível)!")

        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao expurgar log de auditoria: {erro}")

    def fechar(self):
        self.db.fechar()