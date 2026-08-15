from menus.perfil_menu import MenuPerfil
from menus.turma_menu import MenuTurma
from menus.usuario_menu import MenuUsuario
from menus.log_auditoria_menu import MenuLogAuditoria
from menus.setor_menu import MenuSetor
from menus.maquina_menu import MenuMaquina
from menus.item_almoxarifado_menu import MenuItemAlmoxarifado
from menus.alerta_estoque_menu import MenuAlertaEstoque
from menus.registro_quebra_menu import MenuRegistroQuebra
from menus.solicitacao_servico_menu import MenuSolicitacaoServico
from menus.ordem_servico_menu import MenuOrdemServico
from menus.solicitacao_compra_menu import MenuSolicitacaoCompra
from menus.calendario_preventivo_menu import MenuCalendarioPreventivo

# Ao criar uma nova classe: importe o submenu dela aqui em cima e
# adicione uma opção no bloco abaixo (nunca edite a linha de outra classe).


class MenuPrincipal:

    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - MENU PRINCIPAL")
            print("=" * 60)
            print("-- Autenticação e RBAC --")
            print("1  - Perfis de Acesso")
            print("2  - Turmas")
            print("3  - Usuários")
            print("4  - Logs de Auditoria")
            print("-- Mapa da Oficina e Maquinário --")
            print("5  - Setores")
            print("6  - Máquinas")
            print("-- Almoxarifado e Ferramentaria --")
            print("7  - Itens de Almoxarifado")
            print("8  - Alertas de Estoque")
            print("9  - Registros de Quebra")
            print("-- Ordens de Serviço e Execução --")
            print("10 - Solicitações de Serviço")
            print("11 - Ordens de Serviço")
            print("-- Compras --")
            print("12 - Solicitações de Compra")
            print("-- Calendário Preventivo --")
            print("13 - Calendário Preventivo")
            print("-" * 60)
            print("0  - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                MenuPerfil().exibir()

            elif opcao == "2":
                MenuTurma().exibir()

            elif opcao == "3":
                MenuUsuario().exibir()

            elif opcao == "4":
                MenuLogAuditoria().exibir()

            elif opcao == "5":
                MenuSetor().exibir()

            elif opcao == "6":
                MenuMaquina().exibir()

            elif opcao == "7":
                MenuItemAlmoxarifado().exibir()

            elif opcao == "8":
                MenuAlertaEstoque().exibir()

            elif opcao == "9":
                MenuRegistroQuebra().exibir()

            elif opcao == "10":
                MenuSolicitacaoServico().exibir()

            elif opcao == "11":
                MenuOrdemServico().exibir()

            elif opcao == "12":
                MenuSolicitacaoCompra().exibir()

            elif opcao == "13":
                MenuCalendarioPreventivo().exibir()

            elif opcao == "0":
                print()
                print("Sistema Encerrado")
                break

            else:
                print()
                print("Opção inválida!")