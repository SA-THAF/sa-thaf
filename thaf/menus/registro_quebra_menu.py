from models.registro_quebra import RegistroQuebra
from repositories.registro_quebra_repository import RegistroQuebraRepository
from soft_delete.registro_quebra_soft_delete import RegistroQuebraSoftDelete
from utils.registro_quebra_validacoes import (
    validar_item_id,
    validar_usuario_id,
    validar_descricao_quebra,
    validar_foto_url
)


class MenuRegistroQuebra:

    def __init__(self):
        self.repository = RegistroQuebraRepository()
        self.soft_delete = RegistroQuebraSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - REGISTROS DE QUEBRA")
            print("=" * 60)
            print("1 - Cadastrar Registro de Quebra")
            print("2 - Buscar Registro de Quebra")
            print("3 - Listar Registros de Quebra")
            print("4 - Atualizar Registro de Quebra")
            print("5 - Excluir Registro de Quebra")
            print("6 - Ver Registros de Quebra Excluídos")
            print("7 - Restaurar Registro de Quebra Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_registro_quebra()

            elif opcao == "2":
                self.buscar_registro_quebra()

            elif opcao == "3":
                self.listar_registro_quebra()

            elif opcao == "4":
                self.atualizar_registro_quebra()

            elif opcao == "5":
                self.excluir_registro_quebra()

            elif opcao == "6":
                self.listar_registros_excluidos()

            elif opcao == "7":
                self.restaurar_registro_quebra()

            elif opcao == "0":
                self.repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def cadastrar_registro_quebra(self):
        print()
        print("=" * 60)
        print("CADASTRO DE REGISTRO DE QUEBRA")
        print("=" * 60)

        try:
            item_id = validar_item_id(input("Código do item: "))
            usuario_id = validar_usuario_id(input("Código do usuário: "))
            descricao_quebra = validar_descricao_quebra(input("Descrição da quebra: "))
            foto_url = validar_foto_url(input("URL da foto (opcional): "))

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        registro_quebra = RegistroQuebra(
            item_id=item_id,
            usuario_id=usuario_id,
            descricao_quebra=descricao_quebra,
            foto_url=foto_url
        )
        self.repository.salvar(registro_quebra)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_registro_quebra(self):
        print()
        print("=" * 60)
        print("BUSCAR REGISTRO DE QUEBRA")
        print("=" * 60)

        try:
            id_quebra = int(input("Código do registro de quebra: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        registro = self.repository.buscar_por_id(id_quebra)
        print()

        if registro is None:
            print("Registro de quebra não encontrado.")

        else:
            print(f"Código......: {registro.id_quebra}")
            print(f"Item........: {registro.item_id}")
            print(f"Usuário.....: {registro.usuario_id}")
            print(f"Descrição...: {registro.descricao_quebra}")
            print(f"Foto........: {registro.foto_url or '-'}")
            print(f"Criado em...: {registro.criado_em}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_registro_quebra(self):
        print()
        print("=" * 60)
        print("LISTA DE REGISTROS DE QUEBRA")
        print("=" * 60)
        registros = self.repository.listar()

        if not registros:
            print()
            print("Nenhum registro de quebra cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Item':<8}{'Usuário':<10}{'Descrição':<30}{'Criado em':<20}")
        print("-" * 75)

        for registro in registros:
            print(f"{registro.id_quebra:<5}{registro.item_id:<8}{registro.usuario_id:<10}"
                  f"{(registro.descricao_quebra or ''):<30}{str(registro.criado_em):<20}")

        print()
        print(f"Total de registros: {len(registros)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_registro_quebra(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE REGISTRO DE QUEBRA")
        print("=" * 60)

        try:
            id_quebra = int(input("Código do registro de quebra: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        registro = self.repository.buscar_por_id(id_quebra)

        if registro is None:
            print()
            print("Registro de quebra não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print("(Item e usuário não podem ser alterados aqui.)")
        print()

        descricao_quebra = input(f"Descrição [{registro.descricao_quebra}]: ")
        if descricao_quebra:
            try:
                registro.descricao_quebra = validar_descricao_quebra(descricao_quebra)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        foto_url = input(f"Foto [{registro.foto_url or '-'}]: ")
        if foto_url:
            registro.foto_url = validar_foto_url(foto_url)

        self.repository.atualizar(registro)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_registro_quebra(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE REGISTRO DE QUEBRA")
        print("=" * 60)

        try:
            id_quebra = int(input("Código do registro de quebra: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        registro = self.repository.buscar_por_id(id_quebra)

        if registro is None:
            print()
            print("Registro de quebra não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Registro localizado")
        print("-" * 60)
        print(f"Código.....: {registro.id_quebra}")
        print(f"Descrição..: {registro.descricao_quebra}")
        print()

        resposta = input("Deseja realmente excluir este registro? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_quebra)
        print()
        input("Pressione ENTER para continuar...")

    def listar_registros_excluidos(self):
        print()
        print("=" * 60)
        print("REGISTROS DE QUEBRA EXCLUÍDOS")
        print("=" * 60)
        registros = self.soft_delete.listar_excluidos()

        if not registros:
            print()
            print("Nenhum registro de quebra excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Item':<8}{'Usuário':<10}{'Excluído em':<25}")
        print("-" * 60)

        for registro in registros:
            print(f"{registro.id_quebra:<5}{registro.item_id:<8}{registro.usuario_id:<10}"
                  f"{str(registro.deleted_at):<25}")

        print()
        print(f"Total de registros excluídos: {len(registros)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_registro_quebra(self):
        print()
        print("=" * 60)
        print("RESTAURAR REGISTRO DE QUEBRA EXCLUÍDO")
        print("=" * 60)

        try:
            id_quebra = int(input("Código do registro de quebra excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        registro = self.soft_delete.buscar_excluido_por_id(id_quebra)

        if registro is None:
            print()
            print("Registro de quebra excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Registro localizado: {registro.descricao_quebra}")

        resposta = input("Deseja restaurar este registro? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_quebra)
        print()
        input("Pressione ENTER para continuar...")