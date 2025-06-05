import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk

class TelaAdmin:
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
        self.master.title("ADMINISTRADOR - Empório do Sabor")
        self.master.geometry("1000x650")
        self.master.resizable(False, False)
        print("TelaAdmin aberta")

        # Centralizar janela na tela
        largura_janela = 1000
        altura_janela = 650
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Carregar imagem de fundo
        script_dir = Path(__file__).parent
        caminho_imagem = script_dir / "ImagensProjeto" / "telaAdmin.png"
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

        try:
            self.img_botao1 = carregar_imagem_tk("cadastrar_Funcionario.png", (120, 120))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem do botão:\n{e}")
            return

        try:
            self.img_botao2 = carregar_imagem_tk("ver_Relatorio.png", (120, 120))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem do botão:\n{e}")
            return

        # Botões
        self.botao_cadastrar_funcionario = tk.Button(
            self.master,
            text="CADASTRAR FUNCIONÁRIO",
            image=self.img_botao1,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#4E51F6",
            fg="white",
            padx=10,
            pady=20,
            command=self.abrir_cadastro
        )

        self.botao_ver_relatorio = tk.Button(
            self.master,
            text="VER RELATÓRIO",
            image=self.img_botao2,
            compound="bottom",
            font=("Arial", 12, "bold"),
            bg="#E47A01",
            fg="white",
            padx=10,
            pady=20,
            command=self.abrir_relatorio
        )

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

        self.canvas.create_window(340, 340, window=self.botao_cadastrar_funcionario, width=250, height=250)
        self.canvas.create_window(650, 340, window=self.botao_ver_relatorio, width=250, height=250)
        self.canvas.create_window(90, 580, window=self.botao_sair_conta)

    def abrir_cadastro(self):
        try:
            from tela_Cadastro import TelaCadastro
        except ImportError:
            messagebox.showerror("Erro", "Não foi possível importar TelaCadastro.")
            return

        def ao_voltar():
            self.master.deiconify()
            self.master.lift()
            self.master.focus_force()
            self.master.update_idletasks()

        janela_cadastro = tk.Toplevel(self.master)
        app_cadastro = TelaCadastro(janela_cadastro, ao_voltar)
        janela_cadastro.grab_set()
        self.master.withdraw()

    def abrir_relatorio(self):
        print("Aqui irá abrir o relatório")
        # Aqui você implementará a tela_Relatorio mais tarde

    def sair_conta(self):
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.master.destroy()
            self.ao_sair_callback()

# Execução de teste
def ao_sair():
    print("Saindo da tela de administrador")

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaAdmin(root, ao_sair)
    root.mainloop()
