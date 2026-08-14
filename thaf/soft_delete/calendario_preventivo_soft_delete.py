# soft_delete/calendario_preventivo_soft_delete.py

from database.conexao import Conexao
from models.calendario_preventivo import CalendarioPreventivo


class CalendarioPreventivoSoftDelete:
    """Operações sobre calendários preventivos EXCLUÍDOS.

    calendario_preventivo usa soft delete por HERANÇA: ao excluir, o
    trigger trg_soft_delete_calendario_preventivo copia a linha inteira
    para calendario_preventivo_deletados (com deleted_at preenchido) e
    deixa o DELETE original concluir na tabela principal. Por isso esta
    classe consulta diretamente a tabela de histórico
    calendario_preventivo_deletados, e não a tabela principal — que nunca
    guarda registros excluídos nesse padrão.

    Como PRIMARY KEY, UNIQUE e FOREIGN KEY não são herdados pela tabela
    filha (proposital, ver notas do schema), restaurar() faz a operação
    em duas etapas na mesma conexão: INSERT de volta na tabela principal
    (usando OVERRIDING SYSTEM VALUE para reaproveitar o id, já que a
    coluna é GENERATED ALWAYS AS IDENTITY) seguido do DELETE na tabela
    de histórico. Não existe UPDATE aqui: a linha muda fisicamente de
    tabela, não de estado.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_calendario(self, registro):
        return CalendarioPreventivo(
            id_calendario=registro[0],
            maquina_id=registro[1],
            turma_id=registro[2],
            responsavel_id=registro[3],
            titulo_calendario=registro[4],
            descricao_calendario=registro[5],
            frequencia_calendario=registro[6],
            data_proxima_execucao=registro[7],
            status=registro[8],
            criado_em=registro[9],
            deleted_at=registro[10]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_calendario, maquina_id, turma_id, responsavel_id,
                   titulo_calendario, descricao_calendario, frequencia_calendario,
                   data_proxima_execucao, status, criado_em, deleted_at
            FROM calendario_preventivo_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            calendarios = []
            for registro in registros:
                calendarios.append(self.criar_calendario(registro))
            return calendarios
        except Exception as erro:
            print(f"Erro ao listar calendários preventivos excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_calendario):
        sql = """
            SELECT id_calendario, maquina_id, turma_id, responsavel_id,
                   titulo_calendario, descricao_calendario, frequencia_calendario,
                   data_proxima_execucao, status, criado_em, deleted_at
            FROM calendario_preventivo_deletados
            WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_calendario,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_calendario(registro)
        except Exception as erro:
            print(f"Erro ao buscar calendário preventivo excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_calendario):
        calendario = self.buscar_excluido_por_id(id_calendario)

        if calendario is None:
            print("Calendário preventivo excluído não encontrado!")
            return

        sql_insert = """
            INSERT INTO calendario_preventivo
            (
                id_calendario, maquina_id, turma_id, responsavel_id,
                titulo_calendario, descricao_calendario, frequencia_calendario,
                data_proxima_execucao, status, criado_em
            )
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        sql_delete = """
            DELETE FROM calendario_preventivo_deletados
            WHERE id_calendario = %s
        """
        try:
            self.db.cursor.execute(sql_insert, (
                calendario.id_calendario,
                calendario.maquina_id,
                calendario.turma_id,
                calendario.responsavel_id,
                calendario.titulo_calendario,
                calendario.descricao_calendario,
                calendario.frequencia_calendario,
                calendario.data_proxima_execucao,
                calendario.status,
                calendario.criado_em
            ))
            self.db.cursor.execute(sql_delete, (id_calendario,))
            self.db.commit()
            print("Calendário preventivo restaurado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar calendário preventivo: {erro}")

    def fechar(self):
        self.db.fechar()