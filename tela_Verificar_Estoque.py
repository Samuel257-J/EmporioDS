import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk

class TelaVerificarEstoque(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")
        
        self.title("Verificar Estoque - Atendente")
        self.geometry("800x600")
        self.resizable(False, False)

        # Centralizar janela
        largura_janela = 800
        altura_janela = 600
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Configurar estilo moderno
        self.configure(bg="#f5f7fa")
        
        # Inicializar variáveis
        self.produtos = []
        
        # Criar interface primeiro
        self.criar_interface()
        
        # Depois carregar produtos
        self.carregar_produtos()

    def criar_interface(self):
        # Container principal com scroll se necessário
        self.main_frame = tk.Frame(self, bg="#f5f7fa")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header simples
        header_frame = tk.Frame(self.main_frame, bg="#6c5ce7", height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="📦 VERIFICAR ESTOQUE", 
                              font=("Arial", 18, "bold"), bg="#6c5ce7", fg="white")
        title_label.pack(expand=True)

        # Frame de busca
        search_frame = tk.Frame(self.main_frame, bg="white", relief="ridge", bd=1)
        search_frame.pack(fill="x", pady=(0, 10), padx=5)

        tk.Label(search_frame, text="Buscar Produto:", font=("Arial", 12, "bold"), 
                bg="white").pack(anchor="w", padx=10, pady=(10, 5))

        self.entry_busca = tk.Entry(search_frame, font=("Arial", 12), width=50)
        self.entry_busca.pack(anchor="w", padx=10, pady=(0, 10))
        self.entry_busca.bind("<KeyRelease>", self.filtrar_produtos)

        # Frame principal para lista e detalhes
        content_frame = tk.Frame(self.main_frame, bg="#f5f7fa")
        content_frame.pack(fill="both", expand=True)

        # Frame da lista (lado esquerdo)
        list_frame = tk.Frame(content_frame, bg="white", relief="ridge", bd=1)
        list_frame.pack(side="left", fill="both", expand=True, padx=(5, 5))

        tk.Label(list_frame, text="Lista de Produtos", font=("Arial", 12, "bold"), 
                bg="white").pack(pady=10)

        # Container para treeview e scrollbar
        tree_container = tk.Frame(list_frame, bg="white")
        tree_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Treeview para produtos
        columns = ("Produto", "Estoque", "Status")
        self.tree_produtos = ttk.Treeview(tree_container, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.tree_produtos.heading("Produto", text="Produto")
        self.tree_produtos.heading("Estoque", text="Estoque")
        self.tree_produtos.heading("Status", text="Status")
        
        self.tree_produtos.column("Produto", width=200)
        self.tree_produtos.column("Estoque", width=80, anchor="center")
        self.tree_produtos.column("Status", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)

        self.tree_produtos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind para seleção
        self.tree_produtos.bind("<<TreeviewSelect>>", self.mostrar_detalhes)

        # Frame de detalhes (lado direito)
        details_frame = tk.Frame(content_frame, bg="white", relief="ridge", bd=1, width=280)
        details_frame.pack(side="right", fill="y", padx=(5, 5))
        details_frame.pack_propagate(False)

        tk.Label(details_frame, text="Detalhes do Produto", font=("Arial", 12, "bold"), 
                bg="white").pack(pady=10)

        # Container para detalhes
        self.details_container = tk.Frame(details_frame, bg="white")
        self.details_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Mensagem inicial
        self.criar_detalhes_iniciais()

        # Botão fechar
        btn_frame = tk.Frame(self.main_frame, bg="#f5f7fa")
        btn_frame.pack(fill="x", pady=10)

        btn_fechar = tk.Button(btn_frame, text="Fechar", font=("Arial", 12, "bold"),
                              bg="#e74c3c", fg="white", width=15, command=self.destroy)
        btn_fechar.pack()

    def criar_detalhes_iniciais(self):
        """Cria a mensagem inicial dos detalhes"""
        tk.Label(self.details_container, text="📦", font=("Arial", 36), bg="white").pack(pady=20)
        tk.Label(self.details_container, text="Selecione um produto\npara ver os detalhes",
                font=("Arial", 11), bg="white", fg="#636e72", justify="center").pack()

    def mostrar_detalhes(self, event):
        """Mostra detalhes do produto selecionado"""
        selection = self.tree_produtos.selection()
        if not selection:
            return

        item = self.tree_produtos.item(selection[0])
        produto_nome = item['values'][0]
        
        # Encontrar produto nos dados
        produto_data = None
        for produto in self.produtos:
            if produto[1] == produto_nome:
                produto_data = produto
                break
        
        if not produto_data:
            return

        # Limpar detalhes atuais
        for widget in self.details_container.winfo_children():
            widget.destroy()

        id_produto, nome, estoque, preco = produto_data
        
        # Ícone baseado no estoque
        if estoque <= 5:
            icon = "⚠️"
            icon_color = "#e74c3c"
        elif estoque <= 15:
            icon = "📦"
            icon_color = "#f39c12"
        else:
            icon = "✅"
            icon_color = "#27ae60"
            
        tk.Label(self.details_container, text=icon, font=("Arial", 32), 
                bg="white", fg=icon_color).pack(pady=10)

        # Nome do produto
        tk.Label(self.details_container, text=nome, font=("Arial", 12, "bold"), 
                bg="white", fg="#2d3436", wraplength=250).pack(pady=5)

        # Separador
        separator = tk.Frame(self.details_container, height=2, bg="#f0f0f0")
        separator.pack(fill="x", padx=20, pady=10)

        # Informações
        info_frame = tk.Frame(self.details_container, bg="white")
        info_frame.pack(fill="x", padx=10)

        tk.Label(info_frame, text="Estoque Atual:", font=("Arial", 10, "bold"), 
                bg="white", fg="#636e72").pack(anchor="w")
        tk.Label(info_frame, text=f"{estoque} unidades", font=("Arial", 12), 
                bg="white", fg="#2d3436").pack(anchor="w", pady=(0, 10))

        tk.Label(info_frame, text="Preço Unitário:", font=("Arial", 10, "bold"), 
                bg="white", fg="#636e72").pack(anchor="w")
        tk.Label(info_frame, text=f"R$ {preco:.2f}", font=("Arial", 12), 
                bg="white", fg="#2d3436").pack(anchor="w", pady=(0, 10))

        tk.Label(info_frame, text="Valor Total em Estoque:", font=("Arial", 10, "bold"), 
                bg="white", fg="#636e72").pack(anchor="w")
        tk.Label(info_frame, text=f"R$ {estoque * preco:.2f}", font=("Arial", 12), 
                bg="white", fg="#2d3436").pack(anchor="w", pady=(0, 10))

        # Status
        if estoque <= 5:
            status_text = "ESTOQUE CRÍTICO"
            status_color = "#e74c3c"
        elif estoque <= 15:
            status_text = "ESTOQUE BAIXO"
            status_color = "#f39c12"
        else:
            status_text = "ESTOQUE OK"
            status_color = "#27ae60"
            
        status_label = tk.Label(self.details_container, text=status_text, 
                               font=("Arial", 10, "bold"), bg=status_color, fg="white", 
                               padx=10, pady=5)
        status_label.pack(pady=10)

    def carregar_produtos(self):
        """Carrega produtos do banco de dados"""
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, estoque, preco FROM produtos ORDER BY estoque ASC")
            self.produtos = cursor.fetchall()
            print(f"Produtos carregados: {len(self.produtos)}")
            self.atualizar_lista()
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def atualizar_lista(self, filtro=""):
        """Atualiza a lista de produtos com filtro opcional"""
        # Limpar lista atual
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        for produto in self.produtos:
            id_produto, nome, estoque, preco = produto
            if filtro.lower() in nome.lower() or filtro == "":
                if estoque <= 5:
                    status = "CRÍTICO"
                    tag = "critico"
                elif estoque <= 15:
                    status = "BAIXO"
                    tag = "baixo"
                else:
                    status = "OK"
                    tag = "ok"
                
                self.tree_produtos.insert("", "end", values=(nome, estoque, status), tags=(tag,))

        # Configurar cores das tags
        self.tree_produtos.tag_configure("critico", background="#ffebee", foreground="#c62828")
        self.tree_produtos.tag_configure("baixo", background="#fff3e0", foreground="#ef6c00")
        self.tree_produtos.tag_configure("ok", background="#e8f5e8", foreground="#2e7d32")

    def filtrar_produtos(self, event=None):
        """Filtra produtos conforme digitação"""
        busca = self.entry_busca.get()
        self.atualizar_lista(busca)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = TelaVerificarEstoque(root)
    app.mainloop()