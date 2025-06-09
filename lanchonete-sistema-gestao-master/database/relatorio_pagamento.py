from database.db_config import conectar

def relatorio_por_forma_pagamento():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT forma_pagamento, SUM(valor_total) as total
            FROM pedidos
            GROUP BY forma_pagamento
        """)
        resultados = cursor.fetchall()

        print("\n=== RELATÓRIO DE FATURAMENTO POR FORMA DE PAGAMENTO ===")
        for linha in resultados:
            forma, total = linha
            print(f"Forma de Pagamento: {forma} | Faturamento Total: R${total:.2f}")
    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
    finally:
        cursor.close()
        conexao.close()
