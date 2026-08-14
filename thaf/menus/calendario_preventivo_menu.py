# menus/calendario_preventivo_menu.py

from models.calendario_preventivo import CalendarioPreventivo
from repositories.calendario_preventivo_repository import CalendarioPreventivoRepository
from soft_delete.calendario_preventivo_soft_delete import CalendarioPreventivoSoftDelete
from utils.calendario_preventivo_validacoes import (
    validar_titulo_calendario,
    validar_frequencia_calendario,
    validar_status_calendario,
    validar_data_proxima_execucao,
    validar_id_referencia
)


class MenuCalendarioPreventivo:

    def __init__(self):
        self.repository = CalendarioPreventivoRepository()
        self.soft_delete = CalendarioPreventivoSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - CALENDÁRIO PREVENTIVO")
            print("=" * 60)
            print("1 - Cadastrar Calendário")
            print("2 - Buscar Calendário")
            print("3 - Listar Calendários")
            print("4 - Atualizar Calendário")
            print("5 - Excluir Calendário")
            print("6 - Ver Calendários Excluídos")
            print("7 - Restaurar Calendário Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_calendario()

            elif opcao == "2":
                self.buscar_calendario()

            elif opcao == "3":
                self.listar_calendario()

            elif opcao == "4":
                self.atualizar_calendario()

            elif opcao == "5":
                self.excluir_calendario()

            elif opcao == "6":
                self.listar_calendarios_excluidos()

            elif opcao == "7":
                self.restaurar_calendario()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_calendario(self):
        print()
        print("=" * 60)
        print("CADASTRO DE CALENDÁRIO PREVENTIVO")
        print("=" * 60)

        try:
            maquina_id = validar_id_referencia(
                input("Código da máquina: "), "Código da máquina", obrigatorio=True
            )
            turma_id = validar_id_referencia(
                input("Código da turma (opcional): "), "Código da turma", obrigatorio=False
            )
            responsavel_id = validar_id_referencia(
                input("Código do responsável (opcional): "), "Código do responsável", obrigatorio=False
            )
            titulo_calendario = validar_titulo_calendario(input("Título: "))
            descricao_calendario = input("Descrição (opcional): ")
            frequencia_calendario = validar_frequencia_calendario(
                input("Frequência (Diária/Semanal/Quinzenal/Mensal/Semestral/Anual): ")
            )
            data_proxima_execucao = validar_data_proxima_execucao(
                input("Data da próxima execução (DD/MM/AAAA): ")
            )

            status_texto = input("Status (ENTER para 'Agendada'): ")
            status = validar_status_calendario(status_texto) if status_texto else "Agendada"

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        calendario = CalendarioPreventivo(
            maquina_id=maquina_id,
            turma_id=turma_id,
            responsavel_id=responsavel_id,
            titulo_calendario=titulo_calendario,
            descricao_calendario=descricao_calendario,
            frequencia_calendario=frequencia_calendario,
            data_proxima_execucao=data_proxima_execucao,
            status=status
        )
        self.repository.salvar(calendario)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_calendario(self):
        print()
        print("=" * 60)
        print("BUSCAR CALENDÁRIO PREVENTIVO")
        print("=" * 60)

        try:
            id_calendario = int(input("Código do calendário: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        calendario = self.repository.buscar_por_id(id_calendario)
        print()

        if calendario is None:
            print("Calendário preventivo não encontrado.")

        else:
            print(f"Código..............: {calendario.id_calendario}")
            print(f"Máquina.............: {calendario.maquina_id}")
            print(f"Turma...............: {calendario.turma_id}")
            print(f"Responsável.........: {calendario.responsavel_id}")
            print(f"Título..............: {calendario.titulo_calendario}")
            print(f"Descrição...........: {calendario.descricao_calendario}")
            print(f"Frequência..........: {calendario.frequencia_calendario}")
            print(f"Próxima execução....: {calendario.data_proxima_execucao}")
            print(f"Status..............: {calendario.status}")
            print(f"Criado em...........: {calendario.criado_em}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_calendario(self):
        print()
        print("=" * 60)
        print("LISTA DE CALENDÁRIOS PREVENTIVOS")
        print("=" * 60)
        calendarios = self.repository.listar()

        if not calendarios:
            print()
            print("Nenhum calendário cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Título':<25}{'Frequência':<12}{'Próx. Exec.':<14}{'Status':<15}")
        print("-" * 71)

        for calendario in calendarios:
            print(
                f"{calendario.id_calendario:<5}"
                f"{calendario.titulo_calendario:<25}"
                f"{calendario.frequencia_calendario:<12}"
                f"{str(calendario.data_proxima_execucao):<14}"
                f"{calendario.status:<15}"
            )

        print()
        print(f"Total de calendários: {len(calendarios)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_calendario(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE CALENDÁRIO PREVENTIVO")
        print("=" * 60)

        try:
            id_calendario = int(input("Código do calendário: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        calendario = self.repository.buscar_por_id(id_calendario)

        if calendario is None:
            print()
            print("Calendário preventivo não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        try:
            maquina_id = input(f"Máquina [{calendario.maquina_id}]: ")
            if maquina_id:
                calendario.maquina_id = validar_id_referencia(maquina_id, "Código da máquina")

            turma_id = input(f"Turma [{calendario.turma_id}]: ")
            if turma_id:
                calendario.turma_id = validar_id_referencia(turma_id, "Código da turma", obrigatorio=False)

            responsavel_id = input(f"Responsável [{calendario.responsavel_id}]: ")
            if responsavel_id:
                calendario.responsavel_id = validar_id_referencia(
                    responsavel_id, "Código do responsável", obrigatorio=False
                )

            titulo_calendario = input(f"Título [{calendario.titulo_calendario}]: ")
            if titulo_calendario:
                calendario.titulo_calendario = validar_titulo_calendario(titulo_calendario)

            descricao_calendario = input(f"Descrição [{calendario.descricao_calendario}]: ")
            if descricao_calendario:
                calendario.descricao_calendario = descricao_calendario

            frequencia_calendario = input(f"Frequência [{calendario.frequencia_calendario}]: ")
            if frequencia_calendario:
                calendario.frequencia_calendario = validar_frequencia_calendario(frequencia_calendario)

            data_proxima_execucao = input(f"Próxima execução [{calendario.data_proxima_execucao}] (DD/MM/AAAA): ")
            if data_proxima_execucao:
                calendario.data_proxima_execucao = validar_data_proxima_execucao(data_proxima_execucao)

            status = input(f"Status [{calendario.status}]: ")
            if status:
                calendario.status = validar_status_calendario(status)

        except ValueError as erro:
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atualizar(calendario)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_calendario(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE CALENDÁRIO PREVENTIVO")
        print("=" * 60)

        try:
            id_calendario = int(input("Código do calendário: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        calendario = self.repository.buscar_por_id(id_calendario)

        if calendario is None:
            print()
            print("Calendário preventivo não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Calendário localizado")
        print("-" * 60)
        print(f"Código.....: {calendario.id_calendario}")
        print(f"Título.....: {calendario.titulo_calendario}")
        print()

        resposta = input("Deseja realmente excluir este calendário? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_calendario)
        print()
        input("Pressione ENTER para continuar...")

    def listar_calendarios_excluidos(self):
        print()
        print("=" * 60)
        print("CALENDÁRIOS PREVENTIVOS EXCLUÍDOS")
        print("=" * 60)
        calendarios = self.soft_delete.listar_excluidos()

        if not calendarios:
            print()
            print("Nenhum calendário excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Título':<25}{'Excluído em':<25}")
        print("-" * 60)

        for calendario in calendarios:
            print(f"{calendario.id_calendario:<5}{calendario.titulo_calendario:<25}{str(calendario.deleted_at):<25}")

        print()
        print(f"Total de calendários excluídos: {len(calendarios)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_calendario(self):
        print()
        print("=" * 60)
        print("RESTAURAR CALENDÁRIO PREVENTIVO EXCLUÍDO")
        print("=" * 60)

        try:
            id_calendario = int(input("Código do calendário excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        calendario = self.soft_delete.buscar_excluido_por_id(id_calendario)

        if calendario is None:
            print()
            print("Calendário excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Calendário localizado: {calendario.titulo_calendario}")

        resposta = input("Deseja restaurar este calendário? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_calendario)
        print()
        input("Pressione ENTER para continuar...")