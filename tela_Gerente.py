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
    def __init__(self, master, produto_para_editar=None):
        super().__init__(master)
        
        # Armazenar o produto sendo editado
        self.produto_editando = produto_para_editar
        self.modo_edicao = produto_para_editar is not None
        
        # Configurar título baseado no modo
        if self.modo_edicao:
            self.title("Editar Produto")
        else:
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

        # Criar widgets
        self.criar_widgets()
        
        # Se estiver em modo de edição, preencher os campos
        if self.modo_edicao:
            self.preencher_campos_edicao()

    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        y = 60
        
        # Nome do produto
        self.label_nome = tk.Label(self.canvas, text="Nome do Produto:", font=("Arial", 12, "bold"),
                                   fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_nome)
        y += 25

        self.entry_nome = tk.Entry(self.canvas, font=("Arial", 12))
        self.canvas.create_window(200, y, window=self.entry_nome)
        y += 35

        # Categoria
        self.label_categoria = tk.Label(self.canvas, text="Categoria:", font=("Arial", 12, "bold"),
                                        fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_categoria)
        y += 25

        self.combo_categoria = ttk.Combobox(self.canvas, font=("Arial", 12), state="readonly")
        self.combo_categoria['values'] = [
            "Pastel", "Coxinha", "Hambúrguer", "Porção", "Massa", "Bebida", "Sobremesa"
        ]
        self.canvas.create_window(200, y, window=self.combo_categoria)
        y += 35

        # Preço
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

        # Estoque
        self.label_estoque = tk.Label(self.canvas, text="Estoque (quantidade):", font=("Arial", 12, "bold"),
                                      fg="white", bg="#0A0B0A")
        self.canvas.create_window(200, y, window=self.label_estoque)
        y += 25

        self.entry_estoque = tk.Entry(self.canvas, font=("Arial", 12))
        self.canvas.create_window(200, y, window=self.entry_estoque)
        y += 40

        # Botão que muda texto e comando baseado no modo
        texto_botao = "Atualizar" if self.modo_edicao else "Cadastrar"
        cor_botao = "#FF9800" if self.modo_edicao else "#4CAF50"
        
        self.botao_salvar = tk.Button(self.canvas, text=texto_botao, font=("Arial", 12, "bold"),
                                      bg=cor_botao, fg="white", width=15, command=self.salvar_produto)
        self.canvas.create_window(200, 340, window=self.botao_salvar)

    def proteger_prefixo(self, event=None):
        """Protege o prefixo R$ no campo de preço"""
        valor_atual = self.var_preco.get()
        if not valor_atual.startswith("R$"):
            self.var_preco.set("R$" + valor_atual.replace("R$", ""))
            self.entry_preco.icursor(tk.END)

    def preencher_campos_edicao(self):
        """Preenche os campos com os dados do produto sendo editado"""
        if not self.produto_editando:
            return
            
        print(f"Preenchendo campos com produto: {self.produto_editando}")  # Debug
        
        try:
            # Limpar campos primeiro
            self.entry_nome.delete(0, tk.END)
            self.entry_estoque.delete(0, tk.END)
            
            # Assumindo que produto_editando é uma tupla com ordem: (id, nome, preco, categoria, estoque)
            # Ajuste os índices conforme a estrutura real do seu banco de dados
            
            # Preencher nome (índice 1)
            self.entry_nome.insert(0, str(self.produto_editando[1]))
            
            # Selecionar categoria no combobox (índice 3)
            if len(self.produto_editando) > 3 and self.produto_editando[3]:
                self.combo_categoria.set(str(self.produto_editando[3]))
            
            # Preencher preço (índice 2)
            if len(self.produto_editando) > 2:
                preco = self.produto_editando[2]
                try:
                    if preco is None or preco == '':
                        preco_float = 0.0
                    else:
                        preco_float = float(preco)
                    self.var_preco.set(f"R${preco_float:.2f}")
                except (ValueError, TypeError):
                    self.var_preco.set("R$0.00")
            
            # Preencher estoque (índice 4)
            if len(self.produto_editando) > 4:
                self.entry_estoque.insert(0, str(self.produto_editando[4]))
                
        except Exception as e:
            print(f"Erro ao preencher campos: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar dados do produto:\n{e}", parent=self)

    def validar_campos(self):
        """Valida se todos os campos obrigatórios estão preenchidos"""
        # Validar nome
        if not self.entry_nome.get().strip():
            messagebox.showerror("Erro", "O nome do produto é obrigatório!", parent=self)
            return False
        
        # Validar categoria
        if not self.combo_categoria.get():
            messagebox.showerror("Erro", "Selecione uma categoria!", parent=self)
            return False
        
        # Validar preço
        preco_str = self.var_preco.get().replace("R$", "").replace(",", ".")
        try:
            preco = float(preco_str)
            if preco <= 0:
                messagebox.showerror("Erro", "O preço deve ser maior que zero!", parent=self)
                return False
        except ValueError:
            messagebox.showerror("Erro", "Digite um preço válido!", parent=self)
            return False
        
        # Validar estoque
        try:
            estoque = int(self.entry_estoque.get())
            if estoque < 0:
                messagebox.showerror("Erro", "O estoque não pode ser negativo!", parent=self)
                return False
        except ValueError:
            messagebox.showerror("Erro", "Digite uma quantidade válida para o estoque!", parent=self)
            return False
        
        return True

    def salvar_produto(self):
        """Método principal que decide se vai cadastrar ou atualizar"""
        if not self.validar_campos():
            return
        
        if self.modo_edicao:
            self.atualizar_produto()
        else:
            self.cadastrar_produto()

    def cadastrar_produto(self):
        """Cadastra um novo produto"""
        # Obter valores dos campos
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get()
        preco_str = self.var_preco.get().replace("R$", "").replace(",", ".")
        preco = float(preco_str)
        estoque = int(self.entry_estoque.get())
        
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            
            # Verificar se já existe produto com o mesmo nome
            cursor.execute("SELECT id FROM produtos WHERE nome = %s", (nome,))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Já existe um produto com esse nome!", parent=self)
                return
            
            # Inserir novo produto
            query = """
                INSERT INTO produtos (nome, preco, categoria, estoque, ativo)
                VALUES (%s, %s, %s, %s, TRUE)
            """
            valores = (nome, preco, categoria, estoque)
            
            cursor.execute(query, valores)
            conexao.commit()
            
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!", parent=self)
            
            # Limpar campos para novo cadastro
            self.entry_nome.delete(0, tk.END)
            self.combo_categoria.set("")
            self.var_preco.set("R$")
            self.entry_estoque.delete(0, tk.END)
            
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto:\n{e}", parent=self)
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def atualizar_produto(self):
        """Atualiza um produto existente"""
        if not self.produto_editando:
            messagebox.showerror("Erro", "Nenhum produto selecionado para edição!", parent=self)
            return
            
        # Obter valores dos campos
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get()
        preco_str = self.var_preco.get().replace("R$", "").replace(",", ".")
        preco = float(preco_str)
        estoque = int(self.entry_estoque.get())
        
        # Obter ID do produto
        produto_id = self.produto_editando[0]
        
        print(f"Atualizando produto ID: {produto_id}")  # Debug
        print(f"Novos valores: nome={nome}, categoria={categoria}, preco={preco}, estoque={estoque}")  # Debug
        
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            
            # Verificar se já existe outro produto com o mesmo nome (exceto o atual)
            cursor.execute("SELECT id FROM produtos WHERE nome = %s AND id != %s", (nome, produto_id))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Já existe um produto com esse nome!", parent=self)
                return
            
            # Atualizar produto
            query = """
                UPDATE produtos 
                SET nome = %s, preco = %s, categoria = %s, estoque = %s
                WHERE id = %s
            """
            valores = (nome, preco, categoria, estoque, produto_id)
            
            print(f"Executando query: {query}")  # Debug
            print(f"Com valores: {valores}")  # Debug
            
            cursor.execute(query, valores)
            conexao.commit()
            
            print(f"Linhas afetadas: {cursor.rowcount}")  # Debug
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado com sucesso!", parent=self)
                self.destroy()
            else:
                messagebox.showwarning("Aviso", "Nenhuma alteração foi feita. Verifique se o produto existe.", parent=self)
            
        except mysql.connector.Error as e:
            print(f"Erro MySQL: {e}")  # Debug
            messagebox.showerror("Erro", f"Erro ao atualizar produto:\n{e}", parent=self)
            if 'conexao' in locals() and conexao.is_connected():
                conexao.rollback()
        except Exception as e:
            print(f"Erro geral: {e}")  # Debug
            messagebox.showerror("Erro", f"Erro inesperado:\n{e}", parent=self)
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

if __name__ == "__main__":
    def voltar_para_login():
        root = tk.Tk()
        TelaLogin(root, voltar_para_login)
        root.mainloop()

    root = tk.Tk()
    TelaGerente(root, voltar_para_login)
    root.mainloop()