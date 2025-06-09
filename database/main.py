from database.db_config import conectar
from database.produto import cadastrar_produto, listar_produtos, editar_produto, excluir_produto
from database.cliente import cadastrar_cliente, listar_clientes, editar_cliente, excluir_cliente
from database.funcionario import cadastrar_funcionario, listar_funcionarios, editar_funcionario, excluir_funcionario
from database.pedido import (
    registrar_pedido, listar_pedidos, editar_pedido, excluir_pedido,
    relatorio_faturamento_por_pagamento, gerenciar_pedidos_cozinha
)
from database.estoque import visualizar_estoque
from database.mesa import visualizar_mesas, atualizar_status_mesa
from login import login, obter_senha_admin, salvar_senha_admin

def menu_administrador():
    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("1. Cadastrar Funcionário")
        print("2. Listar Funcionários")
        print("3. Editar Funcionário")
        print("4. Excluir Funcionário")
        print("5. Ver Relatório")
        print("6. Alterar Senha do Administrador")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_funcionario()
        elif opcao == '2':
            listar_funcionarios()
        elif opcao == '3':
            editar_funcionario()
        elif opcao == '4':
            excluir_funcionario()
        elif opcao == '5':
            relatorio_faturamento_por_pagamento()
        elif opcao == '6':
            nova_senha = input("Digite a nova senha para o administrador: ")
            salvar_senha_admin(nova_senha)
            print("✅ Senha atualizada com sucesso!")
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_gerente():
    while True:
        print("\n=== MENU GERENTE ===")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Editar Produto")
        print("4. Excluir Produto")
        print("5. Visualizar Estoque")
        print("6. Ver Relatório de Faturamento")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            listar_produtos()
        elif opcao == '3':
            editar_produto()
        elif opcao == '4':
            excluir_produto()
        elif opcao == '5':
            visualizar_estoque()
        elif opcao == '6':
            relatorio_faturamento_por_pagamento()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_atendente():
    while True:
        print("\n=== MENU ATENDENTE ===")
        print("1. Fazer Pedido")
        print("2. Editar Pedido")
        print("3. Excluir Pedido")
        print("4. Visualizar Estoque")
        print("5. Cadastrar Cliente")
        print("6. Listar Clientes")
        print("7. Editar Cliente")
        print("8. Excluir Cliente")
        print("9. Listar Pedidos")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            registrar_pedido()
        elif opcao == '2':
            editar_pedido()
        elif opcao == '3':
            excluir_pedido()
        elif opcao == '4':
            visualizar_estoque()
        elif opcao == '5':
            cadastrar_cliente()
        elif opcao == '6':
            listar_clientes()
        elif opcao == '7':
            editar_cliente()
        elif opcao == '8':
            excluir_cliente()
        elif opcao == '9':
            listar_pedidos()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_cozinheiro():
    while True:
        print("\n=== MENU COZINHEIRO ===")
        print("1. Ver Pedidos Pendentes")
        print("2. Atualizar Status de Pedido")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1' or opcao == '2':
            gerenciar_pedidos_cozinha()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_garcom():
    while True:
        print("\n=== MENU GARÇOM ===")
        print("1. Fazer Pedido")
        print("2. Visualizar Mesas")
        print("3. Atualizar Status da Mesa")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            registrar_pedido()
        elif opcao == '2':
            visualizar_mesas()
        elif opcao == '3':
            atualizar_status_mesa()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

def menu_inicial():
    while True:
        print("\n=== SISTEMA DE GESTÃO DE LANCHONETE ===")
        print("1. Login")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cargo = login()
            if cargo:
                return cargo
        elif escolha == "0":
            print("Encerrando o sistema.")
            exit()
        else:
            print("Opção inválida.")

def main():
    try:
        conexao = conectar()
        if conexao.is_connected():
            conexao.close()

            cargo = menu_inicial()

            if cargo == "administrador":
                menu_administrador()
            elif cargo == "gerente":
                menu_gerente()
            elif cargo == "atendente":
                menu_atendente()
            elif cargo == "cozinheiro":
                menu_cozinheiro()
            elif cargo == "garcom":
                menu_garcom()
            else:
                print("Cargo não reconhecido ou sem permissões.")
    except Exception as e:
        print(f"Erro ao conectar com o banco: {e}")

if __name__ == "__main__":
    main()
