from database.db_config import conectar

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO clientes (nome, cpf, telefone, endereco) VALUES (%s, %s, %s, %s)"
    valores = (nome, cpf, telefone, endereco)
    cursor.execute(sql, valores)

    conexao.commit()
    print("Cliente cadastrado com sucesso!")

    cursor.close()
    conexao.close()

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    print("\n=== LISTA DE CLIENTES ===")
    for cliente in clientes:
        print(f"ID: {cliente[0]}, Nome: {cliente[1]}, CPF: {cliente[2]}, Telefone: {cliente[3]}, Endereço: {cliente[4]}")

    cursor.close()
    conexao.close()

def editar_cliente():
    id_cliente = input("ID do cliente a editar: ")
    nome = input("Novo nome: ")
    cpf = input("Novo CPF: ")
    telefone = input("Novo telefone: ")
    endereco = input("Novo endereço: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE clientes SET nome=%s, cpf=%s, telefone=%s, endereco=%s WHERE id=%s"
    valores = (nome, cpf, telefone, endereco, id_cliente)
    cursor.execute(sql, valores)

    conexao.commit()
    print("Cliente atualizado com sucesso!")

    cursor.close()
    conexao.close()

def excluir_cliente():
    id_cliente = input("ID do cliente a excluir: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM clientes WHERE id=%s"
    cursor.execute(sql, (id_cliente,))

    conexao.commit()
    print("Cliente excluído com sucesso!")

    cursor.close()
    conexao.close()

