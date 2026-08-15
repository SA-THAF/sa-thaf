from models.setor import Setor
from repositories.setor_repository import SetorRepository
from soft_delete.setor_soft_delete import SetorSoftDelete
from utils.setor__validacoes import validar_nome_setor


class MenuSetor:

    def __init__(self):
        self.repository = SetorRepository()
        self.soft_delete = SetorSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - SETORES")
            print("=" * 60)
            print("1 - Cadastrar Setor")
            print("2 - Buscar Setor")
            print("3 - Listar Setores")
            print("4 - Atualizar Setor")
            print("5 - Excluir Setor")
            print("6 - Ver Setores Excluídos")
            print("7 - Restaurar Setor Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_setor()

            elif opcao == "2":
                self.buscar_setor()

            elif opcao == "3":
                self.listar_setor()

            elif opcao == "4":
                self.atualizar_setor()

            elif opcao == "5":
                self.excluir_setor()

            elif opcao == "6":
                self.listar_setores_excluidos()

            elif opcao == "7":
                self.restaurar_setor()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_setor(self):
        print()
        print("=" * 60)
        print("CADASTRO DE SETOR")
        print("=" * 60)

        try:
            nome_setor = validar_nome_setor(
                input("Nome do setor: ")
            )
            descricao_setor = input("Descrição: ")

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        setor = Setor(
            nome_setor=nome_setor,
            descricao_setor=descricao_setor
        )
        self.repository.salvar(setor)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_setor(self):
        print()
        print("=" * 60)
        print("BUSCAR SETOR")
        print("=" * 60)

        try:
            id_setor = int(input("Código do setor: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.repository.buscar_por_id(id_setor)
        print()

        if setor is None:
            print("Setor não encontrado.")

        else:
            print(f"Código......: {setor.id_setor}")
            print(f"Nome........: {setor.nome_setor}")
            print(f"Descrição...: {setor.descricao_setor}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_setor(self):
        print()
        print("=" * 60)
        print("LISTA DE SETORES")
        print("=" * 60)
        setores = self.repository.listar()

        if not setores:
            print()
            print("Nenhum setor cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<20}{'Descrição':<35}")
        print("-" * 60)

        for setor in setores:
            print(f"{setor.id_setor:<5}{setor.nome_setor:<20}{(setor.descricao_setor or ''):<35}")

        print()
        print(f"Total de setores: {len(setores)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_setor(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE SETOR")
        print("=" * 60)

        try:
            id_setor = int(input("Código do setor: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.repository.buscar_por_id(id_setor)

        if setor is None:
            print()
            print("Setor não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        nome_setor = input(f"Nome [{setor.nome_setor}]: ")
        if nome_setor:
            try:
                setor.nome_setor = validar_nome_setor(nome_setor)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        descricao_setor = input(f"Descrição [{setor.descricao_setor}]: ")
        if descricao_setor:
            setor.descricao_setor = descricao_setor

        self.repository.atualizar(setor)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_setor(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE SETOR")
        print("=" * 60)

        try:
            id_setor = int(input("Código do setor: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.repository.buscar_por_id(id_setor)

        if setor is None:
            print()
            print("Setor não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Setor localizado")
        print("-" * 60)
        print(f"Código.....: {setor.id_setor}")
        print(f"Nome.......: {setor.nome_setor}")
        print()

        resposta = input("Deseja realmente excluir este setor? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_setor)
        print()
        input("Pressione ENTER para continuar...")

    def listar_setores_excluidos(self):
        print()
        print("=" * 60)
        print("SETORES EXCLUÍDOS")
        print("=" * 60)
        setores = self.soft_delete.listar_excluidos()

        if not setores:
            print()
            print("Nenhum setor excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<20}{'Excluído em':<25}")
        print("-" * 60)

        for setor in setores:
            print(f"{setor.id_setor:<5}{setor.nome_setor:<20}{str(setor.deleted_at):<25}")

        print()
        print(f"Total de setores excluídos: {len(setores)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_setor(self):
        print()
        print("=" * 60)
        print("RESTAURAR SETOR EXCLUÍDO")
        print("=" * 60)

        try:
            id_setor = int(input("Código do setor excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        setor = self.soft_delete.buscar_excluido_por_id(id_setor)

        if setor is None:
            print()
            print("Setor excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Setor localizado: {setor.nome_setor}")

        resposta = input("Deseja restaurar este setor? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_setor)
        print()
        input("Pressione ENTER para continuar...")