from models.turma import Turma
from repositories.turma_repository import TurmaRepository
from soft_delete.turma_soft_delete import TurmaSoftDelete
from utils.turma_validacoes import validar_codigo_turma, validar_periodo_turma


class MenuTurma:

    def __init__(self):
        self.repository = TurmaRepository()
        self.soft_delete = TurmaSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - TURMAS")
            print("=" * 60)
            print("1 - Cadastrar Turma")
            print("2 - Buscar Turma")
            print("3 - Listar Turmas")
            print("4 - Atualizar Turma")
            print("5 - Excluir Turma")
            print("6 - Ver Turmas Excluídas")
            print("7 - Restaurar Turma Excluída")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_turma()

            elif opcao == "2":
                self.buscar_turma()

            elif opcao == "3":
                self.listar_turma()

            elif opcao == "4":
                self.atualizar_turma()

            elif opcao == "5":
                self.excluir_turma()

            elif opcao == "6":
                self.listar_turmas_excluidas()

            elif opcao == "7":
                self.restaurar_turma()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_turma(self):
        print()
        print("=" * 60)
        print("CADASTRO DE TURMA")
        print("=" * 60)

        try:
            codigo_turma = validar_codigo_turma(
                input("Código (ex: MAN-2026-2T): ")
            )
            periodo_turma = validar_periodo_turma(
                input("Período (Primeiro Turno/Segundo Turno): ")
            )

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        turma = Turma(
            codigo_turma=codigo_turma,
            periodo_turma=periodo_turma
        )
        self.repository.salvar(turma)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_turma(self):
        print()
        print("=" * 60)
        print("BUSCAR TURMA")
        print("=" * 60)

        try:
            id_turma = int(input("Código do registro da turma: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.repository.buscar_por_id(id_turma)
        print()

        if turma is None:
            print("Turma não encontrada.")

        else:
            print(f"Código......: {turma.id_turma}")
            print(f"Turma.......: {turma.codigo_turma}")
            print(f"Período.....: {turma.periodo_turma}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_turma(self):
        print()
        print("=" * 60)
        print("LISTA DE TURMAS")
        print("=" * 60)
        turmas = self.repository.listar()

        if not turmas:
            print()
            print("Nenhuma turma cadastrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Código':<20}{'Período':<35}")
        print("-" * 60)

        for turma in turmas:
            print(f"{turma.id_turma:<5}{turma.codigo_turma:<20}{(turma.periodo_turma or ''):<35}")

        print()
        print(f"Total de turmas: {len(turmas)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_turma(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE TURMA")
        print("=" * 60)

        try:
            id_turma = int(input("Código do registro da turma: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.repository.buscar_por_id(id_turma)

        if turma is None:
            print()
            print("Turma não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        codigo_turma = input(f"Código [{turma.codigo_turma}]: ")
        if codigo_turma:
            try:
                turma.codigo_turma = validar_codigo_turma(codigo_turma)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        periodo_turma = input(f"Período (Primeiro Turno/Segundo Turno) [{turma.periodo_turma}]: ")
        if periodo_turma:
            try:
                turma.periodo_turma = validar_periodo_turma(periodo_turma)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        self.repository.atualizar(turma)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_turma(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE TURMA")
        print("=" * 60)

        try:
            id_turma = int(input("Código do registro da turma: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.repository.buscar_por_id(id_turma)

        if turma is None:
            print()
            print("Turma não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Turma localizada")
        print("-" * 60)
        print(f"Código.....: {turma.id_turma}")
        print(f"Turma......: {turma.codigo_turma}")
        print()

        resposta = input("Deseja realmente excluir esta turma? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_turma)
        print()
        input("Pressione ENTER para continuar...")

    def listar_turmas_excluidas(self):
        print()
        print("=" * 60)
        print("TURMAS EXCLUÍDAS")
        print("=" * 60)
        turmas = self.soft_delete.listar_excluidos()

        if not turmas:
            print()
            print("Nenhuma turma excluída.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Código':<20}{'Excluído em':<25}")
        print("-" * 60)

        for turma in turmas:
            print(f"{turma.id_turma:<5}{turma.codigo_turma:<20}{str(turma.deleted_at):<25}")

        print()
        print(f"Total de turmas excluídas: {len(turmas)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_turma(self):
        print()
        print("=" * 60)
        print("RESTAURAR TURMA EXCLUÍDA")
        print("=" * 60)

        try:
            id_turma = int(input("Código da turma excluída: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        turma = self.soft_delete.buscar_excluido_por_id(id_turma)

        if turma is None:
            print()
            print("Turma excluída não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Turma localizada: {turma.codigo_turma}")

        resposta = input("Deseja restaurar esta turma? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_turma)
        print()
        input("Pressione ENTER para continuar...")