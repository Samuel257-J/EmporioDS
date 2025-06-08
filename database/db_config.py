import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # ou outro usuário válido
        password="bardopastel2020",  # troque pela senha correta
        database="lanchonete_db"  # você pode mudar depois
    )

if __name__ == "__main__":
    try:
        conexao = conectar()
        if conexao.is_connected():
            print("Conexão bem-sucedida!")
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar: {erro}")

