from database.db_config import conectar

def cadastrar_produto():
    nome = input("Nome do produto: ")
    categoria = input("Categoria: ")
    preco = float(input("Preço: "))
    estoque = int(input("Quantidade em estoque: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (%s, %s, %s, %s)"
    valores = (nome, categoria, preco, estoque)
    cursor.execute(sql, valores)

    conexao.commit()
    print("Produto cadastrado com sucesso!")

    cursor.close()
    conexao.close()

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    print("\n=== LISTA DE PRODUTOS ===")
    for produto in produtos:
        print(f"ID: {produto[0]}, Nome: {produto[1]}, Categoria: {produto[2]}, Preço: R${produto[3]:.2f}, Estoque: {produto[4]}")

    cursor.close()
    conexao.close()

def editar_produto():
    id_produto = input("ID do produto a editar: ")
    nome = input("Novo nome: ")
    categoria = input("Nova categoria: ")
    preco = float(input("Novo preço: "))
    estoque = int(input("Nova quantidade em estoque: "))

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE produtos SET nome=%s, categoria=%s, preco=%s, estoque=%s WHERE id=%s"
    valores = (nome, categoria, preco, estoque, id_produto)
    cursor.execute(sql, valores)

    conexao.commit()
    print("Produto atualizado com sucesso!")

    cursor.close()
    conexao.close()

def excluir_produto():
    id_produto = input("ID do produto a excluir: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM produtos WHERE id=%s"
    cursor.execute(sql, (id_produto,))

    conexao.commit()
    print("Produto excluído com sucesso!")

    cursor.close()
    conexao.close()



