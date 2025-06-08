import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk
import re

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
        
        # Variável para controlar visibilidade da senha
        self.senha_visivel = False
        
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
        
        # Bind para formatação automática do CPF
        self.entry_cpf.bind('<KeyRelease>', self.formatar_cpf)

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
        self.entry_senha.place(x=112, y=440, width=170, height=28)  # Reduzida largura para dar espaço ao botão
        
        # Botão para mostrar/ocultar senha
        self.botao_mostrar_senha = tk.Button(
            self.master,
            text="👁",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="black",
            command=self.alternar_visibilidade_senha,
            width=2,
            height=1
        )
        self.botao_mostrar_senha.place(x=287, y=440, width=25, height=28)

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

    def alternar_visibilidade_senha(self):
        """Alterna entre mostrar e ocultar a senha"""
        if self.senha_visivel:
            # Ocultar senha
            self.entry_senha.config(show="*")
            self.botao_mostrar_senha.config(text="👁")
            self.senha_visivel = False
        else:
            # Mostrar senha
            self.entry_senha.config(show="")
            self.botao_mostrar_senha.config(text="🙈")
            self.senha_visivel = True

    def formatar_cpf(self, event):
        """Formata o CPF automaticamente enquanto o usuário digita"""
        cpf = self.entry_cpf.get()
        # Remove tudo que não é número
        cpf = re.sub(r'\D', '', cpf)
        
        # Limita a 11 dígitos
        cpf = cpf[:11]
        
        # Aplica a formatação
        if len(cpf) > 9:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        elif len(cpf) > 6:
            cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
        elif len(cpf) > 3:
            cpf = f"{cpf[:3]}.{cpf[3:]}"
        
        # Atualiza o campo
        cursor_pos = self.entry_cpf.index(tk.INSERT)
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, cpf)
        
        # Ajusta a posição do cursor
        if cursor_pos <= len(cpf):
            self.entry_cpf.icursor(cursor_pos)

    def validar_cpf(self, cpf):
        """Valida se o CPF é válido usando o algoritmo oficial"""
        # Remove formatação
        cpf = re.sub(r'\D', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais (CPFs inválidos)
        if cpf == cpf[0] * 11:
            return False
        
        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[10]) != digito2:
            return False
        
        return True

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        cargo = self.cargo_var.get()
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        # Validação simples
        if not nome or not cpf or not usuario or not senha:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        # Validação do CPF
        if not self.validar_cpf(cpf):
            messagebox.showerror("CPF Inválido", "Por favor, digite um CPF válido.")
            self.entry_cpf.focus_set()  # Foca no campo CPF
            return

        # Validação adicional do nome (apenas letras e espaços)
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            messagebox.showerror("Nome Inválido", "O nome deve conter apenas letras e espaços.")
            self.entry_nome.focus_set()
            return

        # Validação do usuário (sem espaços e caracteres especiais)
        if not re.match( '^[a-zA-Z0-9_]+$', usuario):
            messagebox.showerror("Usuário Inválido", "O usuário deve conter apenas letras, números e underscore.")
            self.entry_usuario.focus_set()
            return

        # Validação da senha (mínimo 6 caracteres)
        if len(senha) < 6:
            messagebox.showerror("Senha Inválida", "A senha deve ter pelo menos 6 caracteres.")
            self.entry_senha.focus_set()
            return

        # Remove formatação do CPF antes de salvar no banco
        cpf_limpo = re.sub(r'\D', '', cpf)

        try:
            self.inserir_funcionario(nome, cpf_limpo, cargo, usuario, senha)
            messagebox.showinfo("Cadastro realizado", "Cadastro feito com sucesso!")
            self.master.destroy()       # Fecha a tela de cadastro
            self.ao_logar_callback()    # Reabre a tela de login
        except Exception as e:
            messagebox.showerror("Erro no cadastro", f"Erro ao cadastrar usuário:\n{e}")

    def voltar_login(self):
        self.ao_logar_callback()  # Chama o callback passado (que destrói e reativa login)
        self.master.destroy()     # Fecha a janela de cadastro

    @staticmethod
    def inserir_funcionario(nome, cpf, cargo, usuario, senha):
        try:
            conexao = mysql.connector.connect(
                host='localhost',    
                user='emporioDoSabor',     
                password='admin321@s',   
                database='lanchonete_db'   
            )

            if conexao.is_connected():
                cursor = conexao.cursor()

                # Verifica se o CPF já existe
                cursor.execute("SELECT id FROM funcionarios WHERE cpf = %s", (cpf,))
                if cursor.fetchone():
                    raise Exception("CPF já cadastrado no sistema!")

                # Verifica se o usuário já existe
                cursor.execute("SELECT id FROM funcionarios WHERE usuario = %s", (usuario,))
                if cursor.fetchone():
                    raise Exception("Nome de usuário já existe!")

                sql = """INSERT INTO funcionarios (nome, cpf, cargo, usuario, senha)
                         VALUES (%s, %s, %s, %s, %s)"""

                valores = (nome, cpf, cargo, usuario, senha) 

                cursor.execute(sql, valores)
                conexao.commit()
                print("Funcionário cadastrado com sucesso!")

        except Error as e:
            raise Exception(f"Erro ao conectar/inserir no MySQL: {e}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

if __name__ == "__main__":
    def ao_logar():
        print("Redirecionando para a próxima tela...")

    root = tk.Tk()
    app = TelaCadastro(root, ao_logar)
    root.mainloop()