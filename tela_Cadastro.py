import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk

class TelaCadastro:
    def __init__(self, master, ao_logar_callback):
        self.master = master
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")
        self.ao_logar_callback = ao_logar_callback
        self.master.title("CADASTRO - Empório do Sabor")	
        self.master.geometry("425x582")
        self.master.resizable(False, False)
        
        # Centralizar janela na tela
        largura_janela = 425
        altura_janela = 582

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        try:
            self.fundo = carregar_imagem_tk("telaCadastro.png", (425, 582))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem de fundo:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=425, height=582, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        fonte = ("Arial", 9)

        # ====== LABELS E CAMPOS DE CADASTRO ======

        # Nome
        tk.Label(self.master, text="Nome:", font=fonte, bg="white").place(x=112, y=135)
        self.entry_nome = tk.Entry(self.master, font=fonte, bd=0, justify="center")
        self.entry_nome.place(x=112, y=160, width=200, height=28)

        # CPF
        tk.Label(self.master, text="CPF:", font=fonte, bg="white").place(x=112, y=205)
        self.entry_cpf = tk.Entry(self.master, font=fonte, bd=0, justify="center")
        self.entry_cpf.place(x=112, y=230, width=200, height=28)

        # Cargo
        tk.Label(self.master, text="Cargo:", font=fonte, bg="white").place(x=112, y=275)
        self.cargo_var = tk.StringVar()
        self.cargo_var.set("Atendente")  # Valor padrão
        self.option_cargo = tk.OptionMenu(self.master, self.cargo_var, "Atendente", "Cozinheiro", "Garçom", "Gerente")
        self.option_cargo.config(font=fonte)
        self.option_cargo.place(x=112, y=300, width=200, height=28)

        # Usuário
        tk.Label(self.master, text="Usuário:", font=fonte, bg="white").place(x=112, y=345)
        self.entry_usuario = tk.Entry(self.master, font=fonte, bd=0, justify="center")
        self.entry_usuario.place(x=112, y=370, width=200, height=28)

        # Senha
        tk.Label(self.master, text="Senha:", font=fonte, bg="white").place(x=112, y=415)
        self.entry_senha = tk.Entry(self.master, font=fonte, bd=0, justify="center", show="*")
        self.entry_senha.place(x=112, y=440, width=200, height=28)

        # Botão Cadastrar
        self.botao_cadastrar = tk.Button(
            self.master,
            text="Cadastrar",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.cadastrar_usuario
        )
        # Botão Voltar
        self.botao_voltar = tk.Button(
            self.master,
            text="Voltar",
            font=("Arial", 10, "bold"),
            bg="#CE0707",
            fg="white",
            command=self.voltar_login
        )
        self.botao_cadastrar.place(x=310, y=500, width=100, height=40)
        self.botao_voltar.place(x=20, y=500, width=100, height=40)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        cargo = self.cargo_var.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        self.inserir_funcionario(nome, cpf, cargo, usuario, senha)

        # Validação simples
        if not nome or not cpf or not usuario or not senha:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        # Aqui você pode inserir no banco de dados
        print(f"Usuário cadastrado: {usuario}, Nome: {nome}, CPF: {cpf}, Cargo: {cargo}")
        messagebox.showinfo("Cadastro realizado", "Cadastro feito com sucesso!")

        self.master.destroy()       # Fecha a tela de cadastro
        self.ao_logar_callback()    # Reabre a tela de login

    def voltar_login(self):
        self.ao_logar_callback()  # Chama o callback passado (que destrói e reativa login)
        self.master.destroy()     # Fecha a janela de cadastro

    @staticmethod
    def inserir_funcionario(nome, cpf, cargo, usuario, senha):
        try:
            conexao = mysql.connector.connect(
                host='localhost',       # seu host
                user='emporioDoSabor',     # seu usuário
                password='admin321@s',   # sua senha
                database='lanchonete_db'   # seu banco
            )

            if conexao.is_connected():
                cursor = conexao.cursor()

                sql = """INSERT INTO funcionarios (nome, cpf, cargo, usuario, senha)
                         VALUES (%s, %s, %s, %s, %s)"""

                valores = (nome, cpf, cargo, usuario, senha)  # passe todos os valores correspondentes

                cursor.execute(sql, valores)
                conexao.commit()
                print("Funcionário cadastrado com sucesso!")

        except Error as e:
            print(f"Erro ao conectar/inserir no MySQL: {e}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


# Teste independente da tela
if __name__ == "__main__":
    def ao_logar():
        print("Redirecionando para a próxima tela...")

    root = tk.Tk()
    app = TelaCadastro(root, ao_logar)
    root.mainloop()
