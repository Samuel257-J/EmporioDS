from database.db_config import conectar
from database.estoque import atualizar_estoque

def registrar_pedido():
    id_cliente = input("ID do cliente: ")
    id_produto = input("ID do produto: ")
    quantidade = int(input("Quantidade: "))
    status = input("Status do pedido (ex: Pendente, Entregue): ")

    formas_validas = ['Dinheiro', 'Cartão', 'Pix']
    forma_pagamento = input("Forma de pagamento (Dinheiro, Cartão, Pix): ").capitalize()
    if forma_pagamento not in formas_validas:
        print("Forma de pagamento inválida. Pedido cancelado.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT preco FROM produtos WHERE id = %s", (id_produto,))
    resultado = cursor.fetchone()

    if resultado:
        preco_unitario = resultado[0]
        valor_total = preco_unitario * quantidade

        sql = """
            INSERT INTO pedidos (id_cliente, id_produto, quantidade, valor_total, status, forma_pagamento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (id_cliente, id_produto, quantidade, valor_total, status, forma_pagamento)
        cursor.execute(sql, valores)
        conexao.commit()

        atualizar_estoque(id_produto, quantidade, 'saida')

        print("Pedido registrado com sucesso!")
    else:
        print("Produto não encontrado.")

    cursor.close()
    conexao.close()

def listar_pedidos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT p.id, c.nome, pr.nome, p.quantidade, p.valor_total, p.status, p.forma_pagamento
        FROM pedidos p
        JOIN clientes c ON p.id_cliente = c.id
        JOIN produtos pr ON p.id_produto = pr.id
    """)
    pedidos = cursor.fetchall()

    print("\n=== LISTA DE PEDIDOS ===")
    for pedido in pedidos:
        print(f"ID: {pedido[0]}, Cliente: {pedido[1]}, Produto: {pedido[2]}, Quantidade: {pedido[3]}, "
              f"Total: R${pedido[4]:.2f}, Status: {pedido[5]}, Pagamento: {pedido[6]}")

    cursor.close()
    conexao.close()

def editar_pedido():
    id_pedido = input("ID do pedido para editar: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_produto, quantidade, status, forma_pagamento FROM pedidos WHERE id = %s", (id_pedido,))
    pedido = cursor.fetchone()

    if pedido:
        id_produto_atual, quantidade_atual, status_atual, pagamento_atual = pedido
        print(f"Pedido atual: Produto ID {id_produto_atual}, Quantidade {quantidade_atual}, Status {status_atual}, Pagamento: {pagamento_atual}")

        nova_quantidade = int(input("Nova quantidade: "))
        novo_status = input("Novo status: ")

        formas_validas = ['Dinheiro', 'Cartão', 'Pix']
        nova_forma_pagamento = input("Nova forma de pagamento (Dinheiro, Cartão, Pix): ").capitalize()
        if nova_forma_pagamento not in formas_validas:
            print("Forma de pagamento inválida. Edição cancelada.")
            return

        atualizar_estoque(id_produto_atual, quantidade_atual, 'entrada')
        atualizar_estoque(id_produto_atual, nova_quantidade, 'saida')

        cursor.execute("SELECT preco FROM produtos WHERE id = %s", (id_produto_atual,))
        preco_unitario = cursor.fetchone()[0]
        novo_valor_total = preco_unitario * nova_quantidade

        sql = """
            UPDATE pedidos
            SET quantidade = %s, valor_total = %s, status = %s, forma_pagamento = %s
            WHERE id = %s
        """
        valores = (nova_quantidade, novo_valor_total, novo_status, nova_forma_pagamento, id_pedido)
        cursor.execute(sql, valores)
        conexao.commit()
        print("Pedido atualizado com sucesso!")
    else:
        print("Pedido não encontrado.")

    cursor.close()
    conexao.close()

def excluir_pedido():
    id_pedido = input("ID do pedido para excluir: ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_produto, quantidade FROM pedidos WHERE id = %s", (id_pedido,))
    pedido = cursor.fetchone()

    if pedido:
        id_produto, quantidade = pedido
        confirmar = input(f"Tem certeza que deseja excluir o pedido {id_pedido}? (s/n): ")
        if confirmar.lower() == 's':
            atualizar_estoque(id_produto, quantidade, 'entrada')

            cursor.execute("DELETE FROM pedidos WHERE id = %s", (id_pedido,))
            conexao.commit()
            print("Pedido excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
    else:
        print("Pedido não encontrado.")

    cursor.close()
    conexao.close()

def relatorio_faturamento_por_pagamento():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT forma_pagamento, SUM(valor_total)
            FROM pedidos
            GROUP BY forma_pagamento
        """)
        resultados = cursor.fetchall()

        print("\n=== RELATÓRIO DE FATURAMENTO POR FORMA DE PAGAMENTO ===")
        for forma, total in resultados:
            print(f"Forma de Pagamento: {forma} | Total Faturado: R$ {total:.2f}")
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

def gerenciar_pedidos_cozinha():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Buscar pedidos com status pendente ou em preparo
        query = """
            SELECT p.id, c.nome AS cliente, pr.nome AS produto, p.quantidade, p.status
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id
            JOIN produtos pr ON p.id_produto = pr.id
            WHERE p.status IN ('pendente', 'em preparo')
            ORDER BY p.id
        """
        cursor.execute(query)
        pedidos = cursor.fetchall()

        if not pedidos:
            print("Nenhum pedido pendente para a cozinha no momento.")
            return

        print("\nPedidos pendentes para cozinha:")
        for pedido in pedidos:
            print(f"ID: {pedido['id']} - Cliente: {pedido['cliente']} - Produto: {pedido['produto']} - Quantidade: {pedido['quantidade']} - Status: {pedido['status']}")

        pedido_id = input("\nDigite o ID do pedido que deseja atualizar o status (ou '0' para sair): ")
        if pedido_id == '0':
            return

        pedido_ids = [str(p['id']) for p in pedidos]
        if pedido_id not in pedido_ids:
            print("ID inválido.")
            return

        print("\nEscolha o novo status:")
        print("1 - Em preparo")
        print("2 - Pronto")
        print("3 - Entregue")
        novo_status_opcao = input("Opção: ")

        status_map = {
            '1': 'em preparo',
            '2': 'pronto',
            '3': 'entregue'
        }

        if novo_status_opcao not in status_map:
            print("Opção inválida.")
            return

        novo_status = status_map[novo_status_opcao]

        update_query = "UPDATE pedidos SET status = %s WHERE id = %s"
        cursor.execute(update_query, (novo_status, pedido_id))
        conexao.commit()

        print(f"Status do pedido {pedido_id} atualizado para '{novo_status}'.")

    except Exception as e:
        print(f"Erro ao gerenciar pedidos da cozinha: {e}")
    finally:
        cursor.close()
        conexao.close()