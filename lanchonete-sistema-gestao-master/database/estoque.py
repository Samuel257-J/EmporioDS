from database.db_config import conectar

def atualizar_estoque(id_produto, quantidade, operacao):
    """
    Atualiza o estoque do produto com base na operação:
    - 'saida': reduz o estoque
    - 'entrada': aumenta o estoque
    """
    conexao = conectar()
    cursor = conexao.cursor()

    if operacao == 'saida':
        sql_estoque = "UPDATE produtos SET estoque = estoque - %s WHERE id = %s"
    elif operacao == 'entrada':
        sql_estoque = "UPDATE produtos SET estoque = estoque + %s WHERE id = %s"
    else:
        print("Operação inválida para o estoque.")
        return

    try:
        cursor.execute(sql_estoque, (quantidade, id_produto))
        conexao.commit()

        sql_registro = """
            INSERT INTO estoque (id_produto, quantidade_entrada, quantidade_saida)
            VALUES (%s, %s, %s)
        """
        entrada = quantidade if operacao == 'entrada' else 0
        saida = quantidade if operacao == 'saida' else 0
        cursor.execute(sql_registro, (id_produto, entrada, saida))
        conexao.commit()

        print("Estoque atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar estoque: {e}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()


def visualizar_estoque():
    """
    Exibe todas as movimentações registradas no estoque
    """
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT e.id, p.nome, e.quantidade_entrada, e.quantidade_saida, e.data_hora
            FROM estoque e
            JOIN produtos p ON e.id_produto = p.id
            ORDER BY e.data_hora DESC
        """)
        resultados = cursor.fetchall()

        print("\n=== MOVIMENTAÇÃO DO ESTOQUE ===")
        for item in resultados:
            print(f"ID: {item[0]} | Produto: {item[1]} | Entrada: {item[2]} | Saída: {item[3]} | Data: {item[4]}")
    except Exception as e:
        print(f"Erro ao consultar movimentações de estoque: {e}")
    finally:
        cursor.close()
        conexao.close()