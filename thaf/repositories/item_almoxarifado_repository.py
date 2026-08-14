from database.conexao import Conexao
from models.item_almoxarifado import ItemAlmoxarifado


class ItemAlmoxarifadoRepository:
    """
    itens_almoxarifado usa soft delete por HERANÇA: o trigger
    trg_soft_delete_itens_almoxarifado (fn_mover_para_historico) copia a
    linha para itens_almoxarifado_deletados e deixa o DELETE concluir
    normalmente na tabela principal.

    Diferente de perfis (in-place), aqui NÃO existe coluna deleted_at em
    itens_almoxarifado, e o DELETE é físico na tabela principal (a linha
    só continua existindo no histórico). Por isso:
    - as consultas não precisam (e não devem) filtrar por deleted_at;
    - cursor.rowcount do DELETE é confiável, pois a exclusão realmente
      ocorre na tabela principal.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_item(self, registro):
        return ItemAlmoxarifado(
            id_ferramenta=registro[0],
            nome_ferramenta=registro[1],
            dimensao_ferramenta=registro[2],
            quantidade_atual=registro[3],
            estoque_minimo=registro[4],
            unidade_medida=registro[5],
            localizacao_gaveta=registro[6],
        )

    def salvar(self, item):
        sql = """
            INSERT INTO itens_almoxarifado (
                nome_ferramenta,
                dimensao_ferramenta,
                quantidade_atual,
                estoque_minimo,
                unidade_medida,
                localizacao_gaveta
            )
            VALUES (
                %s, %s, %s, %s, %s, %s
            )
        """
        valores = (
            item.nome_ferramenta,
            item.dimensao_ferramenta,
            item.quantidade_atual,
            item.estoque_minimo,
            item.unidade_medida,
            item.localizacao_gaveta
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Item de almoxarifado cadastrado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar item de almoxarifado. Erro: {erro}")

    def buscar_por_id(self, id_ferramenta):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                   quantidade_atual, estoque_minimo, unidade_medida,
                   localizacao_gaveta
            FROM itens_almoxarifado
            WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ferramenta,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_item(registro)
        except Exception as erro:
            print(f"Erro ao buscar item de almoxarifado pelo id. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                   quantidade_atual, estoque_minimo, unidade_medida,
                   localizacao_gaveta
            FROM itens_almoxarifado
            ORDER BY nome_ferramenta
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            itens = []
            for registro in registros:
                itens.append(self.criar_item(registro))
            return itens
        except Exception as erro:
            print(f"Erro ao listar itens de almoxarifado: {erro}")
            return []

    def listar_abaixo_do_minimo(self):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                   quantidade_atual, estoque_minimo, unidade_medida,
                   localizacao_gaveta
            FROM itens_almoxarifado
            WHERE quantidade_atual < estoque_minimo
            ORDER BY nome_ferramenta
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            itens = []
            for registro in registros:
                itens.append(self.criar_item(registro))
            return itens
        except Exception as erro:
            print(f"Erro ao listar itens abaixo do estoque mínimo: {erro}")
            return []

    def atualizar(self, item):
        sql = """UPDATE itens_almoxarifado
                  SET nome_ferramenta = %s,
                      dimensao_ferramenta = %s,
                      quantidade_atual = %s,
                      estoque_minimo = %s,
                      unidade_medida = %s,
                      localizacao_gaveta = %s
                  WHERE id_ferramenta = %s
        """
        valores = (
            item.nome_ferramenta,
            item.dimensao_ferramenta,
            item.quantidade_atual,
            item.estoque_minimo,
            item.unidade_medida,
            item.localizacao_gaveta,
            item.id_ferramenta
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Item de almoxarifado não encontrado!")
            else:
                print("Item de almoxarifado atualizado!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar item de almoxarifado: {erro}")

    def excluir(self, id_ferramenta):
        sql = """
            DELETE FROM itens_almoxarifado
            WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ferramenta,))
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Item de almoxarifado não encontrado!")
            else:
                print("Item de almoxarifado excluído com sucesso! (movido para itens_almoxarifado_deletados)")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir item de almoxarifado: {erro}")

    def fechar(self):
        self.db.fechar()