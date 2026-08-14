import hashlib

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from repositories.perfil_repository import PerfilRepository
from soft_delete.usuario_soft_delete import UsuarioSoftDelete
from utils.usuario_validacoes import (
    validar_nome_usuario,
    validar_email_usuario,
    validar_senha_usuario
)


class MenuUsuario:

    def __init__(self):
        self.repository = UsuarioRepository()
        self.perfil_repository = PerfilRepository()
        self.soft_delete = UsuarioSoftDelete()

    # submenu
    def exibir(self):
        while True:
            print()
            print("=" * 60)
            print("CTW MANUTENÇÃO - USUÁRIOS")
            print("=" * 60)
            print("1 - Cadastrar Usuário")
            print("2 - Buscar Usuário")
            print("3 - Listar Usuários")
            print("4 - Atualizar Usuário")
            print("5 - Excluir Usuário")
            print("6 - Ver Usuários Excluídos")
            print("7 - Restaurar Usuário Excluído")
            print("0 - Sair")
            print("=" * 60)

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_usuario()

            elif opcao == "2":
                self.buscar_usuario()

            elif opcao == "3":
                self.listar_usuario()

            elif opcao == "4":
                self.atualizar_usuario()

            elif opcao == "5":
                self.excluir_usuario()

            elif opcao == "6":
                self.listar_usuarios_excluidos()

            elif opcao == "7":
                self.restaurar_usuario()

            elif opcao == "0":
                self.repository.fechar()
                self.perfil_repository.fechar()
                self.soft_delete.fechar()
                print()
                print("Voltando ao menu principal...")
                break

            else:
                print()
                print("Opção inválida!")

    def _hash_senha(self, senha):
        # Hash simples (SHA-256) só para não gravar a senha em texto puro.
        # Em produção, prefira bcrypt/argon2 (com salt) em vez de SHA-256 puro.
        return hashlib.sha256(senha.encode("utf-8")).hexdigest()

    def cadastrar_usuario(self):
        print()
        print("=" * 60)
        print("CADASTRO DE USUÁRIO")
        print("=" * 60)

        try:
            nome_usuario = validar_nome_usuario(input("Nome: "))
            email_usuario = validar_email_usuario(input("Email: "))
            senha_usuario = validar_senha_usuario(input("Senha: "))
            id_perfil = int(input("Código do perfil (coordenador/gestor/professor/aluno): "))

            perfil = self.perfil_repository.buscar_por_id(id_perfil)
            if perfil is None:
                print()
                print("Perfil não encontrado.")
                input("\nPressione ENTER para continuar...")
                return

            turma_input = input("Código da turma (ENTER para nenhuma): ").strip()
            turma_id = int(turma_input) if turma_input else None

        except ValueError as erro:
            print()
            print(f"Erro: {erro}")
            input("\nPressione ENTER para continuar...")
            return

        usuario = Usuario(
            perfil_id=perfil.id_perfil,
            turma_id=turma_id,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            senha_hash=self._hash_senha(senha_usuario)
        )
        self.repository.salvar(usuario)
        print()
        input("Pressione ENTER para continuar...")

    def buscar_usuario(self):
        print()
        print("=" * 60)
        print("BUSCAR USUÁRIO")
        print("=" * 60)

        try:
            id_usuario = int(input("Código do usuário: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.repository.buscar_por_id(id_usuario)
        print()

        if usuario is None:
            print("Usuário não encontrado.")

        else:
            print(f"Código......: {usuario.id_usuario}")
            print(f"Nome........: {usuario.nome_usuario}")
            print(f"Email.......: {usuario.email_usuario}")
            print(f"Perfil (id).: {usuario.perfil_id}")
            print(f"Turma (id)..: {usuario.turma_id if usuario.turma_id else '-'}")

        print()
        input("Pressione ENTER para continuar...")

    def listar_usuario(self):
        print()
        print("=" * 60)
        print("LISTA DE USUÁRIOS")
        print("=" * 60)
        usuarios = self.repository.listar()

        if not usuarios:
            print()
            print("Nenhum usuário cadastrado.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<25}{'Email':<30}")
        print("-" * 60)

        for usuario in usuarios:
            print(f"{usuario.id_usuario:<5}{usuario.nome_usuario:<25}{usuario.email_usuario:<30}")

        print()
        print(f"Total de usuários: {len(usuarios)}")
        print()
        input("Pressione ENTER para continuar...")

    def atualizar_usuario(self):
        print()
        print("=" * 60)
        print("ATUALIZAÇÃO DE USUÁRIO")
        print("=" * 60)

        try:
            id_usuario = int(input("Código do usuário: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.repository.buscar_por_id(id_usuario)

        if usuario is None:
            print()
            print("Usuário não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Pressione ENTER para manter o valor atual.")
        print()

        nome_usuario = input(f"Nome [{usuario.nome_usuario}]: ")
        if nome_usuario:
            try:
                usuario.nome_usuario = validar_nome_usuario(nome_usuario)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        email_usuario = input(f"Email [{usuario.email_usuario}]: ")
        if email_usuario:
            try:
                usuario.email_usuario = validar_email_usuario(email_usuario)
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        senha_usuario = input("Nova senha (ENTER para manter): ")
        if senha_usuario:
            try:
                usuario.senha_hash = self._hash_senha(validar_senha_usuario(senha_usuario))
            except ValueError as erro:
                print(f"Erro: {erro}")
                input("\nPressione ENTER para continuar...")
                return

        perfil_input = input(f"Código do perfil [{usuario.perfil_id}]: ")
        if perfil_input:
            try:
                novo_perfil_id = int(perfil_input)
            except ValueError:
                print("Código de perfil inválido.")
                input("\nPressione ENTER para continuar...")
                return

            perfil = self.perfil_repository.buscar_por_id(novo_perfil_id)
            if perfil is None:
                print("Perfil não encontrado.")
                input("\nPressione ENTER para continuar...")
                return
            usuario.perfil_id = perfil.id_perfil

        turma_atual = usuario.turma_id if usuario.turma_id else '-'
        turma_input = input(f"Código da turma [{turma_atual}] (0 para remover): ")
        if turma_input:
            try:
                novo_turma_id = int(turma_input)
                usuario.turma_id = None if novo_turma_id == 0 else novo_turma_id
            except ValueError:
                print("Código de turma inválido.")
                input("\nPressione ENTER para continuar...")
                return

        self.repository.atualizar(usuario)
        print()
        input("Pressione ENTER para continuar...")

    def excluir_usuario(self):
        print()
        print("=" * 60)
        print("EXCLUSÃO DE USUÁRIO")
        print("=" * 60)

        try:
            id_usuario = int(input("Código do usuário: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.repository.buscar_por_id(id_usuario)

        if usuario is None:
            print()
            print("Usuário não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print("Usuário localizado")
        print("-" * 60)
        print(f"Código.....: {usuario.id_usuario}")
        print(f"Nome.......: {usuario.nome_usuario}")
        print()

        resposta = input("Deseja realmente excluir este usuário? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.repository.excluir(id_usuario)
        print()
        input("Pressione ENTER para continuar...")

    def listar_usuarios_excluidos(self):
        print()
        print("=" * 60)
        print("USUÁRIOS EXCLUÍDOS")
        print("=" * 60)
        usuarios = self.soft_delete.listar_excluidos()

        if not usuarios:
            print()
            print("Nenhum usuário excluído.")
            print()
            input("Pressione ENTER para continuar...")
            return

        print(f"{'ID':<5}{'Nome':<25}{'Excluído em':<25}")
        print("-" * 60)

        for usuario in usuarios:
            print(f"{usuario.id_usuario:<5}{usuario.nome_usuario:<25}{str(usuario.deleted_at):<25}")

        print()
        print(f"Total de usuários excluídos: {len(usuarios)}")
        print()
        input("Pressione ENTER para continuar...")

    def restaurar_usuario(self):
        print()
        print("=" * 60)
        print("RESTAURAR USUÁRIO EXCLUÍDO")
        print("=" * 60)

        try:
            id_usuario = int(input("Código do usuário excluído: "))

        except ValueError:
            print()
            print("Código inválido.")
            input("\nPressione ENTER para continuar...")
            return

        usuario = self.soft_delete.buscar_excluido_por_id(id_usuario)

        if usuario is None:
            print()
            print("Usuário excluído não encontrado.")
            input("\nPressione ENTER para continuar...")
            return

        print()
        print(f"Usuário localizado: {usuario.nome_usuario}")

        resposta = input("Deseja restaurar este usuário? (S/N): ").strip().upper()

        if resposta != "S":
            print()
            print("Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return

        self.soft_delete.restaurar(id_usuario)
        print()
        input("Pressione ENTER para continuar...")