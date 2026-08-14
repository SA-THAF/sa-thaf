from models.alerta_estoque import AlertaEstoque
from repositories.alerta_estoque_repository import AlertaEstoqueRepository
from soft_delete.alerta_estoque_soft_delete import AlertaEstoqueSoftDelete
from utils.alerta_estoque_validacoes import (
    validar_item_id,
    validar_mensagem_alerta,
    validar_status_alerta
)


class MenuAlertaEstoque:

    def __init__(self):
        self.repository = AlertaEstoqueRepository()
        self.soft_delete = AlertaEstoqueSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - ALERTAS DE ESTOQUE")
            print("=" * 60)
            print("1 - Cadastrar Alerta")
            print("2 - Buscar Alerta")
            print("3 - Listar Alertas")
            print("4 - Atualizar Alerta")
            print("5 - Excluir Alerta")
            print("6 - Ver Alertas Excluídos")
            print("7 - Restaurar Alerta Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_alerta()

            elif opcao == "2":
                self.buscar_alerta()

            elif opcao == "3":
                self.listar_alerta()

            elif opcao == "4":
                self.atualizar_alerta()

            elif opcao == "5":
                self.excluir_alerta()

            elif opcao == "6":
                self.listar_alertas_excluidos()

            elif opcao == "7":
                self.restaurar_alerta()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_alerta(self):
        print()
        print("=" * 60)
        print("CADASTRO DE ALERTA DE ESTOQUE")
        print("=" * 60)

        try:
            item_id = validar_item_id(input("Código do item: "))
            mensagem_alerta = validar_mensagem_alerta(input("Mensagem: "))
            status_input = input("Status [Pendente/Resolvido] (ENTER = Pendente): ")
            status_alerta = validar_status_alerta(status_input) if status_input else "Pendente"

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        alerta = AlertaEstoque(
            item_id=item_id,
            mensagem_alerta=mensagem_alerta,
            status=status_alerta
        )
        self.repository.salvar(alerta)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_alerta(self):
        print()
        print("=" * 60)
        print("BUSCAR ALERTA DE ESTOQUE")
        print("=" * 60)

        try:
            id_alerta = int(input("Código do alerta: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        alerta = self.repository.buscar_por_id(id_alerta)
        print()

        if alerta is None:
            print("Alerta não encontrado.")

        else:
            print(f"Código......: {alerta.id_alerta}")
            print(f"Item........: {alerta.item_id}")
            print(f"Mensagem....: {alerta.mensagem_alerta}")
            print(f"Status......: {alerta.status}")
            print(f"Criado em...: {alerta.criado_em}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_alerta(self):
        print()
        print("=" * 60)
        print("LISTA DE ALERTAS DE ESTOQUE")
        print("=" * 60)
        alertas = self.repository.listar()

        if not alertas:
            print()
            print("Nenhum alerta cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Item':<8}{'Status':<12}{'Mensagem':<35}")
        print("-" * 60)

        for alerta in alertas:
            print(f"{alerta.id_alerta:<5}{alerta.item_id:<8}{alerta.status:<12}{alerta.mensagem_alerta:<35}")

        print()
        print(f"Total de alertas: {len(alertas)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_alerta(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE ALERTA DE ESTOQUE")
        print("=" * 60)

        try:
            id_alerta = int(input("Código do alerta: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        alerta = self.repository.buscar_por_id(id_alerta)

        if alerta is None:
            print()
            print("Alerta não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        mensagem_alerta = input(f"Mensagem [{alerta.mensagem_alerta}]: ")
        if mensagem_alerta:
            try:
                alerta.mensagem_alerta = validar_mensagem_alerta(mensagem_alerta)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        status_alerta = input(f"Status [{alerta.status}]: ")
        if status_alerta:
            try:
                alerta.status = validar_status_alerta(status_alerta)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        self.repository.atualizar(alerta)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_alerta(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE ALERTA DE ESTOQUE")
        print("=" * 60)

        try:
            id_alerta = int(input("Código do alerta: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        alerta = self.repository.buscar_por_id(id_alerta)

        if alerta is None:
            print()
            print("Alerta não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Alerta localizado")
        print("-" * 60)
        print(f"Código.....: {alerta.id_alerta}")
        print(f"Mensagem...: {alerta.mensagem_alerta}")
        print()

        resposta = input("Deseja realmente excluir este alerta? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_alerta)
        print()
        input("Pressione ENTER para continuar...")

    def listar_alertas_excluidos(self):
        print()
        print("=" * 60)
        print("ALERTAS DE ESTOQUE EXCLUÍDOS")
        print("=" * 60)
        alertas = self.soft_delete.listar_excluidos()

        if not alertas:
            print()
            print("Nenhum alerta excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Item':<8}{'Excluído em':<25}")
        print("-" * 60)

        for alerta in alertas:
            print(f"{alerta.id_alerta:<5}{alerta.item_id:<8}{str(alerta.deleted_at):<25}")

        print()
        print(f"Total de alertas excluídos: {len(alertas)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_alerta(self):
        print()
        print("=" * 60)
        print("RESTAURAR ALERTA DE ESTOQUE EXCLUÍDO")
        print("=" * 60)

        try:
            id_alerta = int(input("Código do alerta excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        alerta = self.soft_delete.buscar_excluido_por_id(id_alerta)

        if alerta is None:
            print()
            print("Alerta excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Alerta localizado: {alerta.mensagem_alerta}")

        resposta = input("Deseja restaurar este alerta? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_alerta)
        print()
        input("Pressione ENTER para continuar...")