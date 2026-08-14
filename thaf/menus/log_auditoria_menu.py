from models.log_auditoria import LogAuditoria
from repositories.log_auditoria_repository import LogAuditoriaRepository
from soft_delete.log_auditoria_soft_delete import LogAuditoriaSoftDelete
from utils.log_auditoria_validacoes import (
    validar_acao,
    validar_usuario_id,
    validar_endereco_ip
)


class LogAuditoriaMenu:
    def __init__(self):
        self.repository = LogAuditoriaRepository()
        self.soft_delete = LogAuditoriaSoftDelete()

    def exibir_menu(self):
        while True:
            print("\n===== MENU LOGS DE AUDITORIA =====")
            print("1 - Registrar log de auditoria")
            print("2 - Listar logs de auditoria")
            print("3 - Buscar log de auditoria por id")
            print("4 - Listar logs de auditoria por usuário")
            print("5 - Excluir log de auditoria")
            print("6 - Listar histórico (ativos + excluídos)")
            print("7 - Menu de logs excluídos (restaurar/expurgar)")
            print("0 - Voltar")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.registrar_log_auditoria()
            elif opcao == "2":
                self.listar_logs_auditoria()
            elif opcao == "3":
                self.buscar_log_auditoria_por_id()
            elif opcao == "4":
                self.listar_logs_auditoria_por_usuario()
            elif opcao == "5":
                self.excluir_log_auditoria()
            elif opcao == "6":
                self.listar_historico()
            elif opcao == "7":
                self.menu_excluidos()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

    def registrar_log_auditoria(self):
        try:
            usuario_id = validar_usuario_id(int(input("ID do usuário: ").strip()))
            acao = validar_acao(input("Ação: "))
            endereco_ip = validar_endereco_ip(input("Endereço IP (opcional): "))

            log_auditoria = LogAuditoria(
                usuario_id=usuario_id,
                acao=acao,
                endereco_ip=endereco_ip
            )
            self.repository.salvar(log_auditoria)

        except ValueError as erro:
            print(f"Erro de validação: {erro}")

    def listar_logs_auditoria(self):
        logs = self.repository.listar()

        if not logs:
            print("Nenhum log de auditoria encontrado.")
            return

        for log in logs:
            print(log)

    def buscar_log_auditoria_por_id(self):
        try:
            id_log = int(input("ID do log de auditoria: ").strip())
            log = self.repository.buscar_por_id(id_log)

            if log is None:
                print("Log de auditoria não encontrado!")
            else:
                print(log)

        except ValueError:
            print("ID inválido!")

    def listar_logs_auditoria_por_usuario(self):
        try:
            usuario_id = int(input("ID do usuário: ").strip())
            logs = self.repository.listar_por_usuario(usuario_id)

            if not logs:
                print("Nenhum log de auditoria encontrado para este usuário.")
                return

            for log in logs:
                print(log)

        except ValueError:
            print("ID inválido!")

    def excluir_log_auditoria(self):
        try:
            id_log = int(input("ID do log de auditoria a excluir: ").strip())
            self.repository.excluir(id_log)

        except ValueError:
            print("ID inválido!")

    def listar_historico(self):
        historico = self.repository.listar_historico()

        if not historico:
            print("Nenhum registro no histórico.")
            return

        for registro in historico:
            print(registro)

    def menu_excluidos(self):
        while True:
            print("\n----- LOGS DE AUDITORIA EXCLUÍDOS -----")
            print("1 - Listar excluídos")
            print("2 - Restaurar log de auditoria")
            print("3 - Expurgar log de auditoria (irreversível)")
            print("0 - Voltar")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                excluidos = self.soft_delete.listar_excluidos()
                if not excluidos:
                    print("Nenhum log de auditoria excluído.")
                else:
                    for registro in excluidos:
                        print(registro)

            elif opcao == "2":
                try:
                    id_log = int(input("ID do log a restaurar: ").strip())
                    self.soft_delete.restaurar(id_log)
                except ValueError:
                    print("ID inválido!")

            elif opcao == "3":
                try:
                    id_log = int(input("ID do log a expurgar: ").strip())
                    confirmacao = input(
                        "Essa ação é irreversível. Confirma? (s/n): "
                    ).strip().lower()
                    if confirmacao == "s":
                        self.soft_delete.expurgar(id_log)
                    else:
                        print("Operação cancelada.")
                except ValueError:
                    print("ID inválido!")

            elif opcao == "0":
                break
            else:
                print("Opção inválida!")