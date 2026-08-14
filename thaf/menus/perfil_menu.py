from models.perfil import Perfil
from repositories.perfil_repository import PerfilRepository
from soft_delete.perfil_soft_delete import PerfilSoftDelete
from utils.perfil_validacoes import validar_nome_perfil


class MenuPerfil:

    def __init__(self):
        self.repository = PerfilRepository()
        self.soft_delete = PerfilSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - PERFIS DE ACESSO")
            print("=" * 60)
            print("1 - Cadastrar Perfil")
            print("2 - Buscar Perfil")
            print("3 - Listar Perfis")
            print("4 - Atualizar Perfil")
            print("5 - Excluir Perfil")
            print("6 - Ver Perfis Excluídos")
            print("7 - Restaurar Perfil Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_perfil()

            elif opcao == "2":
                self.buscar_perfil()

            elif opcao == "3":
                self.listar_perfil()

            elif opcao == "4":
                self.atualizar_perfil()

            elif opcao == "5":
                self.excluir_perfil()

            elif opcao == "6":
                self.listar_perfis_excluidos()

            elif opcao == "7":
                self.restaurar_perfil()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_perfil(self):
        print()
        print("=" * 60)
        print("CADASTRO DE PERFIL")
        print("=" * 60)

        try:
            nome_perfil = validar_nome_perfil(
                input("Nome (coordenador/gestor/professor/aluno): ")
            )
            descricao_perfil = input("Descrição: ")

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        perfil = Perfil(
            nome_perfil=nome_perfil,
            descricao_perfil=descricao_perfil
        )
        self.repository.salvar(perfil)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_perfil(self):
        print()
        print("=" * 60)
        print("BUSCAR PERFIL")
        print("=" * 60)

        try:
            id_perfil = int(input("Código do perfil: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)
        print()

        if perfil is None:
            print("Perfil não encontrado.")

        else:
            print(f"Código......: {perfil.id_perfil}")
            print(f"Nome........: {perfil.nome_perfil}")
            print(f"Descrição...: {perfil.descricao_perfil}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_perfil(self):
        print()
        print("=" * 60)
        print("LISTA DE PERFIS")
        print("=" * 60)
        perfis = self.repository.listar()

        if not perfis:
            print()
            print("Nenhum perfil cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<20}{'Descrição':<35}")
        print("-" * 60)

        for perfil in perfis:
            print(f"{perfil.id_perfil:<5}{perfil.nome_perfil:<20}{(perfil.descricao_perfil or ''):<35}")

        print()
        print(f"Total de perfis: {len(perfis)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_perfil(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE PERFIL")
        print("=" * 60)

        try:
            id_perfil = int(input("Código do perfil: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        nome_perfil = input(f"Nome [{perfil.nome_perfil}]: ")
        if nome_perfil:
            try:
                perfil.nome_perfil = validar_nome_perfil(nome_perfil)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        descricao_perfil = input(f"Descrição [{perfil.descricao_perfil}]: ")
        if descricao_perfil:
            perfil.descricao_perfil = descricao_perfil

        self.repository.atualizar(perfil)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_perfil(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE PERFIL")
        print("=" * 60)

        try:
            id_perfil = int(input("Código do perfil: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.repository.buscar_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Perfil localizado")
        print("-" * 60)
        print(f"Código.....: {perfil.id_perfil}")
        print(f"Nome.......: {perfil.nome_perfil}")
        print()

        resposta = input("Deseja realmente excluir este perfil? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_perfil)
        print()
        input("Pressione ENTER para continuar...")

    def listar_perfis_excluidos(self):
        print()
        print("=" * 60)
        print("PERFIS EXCLUÍDOS")
        print("=" * 60)
        perfis = self.soft_delete.listar_excluidos()

        if not perfis:
            print()
            print("Nenhum perfil excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<20}{'Excluído em':<25}")
        print("-" * 60)

        for perfil in perfis:
            print(f"{perfil.id_perfil:<5}{perfil.nome_perfil:<20}{str(perfil.deleted_at):<25}")

        print()
        print(f"Total de perfis excluídos: {len(perfis)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_perfil(self):
        print()
        print("=" * 60)
        print("RESTAURAR PERFIL EXCLUÍDO")
        print("=" * 60)

        try:
            id_perfil = int(input("Código do perfil excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        perfil = self.soft_delete.buscar_excluido_por_id(id_perfil)

        if perfil is None:
            print()
            print("Perfil excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Perfil localizado: {perfil.nome_perfil}")

        resposta = input("Deseja restaurar este perfil? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_perfil)
        print()
        input("Pressione ENTER para continuar...")