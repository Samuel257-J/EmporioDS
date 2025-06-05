import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
import mysql.connector
from mysql.connector import Error
from tela_Admin import TelaAdmin
import os
from pathlib import Path

class TelaLogin:
    def __init__(self, master, ao_logar_callback=None):  
        self.master = master
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")

        self.ao_logar_callback = ao_logar_callback
        self.master.title("LOGIN - Empório do Sabor")	
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


        script_dir = Path(__file__).parent
        caminho_imagem = script_dir / "ImagensProjeto" / "telaLogin.png"

        try:
            imagem_fundo = Image.open(str(caminho_imagem)).resize((425, 582))
            self.fundo = ImageTk.PhotoImage(imagem_fundo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=425, height=582, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        self.entry_usuario = tk.Entry(self.master, font=("Arial", 14))
        self.entry_senha = tk.Entry(self.master, font=("Arial", 14), show="*")
        self.botao_login = tk.Button(self.master, text="Entrar", font=("Arial", 10, "bold"),
                                     bg="#ebb501", fg="white", cursor="hand2", command=self.fazer_login)
        self.botao_cadastrar = tk.Button(self.master, text="Cadastrar", font=("Arial", 10, "bold"),
                                         bg="#4E51F6", fg="white", cursor="hand2", command=self.abrir_cadastro)
        self.label_esqueceu = tk.Label(self.master, text="Esqueceu a senha?",
                                       font=("Arial", 9), fg="#A6A0A0", bg="#030101", cursor="hand2")
        self.canvas.create_window(167, 463, window=self.label_esqueceu)
        self.label_esqueceu.bind("<Button-1>", self.redefinir_senha)

        
        self.canvas.create_text(137, 355, text="Usuário", font=("Arial", 10, "bold"), fill="white")
        self.canvas.create_text(132, 410, text="Senha", font=("Arial", 10, "bold"), fill="white")

        self.canvas.create_window(212, 380, window=self.entry_usuario, width=200, height=30)
        self.canvas.create_window(212, 435, window=self.entry_senha, width=200, height=30)
        self.canvas.create_window(340, 520, window=self.botao_login, width=100, height=30)
        self.canvas.create_window(230, 520, window=self.botao_cadastrar, width=100, height=30)

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

    # Conta fixa de admin
        USUARIO_ADMIN_FIXO = "admin"
        SENHA_ADMIN_FIXO = "123456"

        if usuario == USUARIO_ADMIN_FIXO and senha == SENHA_ADMIN_FIXO:
            messagebox.showinfo("Login", "Bem-vindo, administrador!")
            self.master.withdraw()  # Esconde a tela de login
            janela_admin = tk.Toplevel(self.master)
        
            def ao_sair_admin():
                janela_admin.destroy()
                self.limpar_campos()
                self.master.deiconify()

            TelaAdmin(janela_admin, ao_sair_admin)  # Garante que a tela admin tenha também uma forma de voltar
            return

        if not usuario or not senha:
            messagebox.showwarning("Campos vazios", "Preencha usuário e senha.")
            return
        
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )

            if conexao.is_connected():
                cursor = conexao.cursor()
                sql = "SELECT * FROM funcionarios WHERE usuario = %s AND senha = %s"
                valores = (usuario, senha)
                cursor.execute(sql, valores)
                resultado = cursor.fetchone()

                if resultado:
                    id, nome, cpf, cargo, usuario, senha = resultado
                    messagebox.showinfo("Login", f"Bem-vindo, {cargo} {nome}!")
                    self.master.withdraw()

                    cargo = cargo.strip().lower()

                    if cargo == "garçom":
                        from tela_Garcom import TelaGarcom
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaGarcom(janela, ao_sair, tela_cozinheiro=None)

                    elif cargo == "atendente":
                        from tela_Atendente import TelaAtendente
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaAtendente(janela, ao_sair)

                    elif cargo == "cozinheiro":
                        from tela_Cozinheiro import TelaCozinheiro
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaCozinheiro(janela, ao_sair)

                    elif cargo == "gerente":
                        from tela_Gerente import TelaGerente
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaGerente(janela, ao_sair)

                    else:
                        messagebox.showerror("Erro", f"Cargo '{cargo}' não reconhecido.")
                        self.master.deiconify()


        except Error as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados:\n{e}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def abrir_cadastro(self):
        def verificar_admin():
            usuario = entry_admin_usuario.get()
            senha = entry_admin_senha.get()

            USUARIO_ADMIN_FIXO = "admin"
            SENHA_ADMIN_FIXO = "123456"

            if usuario == USUARIO_ADMIN_FIXO and senha == SENHA_ADMIN_FIXO:
                messagebox.showinfo("Acesso liberado", "Administrador autenticado.")
                janela_admin_login.destroy()

                from tela_Cadastro import TelaCadastro

                def ao_voltar():
                    self.master.deiconify()
                    self.master.lift()
                    self.master.focus_force()
                    self.master.update_idletasks()

                janela_cadastro = tk.Toplevel(self.master)
                app_cadastro = TelaCadastro(janela_cadastro, ao_voltar)
                janela_cadastro.grab_set()
                self.master.withdraw()

            else:
                messagebox.showerror("Acesso negado", "Usuário ou senha do administrador incorretos.")

        # Criar janela de autenticação de admin
        janela_admin_login = tk.Toplevel(self.master)
        janela_admin_login.title("Autenticação do Administrador")
        janela_admin_login.geometry("300x180")
        janela_admin_login.resizable(False, False)
        janela_admin_login.grab_set()

        # Centralizar na tela
        largura_janela = 300
        altura_janela = 180
        largura_tela = janela_admin_login.winfo_screenwidth()
        altura_tela = janela_admin_login.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_admin_login.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        tk.Label(janela_admin_login, text="Usuário Admin:").pack(pady=(10, 0))
        entry_admin_usuario = tk.Entry(janela_admin_login)
        entry_admin_usuario.pack()

        tk.Label(janela_admin_login, text="Senha Admin:").pack(pady=(10, 0))
        entry_admin_senha = tk.Entry(janela_admin_login, show="*")
        entry_admin_senha.pack()

        tk.Button(janela_admin_login, text="Autenticar", bg="#47AF06", fg="white",
                  font=("Arial", 10, "bold"), command=verificar_admin).pack(pady=15)

        self.master.withdraw()

    def redefinir_senha(self, event):
        messagebox.showinfo("Redefinir senha", "Função de redefinir senha será implementada aqui.")

    def limpar_campos(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app_login = TelaLogin(root)
    root.mainloop()

