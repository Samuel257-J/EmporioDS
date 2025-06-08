# tela_Cozinheiro.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
from tela_Login import TelaLogin
import tela_PedidosCozinheiro
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk  

class TelaCozinheiro:
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
        self.master.title("COZINHEIRO - Empório do Sabor")
        self.master.geometry("1000x650")
        self.master.resizable(False, False)
        print("TelaCozinheiro aberta")

        # Centralizar janela
        largura_janela = 1000
        altura_janela = 650

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        geometria = f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}"
        self.master.geometry(geometria)
        self.geometria_atual = geometria

        try:
            self.fundo = carregar_imagem_tk("telaCozinheiro.png", (1000, 650))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=1000, height=650, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        # Carregar imagem do botão
        try:
            self.img_ver_pedido = carregar_imagem_tk("ver_Pedido.png", (120, 140))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem do botão de pedido:\n{e}")
            return


        # Botão VER PEDIDOS
        self.botao_ver_pedido = tk.Button(
            self.master,
            text="VER PEDIDOS",
            image=self.img_ver_pedido,
            compound="bottom",
            font=("Arial", 15, "bold"),
            bg="#4E51F6",
            fg="white",
            padx=10,
            pady=20,
            command=self.ver_pedido
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

        # Posicionar botões na tela com canvas
        self.canvas.create_window(500, 325, window=self.botao_ver_pedido, width=250, height=250)
        self.canvas.create_window(90, 580, window=self.botao_sair_conta)
        
        self.tela_pedidos = None
        self.janela_pedidos = None

    def ver_pedido(self):
        # Verificar se já existe uma janela de pedidos aberta
        if self.janela_pedidos and self.janela_pedidos.winfo_exists():
            # Se já existe, apenas traz para frente
            self.janela_pedidos.lift()
            self.janela_pedidos.focus()
        else:
            # Se não existe, cria uma nova
            self.janela_pedidos = tk.Toplevel(self.master)
            self.tela_pedidos = tela_PedidosCozinheiro.TelaPedidosCozinheiro(
                self.janela_pedidos, 
                ao_sair_callback=self.fechar_tela_pedidos
            )

    def fechar_tela_pedidos(self):
        """Callback para quando a tela de pedidos for fechada"""
        if self.janela_pedidos:
            self.janela_pedidos.destroy()
            self.janela_pedidos = None
            self.tela_pedidos = None

    def sair_conta(self):
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            # Fechar tela de pedidos se estiver aberta
            if self.janela_pedidos:
                self.janela_pedidos.destroy()
            self.master.destroy()
            self.ao_sair_callback()

if __name__ == "__main__":
    def voltar_para_login():
        root = tk.Tk()
        TelaLogin(root, voltar_para_login)
        root.mainloop()

    root = tk.Tk()
    TelaCozinheiro(root, voltar_para_login)
    root.mainloop()