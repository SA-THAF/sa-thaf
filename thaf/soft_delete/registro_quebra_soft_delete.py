from database.conexao import Conexao
from models.registro_quebra import RegistroQuebra


class RegistroQuebraSoftDelete:
    """Operações sobre registros de quebra EXCLUÍDOS.

    registros_quebra usa soft delete por HERANÇA: ao excluir, o trigger
    trg_soft_delete_registros_quebra move a linha para
    registros_quebra_deletados (via fn_mover_para_historico) e deixa o
    DELETE concluir na tabela principal — a linha some fisicamente de
    registros_quebra e passa a existir apenas em registros_quebra_deletados.

    Por isso, ao contrário de perfis (soft delete in-place), esta classe
    consulta uma TABELA separada (registros_quebra_deletados), e não uma
    coluna deleted_at na mesma tabela. Fica em pasta separada de
    repositories/ pelo mesmo motivo do módulo de perfis: o CRUD normal
    (repositories/registro_quebra_repository.py) nunca deveria enxergar
    registros já excluídos.

    restaurar() não tem função de trigger equivalente no schema (o padrão
    de herança não prevê "UNDELETE" automático), então a restauração é
    feita manualmente aqui: a linha é reinserida em registros_quebra
    preservando o id_quebra original (com OVERRIDING SYSTEM VALUE, já que
    id_quebra é GENERATED ALWAYS AS IDENTITY) e depois removida de
    registros_quebra_deletados.
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
            criado_em=registro[5],
            deleted_at=registro[6]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url,
                   criado_em, deleted_at
            FROM registros_quebra_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            quebras = []
            for registro in registros:
                quebras.append(self.criar_registro(registro))
            return quebras
        except Exception as erro:
            print(f"Erro ao listar registros de quebra excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_quebra):
        sql = """
            SELECT id_quebra, item_id, usuario_id, descricao_quebra, foto_url,
                   criado_em, deleted_at
            FROM registros_quebra_deletados
            WHERE id_quebra = %s
        """
        try:
            self.db.cursor.execute(sql, (id_quebra,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_registro(registro)
        except Exception as erro:
            print(f"Erro ao buscar registro de quebra excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_quebra):
        registro = self.buscar_excluido_por_id(id_quebra)
        if registro is None:
            print("Registro de quebra excluído não encontrado!")
            return

        sql_inserir = """
            INSERT INTO registros_quebra
            (id_quebra, item_id, usuario_id, descricao_quebra, foto_url, criado_em)
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        sql_remover_historico = """
            DELETE FROM registros_quebra_deletados
            WHERE id_quebra = %s
        """
        try:
            self.db.cursor.execute(sql_inserir, (
                registro.id_quebra,
                registro.item_id,
                registro.usuario_id,
                registro.descricao_quebra,
                registro.foto_url,
                registro.criado_em
            ))
            self.db.cursor.execute(sql_remover_historico, (id_quebra,))
            self.db.commit()
            print("Registro de quebra restaurado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar registro de quebra: {erro}")

    def fechar(self):
        self.db.fechar()