from menus.perfil_menu import MenuPerfil
from menus.solicitacao_compra_menu import MenuSolicitacaoCompra

# Ao criar uma nova classe: importe o submenu dela aqui em cima e
# adicione uma opção no bloco abaixo (nunca edite a linha de outra classe).


class MenuPrincipal:

    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - MENU PRINCIPAL")
            print("=" * 60)
            print("1 - Perfis")
            print("2 - Solicitações de Compra")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                MenuPerfil().exibir()

            elif opcao == "2":
                MenuSolicitacaoCompra().exibir()

            elif opcao == "0":
                print()
                print("Sistema Encerrado")
                break

            else:
                print()
                print("Opção inválida!")

