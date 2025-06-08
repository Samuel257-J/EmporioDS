import mysql.connector
import os

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bardopastel2020",
        database="lanchonete_db"
    )

def obter_senha_admin():
    if not os.path.exists("admin_senha.txt"):
        with open("admin_senha.txt", "w") as f:
            f.write("1234")  # senha padrão
    with open("admin_senha.txt", "r") as f:
        return f.read().strip()

def salvar_senha_admin(nova_senha):
    with open("admin_senha.txt", "w") as f:
        f.write(nova_senha)

def login():
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    # Login fixo do administrador
    if usuario == "admin1234" and senha == obter_senha_admin():
        print("\n✅ Bem-vindo, Administrador!")
        return "administrador"

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM funcionarios WHERE usuario = %s AND senha = %s"
    cursor.execute(query, (usuario, senha))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        print(f"\n✅ Bem-vindo(a), {resultado['nome']}!")
        return resultado['cargo']
    else:
        print("\n❌ Usuário ou senha incorretos.")
        return None


