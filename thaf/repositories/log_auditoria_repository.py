from database.conexao import Conexao
from models.log_auditoria import LogAuditoria
 
 
class LogAuditoriaRepository:
    """logs_auditoria usa soft delete por HERANÇA: o trigger
    trg_soft_delete_logs_auditoria (fn_mover_para_historico) copia a
    linha para logs_auditoria_deletados e devolve OLD, permitindo que o
    DELETE conclua normalmente na tabela principal. Ou seja, ao contrário
    de perfis (soft delete in-place), aqui o registro REALMENTE some de
    "logs_auditoria" — por isso não existe filtro de deleted_at nas
    consultas abaixo, e o cursor.rowcount do DELETE é confiável.
 
    Para auditoria/histórico (registros ativos + excluídos), use
    listar_historico(), que consulta a view vw_todos_logs_auditoria.

    IMPORTANTE: como logs_auditoria_deletados é filha por herança de
    logs_auditoria, todo SELECT/DELETE aqui usa "ONLY logs_auditoria" —
    sem o ONLY, o Postgres também enxergaria/afetaria os logs já movidos
    para o histórico.
    """
 
    def __init__(self):
        self.db = Conexao()
 
    def criar_log_auditoria(self, registro):
        return LogAuditoria(
            id=registro[0],
            usuario_id=registro[1],
            acao=registro[2],
            endereco_ip=registro[3],
            criado_em=registro[4]
        )
 
    def salvar(self, log_auditoria):
        sql = """
        INSERT INTO logs_auditoria
        (
            usuario_id,
            acao,
            endereco_ip
        )
        VALUES
        (
            %s, %s, %s
        )
        """
        valores = (
            log_auditoria.usuario_id,
            log_auditoria.acao,
            log_auditoria.endereco_ip
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Log de auditoria registrado com sucesso!")
 
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao registrar log de auditoria. Erro: {erro}")
 
    def buscar_por_id(self, id_log):
        sql = """
        SELECT id, usuario_id, acao, endereco_ip, criado_em
        FROM ONLY logs_auditoria
        WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_log,))
            registro = self.db.cursor.fetchone()
 
            if registro is None:
                return None
 
            return self.criar_log_auditoria(registro)
 
        except Exception as erro:
            print(f"Erro ao buscar log de auditoria pelo id. Erro: {erro}")
            return None
 
    def listar(self):
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em
            FROM ONLY logs_auditoria
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            logs = []
 
            for registro in registros:
                logs.append(self.criar_log_auditoria(registro))
            return logs
 
        except Exception as erro:
            print(f"Erro ao listar logs de auditoria: {erro}")
            return []
 
    def listar_por_usuario(self, usuario_id):
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em
            FROM ONLY logs_auditoria
            WHERE usuario_id = %s
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql, (usuario_id,))
            registros = self.db.cursor.fetchall()
            logs = []
 
            for registro in registros:
                logs.append(self.criar_log_auditoria(registro))
            return logs
 
        except Exception as erro:
            print(f"Erro ao listar logs de auditoria por usuário: {erro}")
            return []
 
    def listar_historico(self):
        """Consulta vw_todos_logs_auditoria: retorna registros ativos e os
        que já foram movidos para logs_auditoria_deletados (inclui a
        coluna deleted_at, NULL para os ainda ativos)."""
        sql = """
            SELECT id, usuario_id, acao, endereco_ip, criado_em, deleted_at
            FROM vw_todos_logs_auditoria
            ORDER BY criado_em DESC
        """
        try:
            self.db.cursor.execute(sql)
            return self.db.cursor.fetchall()
 
        except Exception as erro:
            print(f"Erro ao listar histórico de logs de auditoria: {erro}")
            return []
 
    def excluir(self, id_log):
        sql = """
            DELETE FROM ONLY logs_auditoria
            WHERE id = %s
        """
        try:
            self.db.cursor.execute(sql, (id_log,))
            self.db.commit()
 
            if self.db.cursor.rowcount == 0:
                print("Log de auditoria não encontrado!")
            else:
                print("Log de auditoria excluído com sucesso (movido para o histórico)!")
 
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir log de auditoria: {erro}")
 
    def fechar(self):
        self.db.fechar()