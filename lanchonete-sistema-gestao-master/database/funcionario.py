from database.db_config import conectar

CARGOS_VALIDOS = ["gerente", "atendente", "cozinheiro", "garcom"]

def cadastrar_funcionario():
    nome = input("Nome do funcionário: ")
    cpf = input("CPF do funcionário (somente números): ")

    while True:
        cargo = input("Cargo (gerente / atendente / cozinheiro / garcom): ").lower()
        if cargo in CARGOS_VALIDOS:
            break
        else:
            print("❌ Cargo inválido. Escolha entre: gerente, atendente, cozinheiro ou garcom.")

    usuario = input("Nome de usuário: ")
    senha = input("Senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO funcionarios (nome, cpf, cargo, usuario, senha) VALUES (%s, %s, %s, %s, %s)"
    valores = (nome, cpf, cargo, usuario, senha)
    cursor.execute(sql, valores)

    conexao.commit()
    print("✅ Funcionário cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionarios")
    funcionarios = cursor.fetchall()

    print("\n=== LISTA DE FUNCIONÁRIOS ===")
    for funcionario in funcionarios:
        print(f"ID: {funcionario[0]}, Nome: {funcionario[1]}, CPF: {funcionario[2]}, Cargo: {funcionario[3]}, Usuário: {funcionario[4]}")

    cursor.close()
    conexao.close()


def editar_funcionario():
    id_funcionario = input("ID do funcionário a editar: ")
    nome = input("Novo nome: ")
    cpf = input("Novo CPF: ")

    while True:
        cargo = input("Novo cargo (gerente / atendente / cozinheiro / garcom): ").lower()
        if cargo in CARGOS_VALIDOS:
            break
        else:
            print("❌ Cargo inválido. Escolha entre: gerente, atendente, cozinheiro ou garcom.")

    usuario = input("Novo usuário: ")
    senha = input("Nova senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "UPDATE funcionarios SET nome=%s, cpf=%s, cargo=%s, usuario=%s, senha=%s WHERE id=%s"
    valores = (nome, cpf, cargo, usuario, senha, id_funcionario)
    cursor.execute(sql, valores)

    conexao.commit()
    print("✅ Funcionário atualizado com sucesso!")

    cursor.close()
    conexao.close()


def excluir_funcionario():
    id_funcionario = input("ID do funcionário a excluir: ")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM funcionarios WHERE id=%s"
    cursor.execute(sql, (id_funcionario,))

    conexao.commit()
    print("✅ Funcionário excluído com sucesso!")

    cursor.close()
    conexao.close()


