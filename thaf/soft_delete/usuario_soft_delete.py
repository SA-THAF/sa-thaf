from database.conexao import Conexao
from models.usuario import Usuario


class UsuarioSoftDelete:
    """Operações sobre usuários EXCLUÍDOS.

    usuarios usa soft delete por HERANÇA: ao excluir, o trigger
    trg_soft_delete_usuarios move a linha inteira para a tabela
    usuarios_deletados (INHERITS usuarios) e conclui o DELETE físico na
    tabela usuarios. Diferente de PerfilSoftDelete (que só lê
    perfis WHERE deleted_at IS NOT NULL), aqui os excluídos ficam numa
    tabela separada, então as consultas abaixo vão direto em
    usuarios_deletados.

    Fica em pasta separada de repositories/ pelo mesmo motivo do módulo
    de perfis: o CRUD normal (repositories/usuario_repository.py) só
    enxerga a tabela ativa (usando ONLY usuarios) e nunca deveria
    consultar o histórico.

    Restaurar aqui não é um simples UPDATE (como em perfis): como a
    linha foi fisicamente movida, restaurar() precisa reinserir a linha
    em usuarios com o mesmo id_usuario (por isso o OVERRIDING SYSTEM
    VALUE, necessário porque id_usuario é GENERATED ALWAYS AS IDENTITY)
    e então remover a cópia de usuarios_deletados, tudo na mesma
    transação.
    """

    def __init__(self):
        self.db = Conexao()

    def criar_usuario(self, registro):
        return Usuario(
            id_usuario=registro[0],
            perfil_id=registro[1],
            turma_id=registro[2],
            nome_usuario=registro[3],
            email_usuario=registro[4],
            senha_hash=registro[5],
            criado_em=registro[6],
            deleted_at=registro[7]
        )

    def listar_excluidos(self):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em, deleted_at
            FROM usuarios_deletados
            ORDER BY deleted_at DESC
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            return [self.criar_usuario(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar usuários excluídos: {erro}")
            return []

    def buscar_excluido_por_id(self, id_usuario):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em, deleted_at
            FROM usuarios_deletados
            WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_usuario,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_usuario(registro)
        except Exception as erro:
            print(f"Erro ao buscar usuário excluído pelo id. Erro: {erro}")
            return None

    def restaurar(self, id_usuario):
        usuario = self.buscar_excluido_por_id(id_usuario)
        if usuario is None:
            print("Usuário excluído não encontrado!")
            return

        sql_inserir = """
            INSERT INTO usuarios
                (id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em)
            OVERRIDING SYSTEM VALUE
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        sql_remover_historico = """
            DELETE FROM usuarios_deletados
            WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql_inserir, (
                usuario.id_usuario,
                usuario.perfil_id,
                usuario.turma_id,
                usuario.nome_usuario,
                usuario.email_usuario,
                usuario.senha_hash,
                usuario.criado_em
            ))
            self.db.cursor.execute(sql_remover_historico, (id_usuario,))
            self.db.commit()
            print("Usuário restaurado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao restaurar usuário: {erro}")

    def fechar(self):
        self.db.fechar()