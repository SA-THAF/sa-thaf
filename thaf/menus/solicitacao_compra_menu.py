from models.solicitacao_compra import SolicitacaoCompra, STATUS_COMPRA_VALIDOS
from repositories.solicitacao_compra_repository import SolicitacaoCompraRepository
from soft_delete.solicitacao_compra_soft_delete import SolicitacaoCompraSoftDelete
from utils.solicitacao_compra_validacoes import (
    validar_status_compra,
    validar_especificacao_tecnica,
    validar_justificativa_solicitacao,
    validar_quantidade_solicitacao,
    validar_sap_solicitacao,
    validar_patrimonio,
    validar_equipamento,
    validar_conjunto_mecanico,
    validar_arquivos,
)


class MenuSolicitacaoCompra:

    def __init__(self):
        self.repository = SolicitacaoCompraRepository()
        self.soft_delete = SolicitacaoCompraSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - SOLICITAÇÕES DE COMPRA")
            print("=" * 60)
            print("1 - Cadastrar Solicitação de Compra")
            print("2 - Buscar Solicitação de Compra")
            print("3 - Listar Solicitações de Compra")
            print("4 - Atualizar Solicitação de Compra")
            print("5 - Excluir Solicitação de Compra")
            print("6 - Ver Solicitações Excluídas")
            print("7 - Restaurar Solicitação Excluída")
            print("8 - Remover Definitivamente do Histórico")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_solicitacao_compra()

            elif opcao == "2":
                self.buscar_solicitacao_compra()

            elif opcao == "3":
                self.listar_solicitacao_compra()

            elif opcao == "4":
                self.atualizar_solicitacao_compra()

            elif opcao == "5":
                self.excluir_solicitacao_compra()

            elif opcao == "6":
                self.listar_solicitacoes_excluidas()

            elif opcao == "7":
                self.restaurar_solicitacao_compra()

            elif opcao == "8":
                self.excluir_definitivamente()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_solicitacao_compra(self):
        print()
        print("=" * 60)
        print("CADASTRO DE SOLICITAÇÃO DE COMPRA")
        print("=" * 60)

        try:
            solicitante_id = int(input("Código do solicitante (usuário): "))
            professor_responsavel_id = int(input("Código do professor responsável (usuário): "))

            turma_id_input = input("Código da turma (opcional, ENTER para pular): ")
            turma_id = int(turma_id_input) if turma_id_input else None

            maquina_id_input = input("Código da máquina (opcional, ENTER para pular): ")
            maquina_id = int(maquina_id_input) if maquina_id_input else None

            especificacao_tecnica = validar_especificacao_tecnica(
                input("Especificação técnica: ")
            )
            quantidade_solicitacao = validar_quantidade_solicitacao(
                input("Quantidade: ")
            )
            sap_solicitacao = validar_sap_solicitacao(
                input("SAP (opcional): ") or None
            )
            justificativa_solicitacao = validar_justificativa_solicitacao(
                input("Justificativa: ")
            )
            patrimonio = validar_patrimonio(input("Patrimônio (opcional): ") or None)
            equipamento = validar_equipamento(input("Equipamento (opcional): ") or None)
            conjunto_mecanico = validar_conjunto_mecanico(
                input("Conjunto mecânico (opcional): ") or None
            )
            arquivos = validar_arquivos(input("Arquivo(s) (opcional): ") or None)

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao_compra = SolicitacaoCompra(
            solicitante_id=solicitante_id,
            professor_responsavel_id=professor_responsavel_id,
            turma_id=turma_id,
            maquina_id=maquina_id,
            especificacao_tecnica=especificacao_tecnica,
            quantidade_solicitacao=quantidade_solicitacao,
            sap_solicitacao=sap_solicitacao,
            justificativa_solicitacao=justificativa_solicitacao,
            patrimonio=patrimonio,
            equipamento=equipamento,
            conjunto_mecanico=conjunto_mecanico,
            arquivos=arquivos
        )
        self.repository.salvar(solicitacao_compra)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_solicitacao_compra(self):
        print()
        print("=" * 60)
        print("BUSCAR SOLICITAÇÃO DE COMPRA")
        print("=" * 60)

        try:
            id_solicitacao = int(input("Código da solicitação: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao_compra = self.repository.buscar_por_id(id_solicitacao)
        print()

        if solicitacao_compra is None:
            print("Solicitação de compra não encontrada.")

        else:
            print(solicitacao_compra)

        print()
        input("Pressione ENTER para continuar...")

    def listar_solicitacao_compra(self):
        print()
        print("=" * 60)
        print("LISTA DE SOLICITAÇÕES DE COMPRA")
        print("=" * 60)
        solicitacoes = self.repository.listar()

        if not solicitacoes:
            print()
            print("Nenhuma solicitação de compra cadastrada.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Status':<22}{'Qtd':<6}{'Especificação':<30}")
        print("-" * 60)

        for solicitacao in solicitacoes:
            print(
                f"{solicitacao.id_solicitacao:<5}"
                f"{solicitacao.status:<22}"
                f"{solicitacao.quantidade_solicitacao:<6}"
                f"{(solicitacao.especificacao_tecnica or '')[:28]:<30}"
            )

        print()
        print(f"Total de solicitações: {len(solicitacoes)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_solicitacao_compra(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE SOLICITAÇÃO DE COMPRA")
        print("=" * 60)

        try:
            id_solicitacao = int(input("Código da solicitação: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao_compra = self.repository.buscar_por_id(id_solicitacao)

        if solicitacao_compra is None:
            print()
            print("Solicitação de compra não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print(f"Status válidos: {', '.join(STATUS_COMPRA_VALIDOS)}")
        print()

        try:
            turma_id_input = input(f"Turma [{solicitacao_compra.turma_id}]: ")
            if turma_id_input:
                solicitacao_compra.turma_id = int(turma_id_input)

            maquina_id_input = input(f"Máquina [{solicitacao_compra.maquina_id}]: ")
            if maquina_id_input:
                solicitacao_compra.maquina_id = int(maquina_id_input)

            status = input(f"Status [{solicitacao_compra.status}]: ")
            if status:
                solicitacao_compra.status = validar_status_compra(status)

            especificacao_tecnica = input(f"Especificação [{solicitacao_compra.especificacao_tecnica}]: ")
            if especificacao_tecnica:
                solicitacao_compra.especificacao_tecnica = validar_especificacao_tecnica(especificacao_tecnica)

            quantidade_solicitacao = input(f"Quantidade [{solicitacao_compra.quantidade_solicitacao}]: ")
            if quantidade_solicitacao:
                solicitacao_compra.quantidade_solicitacao = validar_quantidade_solicitacao(quantidade_solicitacao)

            sap_solicitacao = input(f"SAP [{solicitacao_compra.sap_solicitacao}]: ")
            if sap_solicitacao:
                solicitacao_compra.sap_solicitacao = validar_sap_solicitacao(sap_solicitacao)

            justificativa_solicitacao = input(f"Justificativa [{solicitacao_compra.justificativa_solicitacao}]: ")
            if justificativa_solicitacao:
                solicitacao_compra.justificativa_solicitacao = validar_justificativa_solicitacao(justificativa_solicitacao)

            patrimonio = input(f"Patrimônio [{solicitacao_compra.patrimonio}]: ")
            if patrimonio:
                solicitacao_compra.patrimonio = validar_patrimonio(patrimonio)

            equipamento = input(f"Equipamento [{solicitacao_compra.equipamento}]: ")
            if equipamento:
                solicitacao_compra.equipamento = validar_equipamento(equipamento)

            conjunto_mecanico = input(f"Conjunto mecânico [{solicitacao_compra.conjunto_mecanico}]: ")
            if conjunto_mecanico:
                solicitacao_compra.conjunto_mecanico = validar_conjunto_mecanico(conjunto_mecanico)

            arquivos = input(f"Arquivo(s) [{solicitacao_compra.arquivos}]: ")
            if arquivos:
                solicitacao_compra.arquivos = validar_arquivos(arquivos)

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.atualizar(solicitacao_compra)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_solicitacao_compra(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE SOLICITAÇÃO DE COMPRA")
        print("=" * 60)

        try:
            id_solicitacao = int(input("Código da solicitação: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao_compra = self.repository.buscar_por_id(id_solicitacao)

        if solicitacao_compra is None:
            print()
            print("Solicitação de compra não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Solicitação localizada")
        print("-" * 60)
        print(f"Código.........: {solicitacao_compra.id_solicitacao}")
        print(f"Status.........: {solicitacao_compra.status}")
        print(f"Especificação..: {solicitacao_compra.especificacao_tecnica}")
        print()

        resposta = input("Deseja realmente excluir esta solicitação? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_solicitacao)
        print()
        input("Pressione ENTER para continuar...")

    def listar_solicitacoes_excluidas(self):
        print()
        print("=" * 60)
        print("SOLICITAÇÕES DE COMPRA EXCLUÍDAS")
        print("=" * 60)
        solicitacoes = self.soft_delete.listar_excluidos()

        if not solicitacoes:
            print()
            print("Nenhuma solicitação excluída.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Status':<22}{'Excluída em':<25}")
        print("-" * 60)

        for solicitacao in solicitacoes:
            print(
                f"{solicitacao.id_solicitacao:<5}"
                f"{solicitacao.status:<22}"
                f"{str(solicitacao.deleted_at):<25}"
            )

        print()
        print(f"Total de solicitações excluídas: {len(solicitacoes)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_solicitacao_compra(self):
        print()
        print("=" * 60)
        print("RESTAURAR SOLICITAÇÃO EXCLUÍDA")
        print("=" * 60)

        try:
            id_solicitacao = int(input("Código da solicitação excluída: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao_compra = self.soft_delete.buscar_excluido_por_id(id_solicitacao)

        if solicitacao_compra is None:
            print()
            print("Solicitação excluída não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Solicitação localizada: {solicitacao_compra.especificacao_tecnica}")

        resposta = input("Deseja restaurar esta solicitação? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_solicitacao)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_definitivamente(self):
        print()
        print("=" * 60)
        print("REMOVER DEFINITIVAMENTE DO HISTÓRICO")
        print("=" * 60)

        try:
            id_solicitacao = int(input("Código da solicitação excluída: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        solicitacao_compra = self.soft_delete.buscar_excluido_por_id(id_solicitacao)

        if solicitacao_compra is None:
            print()
            print("Solicitação excluída não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("ATENÇÃO: esta ação apaga o registro do histórico e não pode ser desfeita!")
        resposta = input("Confirma a remoção definitiva? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.excluir_definitivamente(id_solicitacao)
        print()
        input("Pressione ENTER para continuar...")
