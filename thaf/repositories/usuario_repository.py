from database.conexao import Conexao
from models.usuario import Usuario


class UsuarioRepository:
    """usuarios usa soft delete por HERANÇA: o trigger trg_soft_delete_usuarios
    (BEFORE DELETE, fn_mover_para_historico) copia a linha para
    usuarios_deletados e deixa o DELETE original concluir na tabela
    usuarios. Diferente de perfis (soft delete IN-PLACE), aqui a linha
    realmente some da tabela principal, então:

    - o cursor.rowcount do DELETE É confiável (não precisa checar
      existência antes, como faz PerfilRepository.excluir).
    - como usuarios_deletados herda de usuarios, um "SELECT/UPDATE/DELETE
      FROM usuarios" sem a palavra-chave ONLY também enxergaria/afetaria
      as linhas já excluídas (comportamento padrão de herança do
      Postgres). Por isso toda consulta e todo comando de escrita deste
      repositório usa "ONLY usuarios", garantindo que só usuários ativos
      sejam lidos/alterados. Para consultar excluídos, use
      soft_delete/usuario_soft_delete.py, que lê diretamente de
      usuarios_deletados.
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
            criado_em=registro[6]
        )

    def salvar(self, usuario):
        sql = """
        INSERT INTO usuarios
        (
            perfil_id,
            turma_id,
            nome_usuario,
            email_usuario,
            senha_hash
        )
        VALUES
        (
            %s, %s, %s, %s, %s
        )
        """
        valores = (
            usuario.perfil_id,
            usuario.turma_id,
            usuario.nome_usuario,
            usuario.email_usuario,
            usuario.senha_hash
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            print("Usuário cadastrado com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao cadastrar usuário. Erro: {erro}")

    def buscar_por_id(self, id_usuario):
        sql = """
        SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
        FROM ONLY usuarios
        WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_usuario,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_usuario(registro)
        except Exception as erro:
            print(f"Erro ao buscar usuário pelo id. Erro: {erro}")
            return None

    def buscar_por_email(self, email_usuario):
        sql = """
        SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
        FROM ONLY usuarios
        WHERE email_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (email_usuario,))
            registro = self.db.cursor.fetchone()
            if registro is None:
                return None
            return self.criar_usuario(registro)
        except Exception as erro:
            print(f"Erro ao buscar usuário pelo email. Erro: {erro}")
            return None

    def listar(self):
        sql = """
            SELECT id_usuario, perfil_id, turma_id, nome_usuario, email_usuario, senha_hash, criado_em
            FROM ONLY usuarios
            ORDER BY nome_usuario
        """
        try:
            self.db.cursor.execute(sql)
            registros = self.db.cursor.fetchall()
            return [self.criar_usuario(registro) for registro in registros]
        except Exception as erro:
            print(f"Erro ao listar usuários: {erro}")
            return []

    def atualizar(self, usuario):
        sql = """UPDATE ONLY usuarios
        SET
            perfil_id = %s,
            turma_id = %s,
            nome_usuario = %s,
            email_usuario = %s,
            senha_hash = %s
        WHERE id_usuario = %s
        """
        valores = (
            usuario.perfil_id,
            usuario.turma_id,
            usuario.nome_usuario,
            usuario.email_usuario,
            usuario.senha_hash,
            usuario.id_usuario
        )
        try:
            self.db.cursor.execute(sql, valores)
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Usuário não encontrado!")
            else:
                print("Usuário atualizado!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao atualizar usuário: {erro}")

    def excluir(self, id_usuario):
        sql = """
            DELETE FROM ONLY usuarios
            WHERE id_usuario = %s
        """
        try:
            self.db.cursor.execute(sql, (id_usuario,))
            self.db.commit()
            if self.db.cursor.rowcount == 0:
                print("Usuário não encontrado!")
            else:
                print("Usuário excluído com sucesso!")
        except Exception as erro:
            self.db.rollback()
            print(f"Erro ao excluir usuário: {erro}")

    def fechar(self):
        self.db.fechar()