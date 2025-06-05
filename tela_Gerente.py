import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
from tela_Login import TelaLogin
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tela_Gerenciar_Estoque import TelaGerenciarEstoque
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk

class TelaGerente:
    def __init__(self, master, ao_sair_callback):
        self.master = master
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")
        self.ao_sair_callback = ao_sair_callback
        self.master.title("GERENTE - Empório do Sabor")
        self.master.geometry("1000x650")
        self.master.resizable(False, False)
        print("TelaGerente aberta")

        # Centralizar janela
        largura_janela = 1000
        altura_janela = 650

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        try:
            self.fundo = carregar_imagem_tk("telaGerente.png", (1000, 650))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=1000, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        try:
            self.img_cadastrar_produto = carregar_imagem_tk("cadastrar_Produto.png", (150, 150))
            self.img_gerenciar_estoque = carregar_imagem_tk("gerenciar_Estoque.png", (150, 150))
            self.img_ver_relatorio = carregar_imagem_tk("ver_Relatorio.png", (150, 150))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagens dos botões:\n{e}")
            return

        # Botões
        self.botao_cadastrar_produto = tk.Button(
            self.master,
            text="CADASTRAR PRODUTO",
            image=self.img_cadastrar_produto,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#4E51F6",
            fg="white",
            padx=10,
            pady=20,
            command=self.cadastrar_produto
        )

        self.botao_gerenciar_estoque = tk.Button(
            self.master,
            text="GERENCIAR ESTOQUE",
            image=self.img_gerenciar_estoque,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#F6A503",
            fg="white",
            padx=10,
            pady=20,
            command=self.gerenciar_estoque
        )

        self.botao_ver_relatorio = tk.Button(
            self.master,
            text="VER RELATÓRIOS",
            image=self.img_ver_relatorio,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#47AF06",
            fg="white",
            padx=10,
            pady=20,
            command=self.ver_relatorio
        )

        # Posicionamento dos botões no canvas (horizontal)
        self.canvas.create_window(230, 330, window=self.botao_cadastrar_produto, width=250, height=250)
        self.canvas.create_window(500, 330, window=self.botao_gerenciar_estoque, width=250, height=250)
        self.canvas.create_window(770, 330, window=self.botao_ver_relatorio, width=250, height=250)

        # Botão sair
        self.botao_sair_conta = tk.Button(
            self.master,
            text="Sair",
            font=("Arial", 10, "bold"),
            bg="#CE0707",
            fg="white",
            width=14,
            height=2,
            command=self.sair_conta
        )
        self.canvas.create_window(90, 580, window=self.botao_sair_conta)

    # Funções de ação dos botões
    def cadastrar_produto(self):
        TelaCadastroProduto(self.master)

    def gerenciar_estoque(self):
        TelaGerenciarEstoque(self.master)

    def ver_relatorio(self):
        from tela_Ver_Relatorio import TelaVerRelatorioModerna
        nova_janela = TelaVerRelatorioModerna(master=tk._default_root)

    def sair_conta(self):
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.master.destroy()
            self.ao_sair_callback()

class TelaCadastroProduto(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Produto")
        self.geometry("400x400")
        self.resizable(False, False)

        # Centralizar janela
        largura_janela = 400
        altura_janela = 400
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        try:
            self.fundo = carregar_imagem_tk("telaCadastroProduto.png", (400, 400))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.destroy()
            return

        # Canvas com imagem de fundo
        self.canvas = tk.Canvas(self, width=400, height=400, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        # Widgets sobre o canvas
        y = 60
        self.label_nome = tk.Label(self.canvas, text="Nome do Produto:", font=("Arial", 12, "bold"),
                                   fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_nome)
        y += 25

        self.entry_nome = tk.Entry(self.canvas, font=("Arial", 12))
        self.canvas.create_window(200, y, window=self.entry_nome)
        y += 35

        self.label_categoria = tk.Label(self.canvas, text="Categoria:", font=("Arial", 12, "bold"),
                                        fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_categoria)
        y += 25

        self.combo_categoria = ttk.Combobox(self.canvas, font=("Arial", 12), state="readonly")
        self.combo_categoria['values'] = [
            "Pastel", "Coxinha", "Empada",
            "Hambúrguer", "Porções", "Bebidas", "Sobremesa"
        ]
        self.canvas.create_window(200, y, window=self.combo_categoria)
        y += 35

        self.label_preco = tk.Label(self.canvas, text="Preço:", font=("Arial", 12, "bold"),
                                    fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_preco)
        y += 25

        self.var_preco = tk.StringVar()
        self.var_preco.set("R$")
        self.entry_preco = tk.Entry(self.canvas, font=("Arial", 12), textvariable=self.var_preco)
        self.entry_preco.icursor(tk.END)
        self.entry_preco.bind("<KeyRelease>", self.proteger_prefixo)
        self.canvas.create_window(200, y, window=self.entry_preco)
        y += 35

        self.label_estoque = tk.Label(self.canvas, text="Estoque (quantidade):", font=("Arial", 12, "bold"),
                                      fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_estoque)
        y += 25

        self.entry_estoque = tk.Entry(self.canvas, font=("Arial", 12))
        self.canvas.create_window(200, y, window=self.entry_estoque)
        y += 40

        self.botao_cadastrar = tk.Button(self.canvas, text="Cadastrar", font=("Arial", 12, "bold"),
                                         bg="#4CAF50", fg="white", width=15, command=self.salvar_produto)
        self.canvas.create_window(200, 340, window=self.botao_cadastrar)


    def salvar_produto(self):
        nome = self.entry_nome.get()
        categoria = self.combo_categoria.get()
        preco = self.entry_preco.get().replace("R$", "").replace(",", ".").strip()
        estoque = self.entry_estoque.get()

        if not nome or not categoria or not preco.strip("R$") or not estoque:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            preco_float = float(preco)
            estoque_int = int(estoque)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser numérico e estoque deve ser inteiro.")
            return

        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO produtos (nome, categoria, preco, estoque)
                VALUES (%s, %s, %s, %s)
            """, (nome, categoria, preco_float, estoque_int))
            conexao.commit()

            messagebox.showinfo("Produto Cadastrado", f"{nome} foi cadastrado com sucesso!")
            self.destroy()

        except Error as e:
            messagebox.showerror("Erro ao cadastrar", f"Erro: {e}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def proteger_prefixo(self, event=None):
        texto = self.var_preco.get()
        if not texto.startswith("R$"):
            texto = "R$" + texto.lstrip("R$")
        parte_numerica = ''.join(c for c in texto[2:] if c.isdigit() or c == ',')
        self.var_preco.set("R$" + parte_numerica)
        if self.entry_preco.index(tk.INSERT) < 2:
            self.entry_preco.icursor(2)

if __name__ == "__main__":
    def voltar_para_login():
        root = tk.Tk()
        TelaLogin(root, voltar_para_login)
        root.mainloop()

    root = tk.Tk()
    TelaGerente(root, voltar_para_login)
    root.mainloop()