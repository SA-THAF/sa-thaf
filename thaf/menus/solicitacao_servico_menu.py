from models.solicitacao_servico import (
    SolicitacaoServico,
    PRIORIDADES_VALIDAS,
    TIPOS_MANUTENCAO_VALIDOS,
    STATUS_VALIDOS
)
from repositories.solicitacao_servico_repository import SolicitacaoServicoRepository
from soft_delete.solicitacao_servico_soft_delete import SolicitacaoServicoSoftDelete
from utils.solicitacao_servico_validacoes import (
    validar_descricao_problema,
    validar_prioridade_ss,
    validar_tipo_manutencao_ss,
    validar_status_ss,
    validar_id_referencia
)


class MenuSolicitacaoServico:

    def __init__(self):
        self.repository = SolicitacaoServicoRepository()
        self.soft_delete = SolicitacaoServicoSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - SOLICITAÇÕES DE SERVIÇO")
            print("=" * 60)
            print("1 - Cadastrar Solicitação")
            print("2 - Buscar Solicitação")
            print("3 - Listar Solicitações")
            print("4 - Listar Solicitações por Status")
            print("5 - Atualizar Solicitação")
            print("6 - Excluir Solicitação")
            print("7 - Ver Solicitações Excluídas")
            print("8 - Restaurar Solicitação Excluída")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_solicitacao()

            elif opcao == "2":
                self.buscar_solicitacao()

            elif opcao == "3":
                self.listar_solicitacoes()

            elif opcao == "4":
                self.listar_por_status()

            elif opcao == "5":
                self.atualizar_solicitacao()

            elif opcao == "6":
                self.excluir_solicitacao()

            elif opcao == "7":
                self.listar_solicitacoes_excluidas()

            elif opcao == "8":
                self.restaurar_solicitacao()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_solicitacao(self):
        print()
        print("=" * 60)
        print("CADASTRO DE SOLICITAÇÃO DE SERVIÇO")
        print("=" * 60)

        try:
            maquina_id = validar_id_referencia(input("Código da máquina: "), "máquina")
            solicitante_id = validar_id_referencia(input("Código do solicitante: "), "solicitante")

            responsavel_id = validar_id_referencia(
                input("Código do responsável (ENTER para nenhum): "), "responsável", obrigatorio=False
            )
            professor_validador_id = validar_id_referencia(
                input("Código do professor validador (ENTER para nenhum): "), "professor validador", obrigatorio=False
            )

            descricao_problema = validar_descricao_problema(input("Descrição do problema: "))

            prioridade_ss = validar_prioridade_ss(
                input(f"Prioridade {PRIORIDADES_VALIDAS} [Média]: ")
            )
            tipo_manutencao = validar_tipo_manutencao_ss(
                input(f"Tipo de manutenção {TIPOS_MANUTENCAO_VALIDOS} [Corretiva]: ")
            )
            status = validar_status_ss(
                input(f"Status {STATUS_VALIDOS} [Aberta]: ")
            )

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = SolicitacaoServico(
            maquina_id=maquina_id,
            solicitante_id=solicitante_id,
            responsavel_id=responsavel_id,
            professor_validador_id=professor_validador_id,
            descricao_problema=descricao_problema,
            prioridade_ss=prioridade_ss,
            tipo_manutencao=tipo_manutencao,
            status=status
        )
        self.repository.salvar(solicitacao)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_solicitacao(self):
        print()
        print("=" * 60)
        print("BUSCAR SOLICITAÇÃO DE SERVIÇO")
        print("=" * 60)

        try:
            id_ss = int(input("Código da solicitação: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_ss)
        print()

        if solicitacao is None:
            print("Solicitação não encontrada.")
        else:
            print(solicitacao)

        print()
        input("Pressione ENTER para continuar...")

    def listar_solicitacoes(self):
        print()
        print("=" * 60)
        print("LISTA DE SOLICITAÇÕES DE SERVIÇO")
        print("=" * 60)
        solicitacoes = self.repository.listar()

        if not solicitacoes:
            print()
            print("Nenhuma solicitação cadastrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Máquina':<10}{'Prioridade':<12}{'Status':<20}")
        print("-" * 60)

        for solicitacao in solicitacoes:
            print(f"{solicitacao.id_ss:<5}{solicitacao.maquina_id:<10}{solicitacao.prioridade_ss:<12}{solicitacao.status:<20}")

        print()
        print(f"Total de solicitações: {len(solicitacoes)}")
        print()
        input("Pressione ENTER para continuar...")

    def listar_por_status(self):
        print()
        print("=" * 60)
        print("LISTAR SOLICITAÇÕES POR STATUS")
        print("=" * 60)

        try:
            status = validar_status_ss(input(f"Status {STATUS_VALIDOS}: "))
        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        solicitacoes = self.repository.listar_por_status(status)
        print()

        if not solicitacoes:
            print("Nenhuma solicitação encontrada para esse status.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Máquina':<10}{'Prioridade':<12}{'Status':<20}")
        print("-" * 60)

        for solicitacao in solicitacoes:
            print(f"{solicitacao.id_ss:<5}{solicitacao.maquina_id:<10}{solicitacao.prioridade_ss:<12}{solicitacao.status:<20}")

        print()
        print(f"Total de solicitações: {len(solicitacoes)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_solicitacao(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE SOLICITAÇÃO DE SERVIÇO")
        print("=" * 60)

        try:
            id_ss = int(input("Código da solicitação: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_ss)

        if solicitacao is None:
            print()
            print("Solicitação não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        try:
            maquina_input = input(f"Código da máquina [{solicitacao.maquina_id}]: ")
            if maquina_input:
                solicitacao.maquina_id = validar_id_referencia(maquina_input, "máquina")

            responsavel_input = input(f"Código do responsável [{solicitacao.responsavel_id}]: ")
            if responsavel_input:
                solicitacao.responsavel_id = validar_id_referencia(responsavel_input, "responsável", obrigatorio=False)

            professor_input = input(f"Código do professor validador [{solicitacao.professor_validador_id}]: ")
            if professor_input:
                solicitacao.professor_validador_id = validar_id_referencia(professor_input, "professor validador", obrigatorio=False)

            descricao_input = input(f"Descrição do problema [{solicitacao.descricao_problema}]: ")
            if descricao_input:
                solicitacao.descricao_problema = validar_descricao_problema(descricao_input)

            prioridade_input = input(f"Prioridade [{solicitacao.prioridade_ss}]: ")
            if prioridade_input:
                solicitacao.prioridade_ss = validar_prioridade_ss(prioridade_input)

            tipo_input = input(f"Tipo de manutenção [{solicitacao.tipo_manutencao}]: ")
            if tipo_input:
                solicitacao.tipo_manutencao = validar_tipo_manutencao_ss(tipo_input)

            status_input = input(f"Status [{solicitacao.status}]: ")
            if status_input:
                solicitacao.status = validar_status_ss(status_input)

        except ValueError as erro:
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atualizar(solicitacao)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_solicitacao(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE SOLICITAÇÃO DE SERVIÇO")
        print("=" * 60)

        try:
            id_ss = int(input("Código da solicitação: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.repository.buscar_por_id(id_ss)

        if solicitacao is None:
            print()
            print("Solicitação não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Solicitação localizada")
        print("-" * 60)
        print(f"Código.......: {solicitacao.id_ss}")
        print(f"Descrição....: {solicitacao.descricao_problema}")
        print(f"Status.......: {solicitacao.status}")
        print()

        resposta = input("Deseja realmente excluir esta solicitação? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_ss)
        print()
        input("Pressione ENTER para continuar...")

    def listar_solicitacoes_excluidas(self):
        print()
        print("=" * 60)
        print("SOLICITAÇÕES DE SERVIÇO EXCLUÍDAS")
        print("=" * 60)
        solicitacoes = self.soft_delete.listar_excluidos()

        if not solicitacoes:
            print()
            print("Nenhuma solicitação excluída.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Status':<20}{'Excluído em':<25}")
        print("-" * 60)

        for solicitacao in solicitacoes:
            print(f"{solicitacao.id_ss:<5}{solicitacao.status:<20}{str(solicitacao.deleted_at):<25}")

        print()
        print(f"Total de solicitações excluídas: {len(solicitacoes)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_solicitacao(self):
        print()
        print("=" * 60)
        print("RESTAURAR SOLICITAÇÃO EXCLUÍDA")
        print("=" * 60)

        try:
            id_ss = int(input("Código da solicitação excluída: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao = self.soft_delete.buscar_excluido_por_id(id_ss)

        if solicitacao is None:
            print()
            print("Solicitação excluída não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Solicitação localizada: {solicitacao.descricao_problema}")

        resposta = input("Deseja restaurar esta solicitação? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_ss)
        print()
        input("Pressione ENTER para continuar...")