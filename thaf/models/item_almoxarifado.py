UNIDADES_MEDIDA_PADRAO = ("UN", "PC", "KG", "L", "M", "CX")

# class item_almoxarifado
class ItemAlmoxarifado:
    def __init__(
        self,
        id_ferramenta=None,
        nome_ferramenta="",
        dimensao_ferramenta=None,
        quantidade_atual=0,
        estoque_minimo=1,
        unidade_medida="UN",
        localizacao_gaveta=None,
        deleted_at=None,
    ):
        self.id_ferramenta = id_ferramenta
        self.nome_ferramenta = nome_ferramenta
        self.dimensao_ferramenta = dimensao_ferramenta
        self.quantidade_atual = quantidade_atual
        self.estoque_minimo = estoque_minimo
        self.unidade_medida = unidade_medida
        self.localizacao_gaveta = localizacao_gaveta
        self.deleted_at = deleted_at  # só é preenchido pelo módulo soft_delete/

    def esta_abaixo_do_minimo(self):
        return self.quantidade_atual < self.estoque_minimo

    def __str__(self):
        c1 = "\033[38;5;17m"
        c2 = "\033[38;5;18m"
        c3 = "\033[38;5;19m"
        reset = "\033[0m"
        return (
            f"{c1}=== DADOS ITEM ALMOXARIFADO ==={reset}\n"
            f"{c2}Nome:{reset} {self.nome_ferramenta}\n"
            f"{c3}Dimensão:{reset} {self.dimensao_ferramenta}\n"
            f"{c2}Quantidade atual:{reset} {self.quantidade_atual}\n"
            f"{c3}Estoque mínimo:{reset} {self.estoque_minimo}\n"
            f"{c2}Unidade de medida:{reset} {self.unidade_medida}\n"
            f"{c3}Localização (gaveta):{reset} {self.localizacao_gaveta}\n"
            f"{c1}==============================={reset}"
        )