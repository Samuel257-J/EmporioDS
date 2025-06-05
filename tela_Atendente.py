import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
from tela_Login import TelaLogin
from tela_Cadastro_Cliente import TelaCadastroCliente
from tela_Pedido_Viagem import TelaPedidoViagem  # Nova importação
from tela_Verificar_Estoque import TelaVerificarEstoque  # Nova importação
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk

class TelaAtendente:
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
        self.master.title("ATENDENTE - Empório do Sabor")
        self.master.geometry("1000x650")
        self.master.resizable(False, False)
        print("TelaAtendente aberta")
        
        # Centralizar janela
        largura_janela = 1000
        altura_janela = 650

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Carregar imagem de fundo
        script_dir = Path(__file__).parent
        caminho_imagem = script_dir / "ImagensProjeto" / "telaAtendente.png"

        try:
            imagem_fundo = Image.open(str(caminho_imagem)).resize((1000, 650))
            self.fundo = ImageTk.PhotoImage(imagem_fundo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=1000, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        # Carregar imagens dos botões
        try:
            self.img_fazer_pedido = carregar_imagem_tk("fazer_Pedido.png", (150, 150))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem 'fazer_Pedido.png':\n{e}")
            return

        try:
            self.img_cadastrar_cliente = carregar_imagem_tk("cadastrar_Cliente.png", (140, 140))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem 'cadastrar_Cliente.png':\n{e}")
            return

        try:
            self.img_estoque = carregar_imagem_tk("buscar_Produto.png", (150, 150))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem 'buscar_Produto.png':\n{e}")
            return

        # Botão Ver Pedidos
        self.botao_fazer_pedido = tk.Button(
            self.master,
            text="PEDIDO PARA VIAGEM",
            image=self.img_fazer_pedido,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#47AF06",
            fg="white",
            padx=10,
            pady=10,
            command=self.fazer_pedido
        )

        # Botão Cadastrar Cliente
        self.botao_cadastrar_cliente = tk.Button(
            self.master,
            text="CADASTRAR CLIENTE",
            image=self.img_cadastrar_cliente,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#4E51F6",
            fg="white",
            padx=10,
            pady=18,
            command=self.cadastrar_cliente
        )

        # Botão Verificar Estoque
        self.botao_estoque = tk.Button(
            self.master,
            text="VERIFICAR ESTOQUE",
            image=self.img_estoque,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#F6A503",
            fg="white",
            padx=10,
            pady=10,
            command=self.verificar_estoque
        )

        # Botão Sair
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

        # Posicionar os botões
        self.canvas.create_window(210, 340, window=self.botao_fazer_pedido, width=250, height=250)
        self.canvas.create_window(500, 340, window=self.botao_cadastrar_cliente, width=250, height=250)
        self.canvas.create_window(790, 340, window=self.botao_estoque, width=250, height=250)
        self.canvas.create_window(90, 580, window=self.botao_sair_conta)

    def fazer_pedido(self):
        """Abre a tela de pedido para viagem"""
        try:
            TelaPedidoViagem(self.master)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de pedido:\n{e}")

    def cadastrar_cliente(self):
        """Abre a tela de cadastro de cliente"""
        try:
            nova_janela = tk.Toplevel(self.master)
            TelaCadastroCliente(nova_janela)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de cadastro:\n{e}")

    def verificar_estoque(self):
        """Abre a tela de verificação de estoque"""
        try:
            TelaVerificarEstoque(self.master)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir tela de estoque:\n{e}")

    def sair_conta(self):
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.master.destroy()
            self.ao_sair_callback()


if __name__ == "__main__":
    def voltar_para_login():
        root = tk.Tk()
        TelaLogin(root, voltar_para_login)
        root.mainloop()

    root = tk.Tk()
    TelaAtendente(root, voltar_para_login)
    root.mainloop()