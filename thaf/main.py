"""Ponto de entrada do sistema CTW MANUTENÇÃO.

Execute a partir da pasta 'thaf/' (mesmo nível deste arquivo):

    cd thaf
    python main.py

Antes de rodar, configure o arquivo .env (veja .env.example) com os
dados de conexão do banco Postgres e garanta que o script
database/script_bd.sql já foi executado no banco de destino.
"""

from menu_principal import MenuPrincipal


def main():
    try:
        MenuPrincipal().exibir()
    except KeyboardInterrupt:
        print()
        print("Sistema Encerrado")
    except Exception as erro:
        print()
        print(f"Erro inesperado: {erro}")


if __name__ == "__main__":
    main()