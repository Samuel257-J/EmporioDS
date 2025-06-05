import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk  

class TelaGerenciarEstoque(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")
        self.title("Gerenciar Estoque")
        self.geometry("700x400")
        self.resizable(False, False)

        # Centralizar janela
        largura_janela = 700
        altura_janela = 400
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        try:
            self.fundo = carregar_imagem_tk("telaGerenciarEstoque.png", (700, 400))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.destroy()
            return

        self.canvas = tk.Canvas(self, width=700, height=400, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        self.produtos = []
        self.produto_selecionado = None

        # --- Widgets sobre canvas ---
        self.label_filtro = tk.Label(self.canvas, text="Filtrar por nome:", font=("Arial", 12, "bold"), fg="white", bg="#0A0B0A")
        self.canvas.create_window(30, 85, window=self.label_filtro, anchor="nw")

        self.entry_filtro = tk.Entry(self.canvas, font=("Arial", 12))
        self.canvas.create_window(170, 86, window=self.entry_filtro, anchor="nw")
        self.entry_filtro.bind("<KeyRelease>", self.filtrar_produtos)

        # Frame que vai conter a Listbox e a Scrollbar
        frame_lista = tk.Frame(self.canvas, bg="#0A0B0A")
        self.canvas.create_window(30, 120, window=frame_lista, anchor="nw")

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.lista_produtos = tk.Listbox(frame_lista, font=("Arial", 12), width=35, height=12, yscrollcommand=scrollbar.set)
        self.lista_produtos.pack(side=tk.LEFT, fill=tk.BOTH)

        # Conecta Scrollbar com Listbox
        scrollbar.config(command=self.lista_produtos.yview)

        # Evento de seleção
        self.lista_produtos.bind("<<ListboxSelect>>", self.selecionar_produto)

        # Frame detalhes como container invisível
        self.frame_detalhes = tk.Frame(self.canvas, bg="#050505")
        self.canvas.create_window(410, 120, window=self.frame_detalhes, anchor="nw")

        caixa_info = tk.Frame(self.frame_detalhes, bd=2, relief=tk.GROOVE, padx=10, pady=10, bg="#050505", width=250, height=100)
        caixa_info.pack_propagate(False)
        caixa_info.pack(pady=(0, 10))

        self.label_nome = tk.Label(caixa_info, text="Nome: ", font=("Arial", 13, "bold"), fg="white", bg="#050505", anchor="w", width=25)
        self.label_nome.pack(anchor="w", pady=(0, 5))

        frame_estoque = tk.Frame(caixa_info, bg="#050505")
        frame_estoque.pack(anchor="w", pady=(0, 5))

        tk.Label(frame_estoque, text="Estoque:", font=("Arial", 13, "bold"), fg="white", bg="#050505").pack(side=tk.LEFT)

        self.entry_estoque = tk.Entry(frame_estoque, font=("Arial", 13), width=10)
        self.entry_estoque.pack(side=tk.LEFT, padx=5)
        self.entry_estoque.config(validate="key", validatecommand=(self.register(self.validar_numeros), "%P"))

        # Frame fixo para os botões + e -
        frame_botoes = tk.Frame(self.frame_detalhes, bg="#050505", width=150, height=70)
        frame_botoes.pack_propagate(False)
        frame_botoes.pack(pady=5)

        try:
            img_mais = carregar_imagem_tk("mais_Estoque.png", (60, 60))
            img_menos = carregar_imagem_tk("menos_Estoque.png", (60, 60))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagens dos botões de estoque:\n{e}")
            return

        self.botao_mais = tk.Button(frame_botoes, image=img_mais, command=self.aumentar_estoque, bd=0, bg="#050505", width=60, height=60)
        self.botao_menos = tk.Button(frame_botoes, image=img_menos, command=self.diminuir_estoque, bd=0, bg="#050505", width=60, height=60)
        self.botao_mais.image = img_mais
        self.botao_menos.image = img_menos
        self.botao_menos.pack(side=tk.LEFT, padx=5)
        self.botao_mais.pack(side=tk.LEFT, padx=5)

        # Botão confirmar com tamanho fixo
        self.botao_confirmar = tk.Button(self.frame_detalhes, text="Confirmar", font=("Arial", 12), bg="green", fg="white", command=self.confirmar_estoque, width=20, height=1)
        self.botao_confirmar.pack(pady=5)

        self.estoque_temp = None
        self.carregar_produtos()

    def carregar_produtos(self):
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, estoque FROM produtos ORDER BY estoque ASC")
            self.produtos = cursor.fetchall()
            self.atualizar_lista()
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def atualizar_lista(self, filtro=""):
        self.lista_produtos.delete(0, tk.END)
        
        # Índice para controlar a posição na lista
        index = 0
        
        for produto in self.produtos:
            nome, estoque = produto[1], produto[2]
            if nome.lower().startswith(filtro.lower()):
                # Adiciona o item na lista
                self.lista_produtos.insert(tk.END, f"{nome} - Estoque: {estoque}")
                
                # Se o estoque for <= 10, muda a cor de fundo para vermelho
                if estoque <= 10:
                    self.lista_produtos.itemconfig(index, {'bg': '#FF4444', 'fg': 'white'})
                else:
                    # Restaura a cor padrão para itens com estoque normal
                    self.lista_produtos.itemconfig(index, {'bg': 'white', 'fg': 'black'})
                
                index += 1

    def filtrar_produtos(self, event=None):
        filtro = self.entry_filtro.get()
        self.atualizar_lista(filtro)

    def selecionar_produto(self, event):
        selecao = self.lista_produtos.curselection()
        if selecao:
            index = selecao[0]
            nome_filtrado = self.entry_filtro.get().lower()
            produtos_visiveis = [p for p in self.produtos if p[1].lower().startswith(nome_filtrado)]
            self.produto_selecionado = produtos_visiveis[index]
            self.estoque_temp = None
            self.label_nome.config(text=f"Nome: {self.produto_selecionado[1][:40]}")  # corta o nome se for muito grande
            self.entry_estoque.delete(0, tk.END)
            self.entry_estoque.insert(0, str(self.produto_selecionado[2]))

    def atualizar_estoque_no_banco(self, novo_estoque):
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            cursor.execute("UPDATE produtos SET estoque = %s WHERE id = %s", (novo_estoque, self.produto_selecionado[0]))
            conexao.commit()
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estoque: {e}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def aumentar_estoque(self):
        if self.produto_selecionado:
            if self.estoque_temp is None:
                self.estoque_temp = self.produto_selecionado[2]
            self.estoque_temp += 10
            self.entry_estoque.delete(0, tk.END)
            self.entry_estoque.insert(0, str(self.estoque_temp))

    def diminuir_estoque(self):
        if self.produto_selecionado:
            if self.estoque_temp is None:
                self.estoque_temp = self.produto_selecionado[2]
            self.estoque_temp = max(0, self.estoque_temp - 10)
            self.entry_estoque.delete(0, tk.END)
            self.entry_estoque.insert(0, str(self.estoque_temp))

    def confirmar_estoque(self):
        if self.produto_selecionado:
            valor_digitado = self.entry_estoque.get()
            if not valor_digitado.isdigit():
                messagebox.showwarning("Entrada inválida", "Digite um valor numérico válido para o estoque.", parent=self)
                return
            estoque_final = int(valor_digitado)

            resposta = messagebox.askyesno(
                "Confirmar Alteração",
                f"Deseja realmente atualizar o estoque para {estoque_final}?",
                icon='warning',
                parent=self
            )
            if resposta:
                self.atualizar_estoque_no_banco(estoque_final)
                self.produto_selecionado = (self.produto_selecionado[0], self.produto_selecionado[1], estoque_final)
                self.estoque_temp = None
                messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso.", parent=self)
                self.entry_estoque.delete(0, tk.END)
                self.entry_estoque.insert(0, str(estoque_final))
                self.carregar_produtos()

    def validar_numeros(self, valor):
        return valor.isdigit() or valor == ""

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = TelaGerenciarEstoque(root)
    app.mainloop()