from models.ordem_servico import OrdemServico
from repositories.ordem_servico_repository import OrdemServicoRepository
from soft_delete.ordem_servico_soft_delete import OrdemServicoSoftDelete
from utils.ordem_servico_validacoes import (
    validar_tipo_manutencao_os,
    validar_criticidade_os,
    validar_data_execucao,
    validar_hora,
    validar_hora_inicio_fim,
    validar_quantidade_pessoas,
    validar_id_relacionado
)


class MenuOrdemServico:

    def __init__(self):
        self.repository = OrdemServicoRepository()
        self.soft_delete = OrdemServicoSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - ORDENS DE SERVIÇO")
            print("=" * 60)
            print("1 - Cadastrar Ordem de Serviço")
            print("2 - Buscar Ordem de Serviço")
            print("3 - Listar Ordens de Serviço")
            print("4 - Listar Ordens de Serviço por Máquina")
            print("5 - Atualizar Ordem de Serviço")
            print("6 - Excluir Ordem de Serviço")
            print("7 - Ver Ordens de Serviço Excluídas")
            print("8 - Restaurar Ordem de Serviço Excluída")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_ordem_servico()

            elif opcao == "2":
                self.buscar_ordem_servico()

            elif opcao == "3":
                self.listar_ordem_servico()

            elif opcao == "4":
                self.listar_ordem_servico_por_maquina()

            elif opcao == "5":
                self.atualizar_ordem_servico()

            elif opcao == "6":
                self.excluir_ordem_servico()

            elif opcao == "7":
                self.listar_ordens_excluidas()

            elif opcao == "8":
                self.restaurar_ordem_servico()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_ordem_servico(self):
        print()
        print("=" * 60)
        print("CADASTRO DE ORDEM DE SERVIÇO")
        print("=" * 60)

        try:
            solicitacao_id = validar_id_relacionado(
                input("Código da solicitação (SS): "), "solicitação"
            )
            maquina_id = validar_id_relacionado(
                input("Código da máquina: "), "máquina"
            )

            turma_texto = input("Código da turma (ENTER para nenhuma): ")
            turma_id = validar_id_relacionado(turma_texto, "turma") if turma_texto else None

            tipo_manutencao = validar_tipo_manutencao_os(
                input("Tipo de manutenção (corretiva/preventiva/preditiva/melhoria): ")
            )
            criticidade_os = validar_criticidade_os(
                input("Criticidade (baixa/média/alta/crítica): ")
            )
            descricao_execucao = input("Descrição da execução: ")

            pecas_texto = input("Peças usadas (ENTER para nenhuma): ")
            pecas_usadas = pecas_texto if pecas_texto else None

            data_execucao = validar_data_execucao(input("Data de execução (DD/MM/AAAA): "))
            hora_inicio = validar_hora(input("Hora de início (HH:MM): "), "hora de início")
            hora_fim = validar_hora(input("Hora de fim (HH:MM): "), "hora de fim")
            validar_hora_inicio_fim(hora_inicio, hora_fim)

            quantidade_pessoas = validar_quantidade_pessoas(
                input("Quantidade de pessoas [1]: ") or "1"
            )

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        ordem_servico = OrdemServico(
            solicitacao_id=solicitacao_id,
            maquina_id=maquina_id,
            turma_id=turma_id,
            tipo_manutencao=tipo_manutencao,
            criticidade_os=criticidade_os,
            descricao_execucao=descricao_execucao,
            pecas_usadas=pecas_usadas,
            data_execucao=data_execucao,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            quantidade_pessoas=quantidade_pessoas
        )
        self.repository.salvar(ordem_servico)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_ordem_servico(self):
        print()
        print("=" * 60)
        print("BUSCAR ORDEM DE SERVIÇO")
        print("=" * 60)

        try:
            id_os = int(input("Código da ordem de serviço: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordem_servico = self.repository.buscar_por_id(id_os)
        print()

        if ordem_servico is None:
            print("Ordem de serviço não encontrada.")

        else:
            print(ordem_servico)

        print()
        input("Pressione ENTER para continuar...")

    def listar_ordem_servico(self):
        print()
        print("=" * 60)
        print("LISTA DE ORDENS DE SERVIÇO")
        print("=" * 60)
        ordens = self.repository.listar()

        if not ordens:
            print()
            print("Nenhuma ordem de serviço cadastrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Máquina':<10}{'Tipo':<14}{'Criticidade':<13}{'Data':<12}")
        print("-" * 60)

        for ordem_servico in ordens:
            print(
                f"{ordem_servico.id_os:<5}"
                f"{ordem_servico.maquina_id:<10}"
                f"{ordem_servico.tipo_manutencao:<14}"
                f"{ordem_servico.criticidade_os:<13}"
                f"{str(ordem_servico.data_execucao):<12}"
            )

        print()
        print(f"Total de ordens de serviço: {len(ordens)}")
        print()
        input("Pressione ENTER para continuar...")

    def listar_ordem_servico_por_maquina(self):
        print()
        print("=" * 60)
        print("ORDENS DE SERVIÇO POR MÁQUINA")
        print("=" * 60)

        try:
            maquina_id = int(input("Código da máquina: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordens = self.repository.listar_por_maquina(maquina_id)

        if not ordens:
            print()
            print("Nenhuma ordem de serviço encontrada para esta máquina.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Tipo':<14}{'Criticidade':<13}{'Data':<12}")
        print("-" * 60)

        for ordem_servico in ordens:
            print(
                f"{ordem_servico.id_os:<5}"
                f"{ordem_servico.tipo_manutencao:<14}"
                f"{ordem_servico.criticidade_os:<13}"
                f"{str(ordem_servico.data_execucao):<12}"
            )

        print()
        print(f"Total de ordens de serviço: {len(ordens)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_ordem_servico(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE ORDEM DE SERVIÇO")
        print("=" * 60)

        try:
            id_os = int(input("Código da ordem de serviço: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordem_servico = self.repository.buscar_por_id(id_os)

        if ordem_servico is None:
            print()
            print("Ordem de serviço não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        try:
            turma_texto = input(f"Turma [{ordem_servico.turma_id}]: ")
            if turma_texto:
                ordem_servico.turma_id = validar_id_relacionado(turma_texto, "turma")

            tipo_texto = input(f"Tipo de manutenção [{ordem_servico.tipo_manutencao}]: ")
            if tipo_texto:
                ordem_servico.tipo_manutencao = validar_tipo_manutencao_os(tipo_texto)

            criticidade_texto = input(f"Criticidade [{ordem_servico.criticidade_os}]: ")
            if criticidade_texto:
                ordem_servico.criticidade_os = validar_criticidade_os(criticidade_texto)

            descricao_texto = input(f"Descrição da execução [{ordem_servico.descricao_execucao}]: ")
            if descricao_texto:
                ordem_servico.descricao_execucao = descricao_texto

            pecas_texto = input(f"Peças usadas [{ordem_servico.pecas_usadas}]: ")
            if pecas_texto:
                ordem_servico.pecas_usadas = pecas_texto

            data_texto = input(f"Data de execução [{ordem_servico.data_execucao}] (DD/MM/AAAA): ")
            if data_texto:
                ordem_servico.data_execucao = validar_data_execucao(data_texto)

            hora_inicio_texto = input(f"Hora de início [{ordem_servico.hora_inicio}]: ")
            if hora_inicio_texto:
                ordem_servico.hora_inicio = validar_hora(hora_inicio_texto, "hora de início")

            hora_fim_texto = input(f"Hora de fim [{ordem_servico.hora_fim}]: ")
            if hora_fim_texto:
                ordem_servico.hora_fim = validar_hora(hora_fim_texto, "hora de fim")

            validar_hora_inicio_fim(ordem_servico.hora_inicio, ordem_servico.hora_fim)

            quantidade_texto = input(f"Quantidade de pessoas [{ordem_servico.quantidade_pessoas}]: ")
            if quantidade_texto:
                ordem_servico.quantidade_pessoas = validar_quantidade_pessoas(quantidade_texto)

        except ValueError as erro:
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atualizar(ordem_servico)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_ordem_servico(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE ORDEM DE SERVIÇO")
        print("=" * 60)

        try:
            id_os = int(input("Código da ordem de serviço: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordem_servico = self.repository.buscar_por_id(id_os)

        if ordem_servico is None:
            print()
            print("Ordem de serviço não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Ordem de serviço localizada")
        print("-" * 60)
        print(f"Código.....: {ordem_servico.id_os}")
        print(f"Máquina....: {ordem_servico.maquina_id}")
        print(f"Data.......: {ordem_servico.data_execucao}")
        print()

        resposta = input("Deseja realmente excluir esta ordem de serviço? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_os)
        print()
        input("Pressione ENTER para continuar...")

    def listar_ordens_excluidas(self):
        print()
        print("=" * 60)
        print("ORDENS DE SERVIÇO EXCLUÍDAS")
        print("=" * 60)
        ordens = self.soft_delete.listar_excluidos()

        if not ordens:
            print()
            print("Nenhuma ordem de serviço excluída.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Máquina':<10}{'Data':<12}{'Excluído em':<25}")
        print("-" * 60)

        for ordem_servico in ordens:
            print(
                f"{ordem_servico.id_os:<5}"
                f"{ordem_servico.maquina_id:<10}"
                f"{str(ordem_servico.data_execucao):<12}"
                f"{str(ordem_servico.deleted_at):<25}"
            )

        print()
        print(f"Total de ordens de serviço excluídas: {len(ordens)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_ordem_servico(self):
        print()
        print("=" * 60)
        print("RESTAURAR ORDEM DE SERVIÇO EXCLUÍDA")
        print("=" * 60)

        try:
            id_os = int(input("Código da ordem de serviço excluída: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        ordem_servico = self.soft_delete.buscar_excluido_por_id(id_os)

        if ordem_servico is None:
            print()
            print("Ordem de serviço excluída não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Ordem de serviço localizada: OS nº {ordem_servico.id_os} (máquina {ordem_servico.maquina_id})")

        resposta = input("Deseja restaurar esta ordem de serviço? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_os)
        print()
        input("Pressione ENTER para continuar...")