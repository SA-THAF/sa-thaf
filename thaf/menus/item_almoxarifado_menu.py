from models.item_almoxarifado import ItemAlmoxarifado
from repositories.item_almoxarifado_repository import ItemAlmoxarifadoRepository
from soft_delete.item_almoxarifado_soft_delete import ItemAlmoxarifadoSoftDelete
from utils.item_almoxarifado_validacoes import (
    validar_nome_ferramenta,
    validar_dimensao_ferramenta,
    validar_quantidade_atual,
    validar_estoque_minimo,
    validar_unidade_medida,
    validar_localizacao_gaveta
)


class MenuItemAlmoxarifado:

    def __init__(self):
        self.repository = ItemAlmoxarifadoRepository()
        self.soft_delete = ItemAlmoxarifadoSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - ALMOXARIFADO")
            print("=" * 60)
            print("1 - Cadastrar Item")
            print("2 - Buscar Item")
            print("3 - Listar Itens")
            print("4 - Atualizar Item")
            print("5 - Excluir Item")
            print("6 - Ver Itens Excluídos")
            print("7 - Restaurar Item Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_item()

            elif opcao == "2":
                self.buscar_item()

            elif opcao == "3":
                self.listar_item()

            elif opcao == "4":
                self.atualizar_item()

            elif opcao == "5":
                self.excluir_item()

            elif opcao == "6":
                self.listar_itens_excluidos()

            elif opcao == "7":
                self.restaurar_item()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_item(self):
        print()
        print("=" * 60)
        print("CADASTRO DE ITEM DE ALMOXARIFADO")
        print("=" * 60)

        try:
            nome_ferramenta = validar_nome_ferramenta(
                input("Nome da ferramenta: ")
            )
            dimensao_ferramenta = validar_dimensao_ferramenta(
                input("Dimensão (opcional): ")
            )
            quantidade_atual = validar_quantidade_atual(
                input("Quantidade atual: ")
            )
            estoque_minimo = validar_estoque_minimo(
                input("Estoque mínimo: ")
            )
            unidade_medida = validar_unidade_medida(
                input("Unidade de medida (UN/PC/KG/L/M/CX): ")
            )
            localizacao_gaveta = validar_localizacao_gaveta(
                input("Localização (gaveta, opcional): ")
            )

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        item = ItemAlmoxarifado(
            nome_ferramenta=nome_ferramenta,
            dimensao_ferramenta=dimensao_ferramenta,
            quantidade_atual=quantidade_atual,
            estoque_minimo=estoque_minimo,
            unidade_medida=unidade_medida,
            localizacao_gaveta=localizacao_gaveta
        )
        self.repository.salvar(item)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_item(self):
        print()
        print("=" * 60)
        print("BUSCAR ITEM DE ALMOXARIFADO")
        print("=" * 60)

        try:
            id_ferramenta = int(input("Código do item: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.buscar_por_id(id_ferramenta)
        print()

        if item is None:
            print("Item não encontrado.")

        else:
            print(f"Código..............: {item.id_ferramenta}")
            print(f"Nome................: {item.nome_ferramenta}")
            print(f"Dimensão............: {item.dimensao_ferramenta}")
            print(f"Quantidade atual....: {item.quantidade_atual}")
            print(f"Estoque mínimo......: {item.estoque_minimo}")
            print(f"Unidade de medida...: {item.unidade_medida}")
            print(f"Localização.........: {item.localizacao_gaveta}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_item(self):
        print()
        print("=" * 60)
        print("LISTA DE ITENS DE ALMOXARIFADO")
        print("=" * 60)
        itens = self.repository.listar()

        if not itens:
            print()
            print("Nenhum item cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<25}{'Qtd':<8}{'Mín':<8}{'Un':<6}{'Gaveta':<15}")
        print("-" * 70)

        for item in itens:
            print(
                f"{item.id_ferramenta:<5}"
                f"{item.nome_ferramenta:<25}"
                f"{item.quantidade_atual:<8}"
                f"{item.estoque_minimo:<8}"
                f"{item.unidade_medida:<6}"
                f"{(item.localizacao_gaveta or ''):<15}"
            )

        print()
        print(f"Total de itens: {len(itens)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_item(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE ITEM DE ALMOXARIFADO")
        print("=" * 60)

        try:
            id_ferramenta = int(input("Código do item: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.buscar_por_id(id_ferramenta)

        if item is None:
            print()
            print("Item não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        nome_ferramenta = input(f"Nome [{item.nome_ferramenta}]: ")
        if nome_ferramenta:
            try:
                item.nome_ferramenta = validar_nome_ferramenta(nome_ferramenta)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        dimensao_ferramenta = input(f"Dimensão [{item.dimensao_ferramenta}]: ")
        if dimensao_ferramenta:
            try:
                item.dimensao_ferramenta = validar_dimensao_ferramenta(dimensao_ferramenta)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        quantidade_atual = input(f"Quantidade atual [{item.quantidade_atual}]: ")
        if quantidade_atual:
            try:
                item.quantidade_atual = validar_quantidade_atual(quantidade_atual)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        estoque_minimo = input(f"Estoque mínimo [{item.estoque_minimo}]: ")
        if estoque_minimo:
            try:
                item.estoque_minimo = validar_estoque_minimo(estoque_minimo)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        unidade_medida = input(f"Unidade de medida [{item.unidade_medida}]: ")
        if unidade_medida:
            try:
                item.unidade_medida = validar_unidade_medida(unidade_medida)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        localizacao_gaveta = input(f"Localização [{item.localizacao_gaveta}]: ")
        if localizacao_gaveta:
            try:
                item.localizacao_gaveta = validar_localizacao_gaveta(localizacao_gaveta)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        self.repository.atualizar(item)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_item(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE ITEM DE ALMOXARIFADO")
        print("=" * 60)

        try:
            id_ferramenta = int(input("Código do item: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.repository.buscar_por_id(id_ferramenta)

        if item is None:
            print()
            print("Item não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Item localizado")
        print("-" * 60)
        print(f"Código.....: {item.id_ferramenta}")
        print(f"Nome.......: {item.nome_ferramenta}")
        print()

        resposta = input("Deseja realmente excluir este item? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_ferramenta)
        print()
        input("Pressione ENTER para continuar...")

    def listar_itens_excluidos(self):
        print()
        print("=" * 60)
        print("ITENS DE ALMOXARIFADO EXCLUÍDOS")
        print("=" * 60)
        itens = self.soft_delete.listar_excluidos()

        if not itens:
            print()
            print("Nenhum item excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<25}{'Excluído em':<25}")
        print("-" * 60)

        for item in itens:
            print(f"{item.id_ferramenta:<5}{item.nome_ferramenta:<25}{str(item.deleted_at):<25}")

        print()
        print(f"Total de itens excluídos: {len(itens)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_item(self):
        print()
        print("=" * 60)
        print("RESTAURAR ITEM EXCLUÍDO")
        print("=" * 60)

        try:
            id_ferramenta = int(input("Código do item excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        item = self.soft_delete.buscar_excluido_por_id(id_ferramenta)

        if item is None:
            print()
            print("Item excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Item localizado: {item.nome_ferramenta}")

        resposta = input("Deseja restaurar este item? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_ferramenta)
        print()
        input("Pressione ENTER para continuar...")