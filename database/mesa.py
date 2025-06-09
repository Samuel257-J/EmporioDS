from database.db_config import conectar

def visualizar_mesas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, numero, status FROM mesas")
    mesas = cursor.fetchall()

    print("\n=== MESAS DISPONÍVEIS ===")
    for mesa in mesas:
        print(f"ID: {mesa[0]} | Número: {mesa[1]} | Status: {mesa[2]}")

    cursor.close()
    conexao.close()

def atualizar_status_mesa():
    numero = input("Digite o número da mesa: ")
    novo_status = input("Novo status (livre / ativa / ocupada): ").lower()

    if novo_status not in ["livre", "ativa", "ocupada"]:
        print("❌ Status inválido.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE mesas SET status = %s WHERE numero = %s"
    cursor.execute(sql, (novo_status, numero))
    conexao.commit()

    if cursor.rowcount:
        print("✅ Status da mesa atualizado com sucesso!")
    else:
        print("❌ Mesa não encontrada.")

    cursor.close()
    conexao.close()
