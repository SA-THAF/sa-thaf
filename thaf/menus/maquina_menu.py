from models.maquina import Maquina
from repositories.maquina_repository import MaquinaRepository
from soft_delete.maquina_soft_delete import MaquinaSoftDelete
from utils.maquina_validacoes import (
    validar_tag_maquina,
    validar_status_vivo,
    validar_setor_id
)

class MenuMaquina:

    def __init__(self):
        self.repository = MaquinaRepository()
        self.soft_delete = MaquinaSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - MÁQUINAS")
            print("=" * 60)
            print("1 - Cadastrar Máquina")
            print("2 - Buscar Máquina")
            print("3 - Listar Máquinas")
            print("4 - Atualizar Máquina")
            print("5 - Excluir Máquina")
            print("6 - Ver Máquinas Excluídas")
            print("7 - Restaurar Máquina Excluída")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_maquina()

            elif opcao == "2":
                self.buscar_maquina()

            elif opcao == "3":
                self.listar_maquina()

            elif opcao == "4":
                self.atualizar_maquina()

            elif opcao == "5":
                self.excluir_maquina()

            elif opcao == "6":
                self.listar_maquinas_excluidas()

            elif opcao == "7":
                self.restaurar_maquina()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_maquina(self):
        print()
        print("=" * 60)
        print("CADASTRO DE MÁQUINA")
        print("=" * 60)

        try:
            setor_id = validar_setor_id(input("Código do setor: "))
            tag_maquina = validar_tag_maquina(input("Tag: "))
            nome_maquina = input("Nome: ")
            status_vivo = validar_status_vivo(
                input("Status (Operando/Manutenção/Parado/Crítico) [Operando]: ") or "Operando"
            )

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        maquina = Maquina(
            setor_id=setor_id,
            tag_maquina=tag_maquina,
            nome_maquina=nome_maquina,
            status_vivo=status_vivo
        )
        self.repository.salvar(maquina)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_maquina(self):
        print()
        print("=" * 60)
        print("BUSCAR MÁQUINA")
        print("=" * 60)

        try:
            id_maquina = int(input("Código da máquina: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.repository.buscar_por_id(id_maquina)
        print()

        if maquina is None:
            print("Máquina não encontrada.")

        else:
            print(f"Código..............: {maquina.id_maquina}")
            print(f"Setor................: {maquina.setor_id}")
            print(f"Tag..................: {maquina.tag_maquina}")
            print(f"Nome.................: {maquina.nome_maquina}")
            print(f"Status...............: {maquina.status_vivo}")
            print(f"Última manutenção....: {maquina.ultima_manutencao}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_maquina(self):
        print()
        print("=" * 60)
        print("LISTA DE MÁQUINAS")
        print("=" * 60)
        maquinas = self.repository.listar()

        if not maquinas:
            print()
            print("Nenhuma máquina cadastrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Tag':<12}{'Nome':<25}{'Status':<15}")
        print("-" * 60)

        for maquina in maquinas:
            print(f"{maquina.id_maquina:<5}{maquina.tag_maquina:<12}{maquina.nome_maquina:<25}{maquina.status_vivo:<15}")

        print()
        print(f"Total de máquinas: {len(maquinas)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_maquina(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE MÁQUINA")
        print("=" * 60)

        try:
            id_maquina = int(input("Código da máquina: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.repository.buscar_por_id(id_maquina)

        if maquina is None:
            print()
            print("Máquina não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        setor_id = input(f"Código do setor [{maquina.setor_id}]: ")
        if setor_id:
            try:
                maquina.setor_id = validar_setor_id(setor_id)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        tag_maquina = input(f"Tag [{maquina.tag_maquina}]: ")
        if tag_maquina:
            try:
                maquina.tag_maquina = validar_tag_maquina(tag_maquina)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        nome_maquina = input(f"Nome [{maquina.nome_maquina}]: ")
        if nome_maquina:
            maquina.nome_maquina = nome_maquina

        status_vivo = input(f"Status [{maquina.status_vivo}]: ")
        if status_vivo:
            try:
                maquina.status_vivo = validar_status_vivo(status_vivo)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        self.repository.atualizar(maquina)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_maquina(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE MÁQUINA")
        print("=" * 60)

        try:
            id_maquina = int(input("Código da máquina: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.repository.buscar_por_id(id_maquina)

        if maquina is None:
            print()
            print("Máquina não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Máquina localizada")
        print("-" * 60)
        print(f"Código.....: {maquina.id_maquina}")
        print(f"Tag........: {maquina.tag_maquina}")
        print(f"Nome.......: {maquina.nome_maquina}")
        print()

        resposta = input("Deseja realmente excluir esta máquina? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_maquina)
        print()
        input("Pressione ENTER para continuar...")

    def listar_maquinas_excluidas(self):
        print()
        print("=" * 60)
        print("MÁQUINAS EXCLUÍDAS")
        print("=" * 60)
        maquinas = self.soft_delete.listar_excluidos()

        if not maquinas:
            print()
            print("Nenhuma máquina excluída.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Tag':<12}{'Nome':<25}{'Excluída em':<25}")
        print("-" * 60)

        for maquina in maquinas:
            print(f"{maquina.id_maquina:<5}{maquina.tag_maquina:<12}{maquina.nome_maquina:<25}{str(maquina.deleted_at):<25}")

        print()
        print(f"Total de máquinas excluídas: {len(maquinas)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_maquina(self):
        print()
        print("=" * 60)
        print("RESTAURAR MÁQUINA EXCLUÍDA")
        print("=" * 60)

        try:
            id_maquina = int(input("Código da máquina excluída: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        maquina = self.soft_delete.buscar_excluido_por_id(id_maquina)

        if maquina is None:
            print()
            print("Máquina excluída não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Máquina localizada: {maquina.tag_maquina} - {maquina.nome_maquina}")

        resposta = input("Deseja restaurar esta máquina? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_maquina)
        print()
        input("Pressione ENTER para continuar...")