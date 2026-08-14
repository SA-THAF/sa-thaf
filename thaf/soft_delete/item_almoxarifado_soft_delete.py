from database.conexao import Conexao
from models.item_almoxarifado import ItemAlmoxarifado


class ItemAlmoxarifadoSoftDelete:
    """
    Operações sobre itens de almoxarifado EXCLUÍDOS.

    itens_almoxarifado usa soft delete por HERANÇA: o DELETE do
    ItemAlmoxarifadoRepository é físico na tabela principal, mas o
    trigger trg_soft_delete_itens_almoxarifado (fn_mover_para_historico)
    copia a linha para itens_almoxarifado_deletados ANTES disso
    acontecer. Esta classe é o lado "administrativo" disso — ver o que
    foi excluído e, se for o caso, restaurar. Fica em pasta separada de
    repositories/ de propósito: o CRUD normal
    (repositories/item_almoxarifado_repository.py) só enxerga
    itens_almoxarifado, nunca o histórico.

    Diferente de perfis (in-place), aqui não existe "UPDATE deleted_at =
    NULL" para restaurar: o registro excluído já não está mais em
    itens_almoxarifado, então restaurar() precisa mover a linha de volta
    (INSERT ... SELECT de itens_almoxarifado_deletados para
    itens_almoxarifado, com OVERRIDING SYSTEM VALUE para preservar o
    id_ferramenta original, já que a PK é GENERATED ALWAYS AS IDENTITY)
    e então remover o registro de itens_almoxarifado_deletados.

    Também não existe "excluir_definitivamente" aqui: a remoção
    definitiva do histórico seria só um DELETE direto em
    itens_almoxarifado_deletados (tabela comum, sem trigger de soft
    delete), fora do escopo desta classe.
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
            deleted_at=registro[7]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                   quantidade_atual, estoque_minimo, unidade_medida,
                   localizacao_gaveta, deleted_at
            FROM itens_almoxarifado_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            itens = []
            for registro in registros:
                itens.append(self.criar_item(registro))
            return itens
        except Exception as erro:
            print(f"Erro ao listar itens de almoxarifado excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_ferramenta):
        sql = """
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                   quantidade_atual, estoque_minimo, unidade_medida,
                   localizacao_gaveta, deleted_at
            FROM itens_almoxarifado_deletados
            WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql, (id_ferramenta,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_item(registro)
        except Exception as erro:
            print(f"Erro ao buscar item de almoxarifado excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_ferramenta):
        if self.buscar_excluido_por_id(id_ferramenta) is None:
            print("Item de almoxarifado excluído não encontrado!")
            return

        sql_inserir = """
            INSERT INTO itens_almoxarifado (
                id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                quantidade_atual, estoque_minimo, unidade_medida,
                localizacao_gaveta
            )
            OVERRIDING SYSTEM VALUE
            SELECT id_ferramenta, nome_ferramenta, dimensao_ferramenta,
                   quantidade_atual, estoque_minimo, unidade_medida,
                   localizacao_gaveta
            FROM itens_almoxarifado_deletados
            WHERE id_ferramenta = %s
        """
        sql_remover_historico = """
            DELETE FROM itens_almoxarifado_deletados
            WHERE id_ferramenta = %s
        """
        try:
            self.db.cursor.execute(sql_inserir, (id_ferramenta,))
            self.db.cursor.execute(sql_remover_historico, (id_ferramenta,))
            self.db.commit()
            print("Item de almoxarifado restaurado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar item de almoxarifado: {erro}")

    def fechar(self):
        self.db.fechar()