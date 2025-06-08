import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk

class TelaPedidoViagem(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.iconphoto(False, icone)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o ícone: {e}")
            
        self.conn = mysql.connector.connect(
            host="localhost",
            user="emporioDoSabor",
            password="admin321@s",
            database="lanchonete_db"
        )
        
        self.title("Pedido para Viagem - Empório do Sabor")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.minsize(1000, 600)

        # Centralizar janela
        largura_janela = 1220
        altura_janela = 730
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Configurar estilo moderno
        self.configure(bg="#f8fafc")
        
        # Variáveis
        self.produtos = []
        self.itens_pedido = []
        self.total_pedido = 0.0
        self.numero_pedido = self.gerar_numero_pedido()
        
        # Variáveis para autocompletar
        self.clientes_cadastrados = []
        self.listbox_sugestoes = None
        self.sugestoes_visivel = False

        # Configurar protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.criar_interface()
        self.carregar_produtos()
        self.carregar_clientes()
        self.configurar_bindings()

    def conectar_banco(self):
        """Método da classe para conectar ao banco de dados"""
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',  
                database='lanchonete_db',
                charset='utf8mb4',
                collation='utf8mb4_0900_ai_ci'
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def gerar_numero_pedido(self):
        """Gera número único para o pedido"""
        return f"PV{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def carregar_clientes(self):
        """Carrega lista de clientes cadastrados para autocompletar"""
        try:
            conexao = self.conectar_banco()
            if not conexao:
                return
            
            cursor = conexao.cursor()
            cursor.execute("SELECT DISTINCT nome FROM clientes ORDER BY nome")
            self.clientes_cadastrados = [cliente[0] for cliente in cursor.fetchall()]
        
        except Error as e:
            print(f"Erro ao carregar clientes: {e}")
            self.clientes_cadastrados = []
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()
        
        print(f"Clientes carregados: {len(self.clientes_cadastrados)}")
        if self.clientes_cadastrados:
            print("Primeiros 3 clientes:", self.clientes_cadastrados[:3])

    def criar_interface(self):
        # Container principal com scroll
        main_canvas = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#f8fafc")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)

        # Header moderno com gradiente
        self.criar_header(scrollable_frame)

        # Container principal de conteúdo
        content_container = tk.Frame(scrollable_frame, bg="#f8fafc")
        content_container.pack(fill="both", expand=True, padx=30, pady=20)

        # Grid layout responsivo
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=1)

        # Lado esquerdo - Informações do cliente e produtos
        left_panel = tk.Frame(content_container, bg="#f8fafc")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # Informações do cliente
        self.criar_secao_cliente(left_panel)

        # Produtos disponíveis
        self.criar_secao_produtos(left_panel)

        # Lado direito - Pedido atual
        right_panel = tk.Frame(content_container, bg="#f8fafc")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        # Pedido atual
        self.criar_secao_pedido(right_panel)

        # Observações
        self.criar_secao_observacoes(right_panel)

        # Botões de ação
        self.criar_botoes_acao(right_panel)

        # Configurar canvas e scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")

        # Bind do scroll do mouse
        self.bind_mousewheel(main_canvas)

    def criar_header(self, parent):
        """Cria header moderno com gradiente"""
        header_frame = tk.Frame(parent, bg="#4f46e5", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Canvas para gradiente
        header_canvas = tk.Canvas(header_frame, height=120, highlightthickness=0)
        header_canvas.pack(fill="both", expand=True)

        # Gradiente de roxo para azul
        for i in range(120):
            color = self.interpolar_cor("#4f46e5", "#06b6d4", i/120)
            header_canvas.create_line(0, i, 1200, i, fill=color, width=1)

        # Conteúdo do header
        header_canvas.create_text(60, 35, text="🍽️", font=("Arial", 28), fill="white", anchor="w")
        header_canvas.create_text(120, 30, text="PEDIDO PARA VIAGEM", 
                                 font=("Arial", 24, "bold"), fill="white", anchor="w")
        header_canvas.create_text(120, 55, text="Crie pedidos de forma rápida e organizada", 
                                 font=("Arial", 12), fill="#e0e7ff", anchor="w")
        
        # Número do pedido
        header_canvas.create_text(1140, 30, text=f"Nº {self.numero_pedido}", 
                                 font=("Arial", 14, "bold"), fill="white", anchor="e")
        header_canvas.create_text(1140, 50, text=datetime.now().strftime("%d/%m/%Y %H:%M"), 
                                 font=("Arial", 11), fill="#e0e7ff", anchor="e")

    def criar_card_moderno(self, parent, titulo, icon=""):
        """Cria um card moderno com sombra"""
        # Container do card
        card_container = tk.Frame(parent, bg="#f8fafc")
        card_container.pack(fill="both", expand=True, pady=(0, 20))

        # Sombra
        shadow = tk.Frame(card_container, bg="#e2e8f0", height=3)
        shadow.pack(side="bottom", fill="x")

        # Card principal
        card = tk.Frame(card_container, bg="white", relief="flat")
        card.pack(fill="both", expand=True, padx=0, pady=(0, 3))

        # Header do card
        header = tk.Frame(card, bg="#f1f5f9", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Título com ícone
        title_frame = tk.Frame(header, bg="#f1f5f9")
        title_frame.pack(fill="x", padx=20, pady=12)

        if icon:
            icon_label = tk.Label(title_frame, text=icon, font=("Arial", 16), 
                                 bg="#f1f5f9", fg="#4f46e5")
            icon_label.pack(side="left", padx=(0, 10))

        title_label = tk.Label(title_frame, text=titulo, font=("Arial", 14, "bold"),
                              bg="#f1f5f9", fg="#1e293b")
        title_label.pack(side="left")

        # Conteúdo do card
        content = tk.Frame(card, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        return content

    def criar_secao_cliente(self, parent):
        """Cria seção de informações do cliente com autocompletar"""
        content = self.criar_card_moderno(parent, "Informações do Cliente", "👤")

        # Grid para organizar campos
        content.grid_columnconfigure(1, weight=1)

        # Nome do cliente
        tk.Label(content, text="Nome do Cliente *", font=("Arial", 11, "bold"),
                bg="white", fg="#374151").grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Container para entry com autocompletar
        self.cliente_container = tk.Frame(content, bg="white")
        self.cliente_container.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        self.entry_cliente = tk.Entry(self.cliente_container, font=("Arial", 12), bg="#f9fafb", 
                                    relief="flat", bd=1, highlightthickness=1,
                                    highlightcolor="#4f46e5", highlightbackground="#d1d5db")
        self.entry_cliente.pack(fill="x", ipady=8)

        # Configurar eventos para autocompletar
        self.entry_cliente.bind("<KeyRelease>", self.on_cliente_keyrelease)
        self.entry_cliente.bind("<Button-1>", self.on_cliente_click)
        self.entry_cliente.bind("<FocusOut>", self.on_cliente_focus_out)

        # Telefone
        tk.Label(content, text="Telefone (opcional)", font=("Arial", 11, "bold"),
                bg="white", fg="#374151").grid(row=2, column=0, sticky="w", pady=(0, 5))

        self.entry_telefone = tk.Entry(content, font=("Arial", 12), bg="#f9fafb", 
                                    relief="flat", bd=1, highlightthickness=1,
                                    highlightcolor="#4f46e5", highlightbackground="#d1d5db")
        self.entry_telefone.grid(row=3, column=0, columnspan=2, sticky="ew", ipady=8)

    def on_cliente_keyrelease(self, event):
        """Evento ao digitar no campo cliente"""
        # Navegação com teclado nas sugestões
        if event.keysym in ['Up', 'Down'] and self.sugestoes_visivel:
            if self.listbox_sugestoes:
                self.listbox_sugestoes.focus_set()
                # Selecionar primeiro item se nada selecionado
                if not self.listbox_sugestoes.curselection():
                    self.listbox_sugestoes.selection_set(0)
                    self.listbox_sugestoes.activate(0)
            return
        
        if event.keysym == 'Return' and self.sugestoes_visivel:
            if self.listbox_sugestoes and self.listbox_sugestoes.curselection():
                self.on_suggestion_click(event)
            return
            
        if event.keysym in ['Tab', 'Escape']:
            self.hide_suggestions()
            return
            
        texto = self.entry_cliente.get()
        if len(texto) >= 1:
            self.show_suggestions(texto)
        else:
            self.hide_suggestions()

    def on_cliente_click(self, event):
        """Evento ao clicar no campo cliente"""
        texto = self.entry_cliente.get()
        if texto:
            self.show_suggestions(texto)

    def on_cliente_focus_out(self, event):
        """Evento ao perder foco do campo cliente"""
        # Delay para permitir clique na sugestão
        self.after(500, self.hide_suggestions)

    def show_suggestions(self, texto):
        """Mostra sugestões de clientes"""
        # Filtrar clientes que começam com o texto digitado
        sugestoes = [cliente for cliente in self.clientes_cadastrados 
                    if cliente.lower().startswith(texto.lower())]
        
        if not sugestoes:
            self.hide_suggestions()
            return
            
        # Criar ou atualizar listbox de sugestões
        if self.listbox_sugestoes is None:
            self.listbox_sugestoes = tk.Listbox(
                self.cliente_container,
                height=min(5, len(sugestoes)),
                font=("Arial", 11),
                bg="white",
                fg="black",
                relief="solid",
                bd=1,
                highlightthickness=0,
                activestyle="dotbox",
                selectbackground="#e0e7ff",
                selectforeground="black",
                exportselection=False  # IMPORTANTE: Evita conflitos de seleção
            )
            self.listbox_sugestoes.pack(fill="x", pady=(2, 0))
            
            # Configurar eventos - ORDEM IMPORTANTE
            self.listbox_sugestoes.bind("<Button-1>", self.on_suggestion_click)
            self.listbox_sugestoes.bind("<ButtonRelease-1>", self.on_suggestion_click)
            self.listbox_sugestoes.bind("<Double-Button-1>", self.on_suggestion_click)
            
            # Eventos de teclado
            self.listbox_sugestoes.bind("<Return>", self.on_suggestion_click)
            self.listbox_sugestoes.bind("<Up>", self.navigate_suggestions)
            self.listbox_sugestoes.bind("<Down>", self.navigate_suggestions)
            
        # Limpar e adicionar sugestões
        self.listbox_sugestoes.delete(0, tk.END)
        for sugestao in sugestoes[:5]:  # Máximo 5 sugestões
            self.listbox_sugestoes.insert(tk.END, sugestao)
            
        self.listbox_sugestoes.config(height=min(5, len(sugestoes)))
        self.sugestoes_visivel = True
        
    def navigate_suggestions(self, event):
        """Navega pelas sugestões com teclado"""
        try:
            if event.keysym == "Up":
                current = self.listbox_sugestoes.curselection()
                if current:
                    index = current[0]
                    if index > 0:
                        self.listbox_sugestoes.selection_clear(0, tk.END)
                        self.listbox_sugestoes.selection_set(index - 1)
                        self.listbox_sugestoes.activate(index - 1)
            
            elif event.keysym == "Down":
                current = self.listbox_sugestoes.curselection()
                if current:
                    index = current[0]
                    if index < self.listbox_sugestoes.size() - 1:
                        self.listbox_sugestoes.selection_clear(0, tk.END)
                        self.listbox_sugestoes.selection_set(index + 1)
                        self.listbox_sugestoes.activate(index + 1)
                else:
                    # Se nada selecionado, selecionar primeiro
                    self.listbox_sugestoes.selection_set(0)
                    self.listbox_sugestoes.activate(0)
                    
        except Exception as e:
            print(f"Erro na navegação: {e}")    

    def on_suggestion_click(self, event):
        """Evento ao clicar em uma sugestão"""
        try:
            widget = event.widget
            selection = widget.curselection()
            
            if selection:
                index = selection[0]
                selected = widget.get(index)
                
                print(f"Cliente selecionado: '{selected}'")  # Debug
                
                # Preencher o campo cliente IMEDIATAMENTE
                self.entry_cliente.delete(0, tk.END)
                self.entry_cliente.insert(0, selected)
                
                # Esconder sugestões
                self.hide_suggestions()
                
                # Carregar dados do cliente
                self.carregar_dados_cliente(selected)
                
                # Dar foco para o próximo campo
                self.entry_telefone.focus_set()
                
            else:
                # Se não há seleção, pegar o item sob o cursor
                index = widget.nearest(event.y)
                if index >= 0:
                    selected = widget.get(index)
                    print(f"Cliente selecionado (nearest): '{selected}'")
                    
                    self.entry_cliente.delete(0, tk.END)
                    self.entry_cliente.insert(0, selected)
                    self.hide_suggestions()
                    self.carregar_dados_cliente(selected)
                    self.entry_telefone.focus_set()
                    
        except Exception as e:
            print(f"Erro ao selecionar sugestão: {e}")
            
    def debug_clientes(self):
        """Método para debug - mostra lista de clientes carregados"""
        print("Clientes carregados:")
        for i, cliente in enumerate(self.clientes_cadastrados):
            print(f"{i}: '{cliente}' (len: {len(cliente)})")
        print(f"Total: {len(self.clientes_cadastrados)} clientes")

    def on_suggestion_select(self, event):
        """Evento ao pressionar Enter em uma sugestão"""
        self.on_suggestion_click(event)

    def hide_suggestions(self):
        """Esconde sugestões"""
        if self.listbox_sugestoes is not None:
            self.listbox_sugestoes.destroy()
            self.listbox_sugestoes = None
        self.sugestoes_visivel = False

    def carregar_dados_cliente(self, nome_cliente):
        """Carrega dados do cliente se estiver cadastrado"""
        try:
            conexao = self.conectar_banco()
            if not conexao:
                return
            
            cursor = conexao.cursor()
            cursor.execute("SELECT telefone FROM clientes WHERE nome = %s LIMIT 1", (nome_cliente,))
            result = cursor.fetchone()
        
            if result:
                telefone = result[0] if result[0] else ""
                self.entry_telefone.delete(0, tk.END)
                if telefone:
                    self.entry_telefone.insert(0, telefone)
            
        except Exception as e:
            print(f"Erro ao carregar dados do cliente: {e}")
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def criar_secao_produtos(self, parent):
        """Cria seção de produtos disponíveis"""
        content = self.criar_card_moderno(parent, "Produtos Disponíveis", "🛍️")

        # Busca de produtos
        search_frame = tk.Frame(content, bg="white")
        search_frame.pack(fill="x", pady=(0, 15))

        # Campo de busca moderno
        search_container = tk.Frame(search_frame, bg="#f9fafb", relief="flat")
        search_container.pack(fill="x", ipady=5)

        search_icon = tk.Label(search_container, text="🔍", font=("Arial", 12), 
                              bg="#f9fafb", fg="#6b7280")
        search_icon.pack(side="left", padx=(10, 5))

        self.entry_busca = tk.Entry(search_container, font=("Arial", 11), 
                                   bd=0, bg="#f9fafb", fg="#374151",
                                   insertbackground="#4f46e5")
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_busca.bind("<KeyRelease>", self.filtrar_produtos)

        # Placeholder
        self.entry_busca.insert(0, "Buscar produtos...")
        self.entry_busca.bind("<FocusIn>", self.clear_placeholder)
        self.entry_busca.bind("<FocusOut>", self.add_placeholder)
        self.entry_busca.config(fg="#6b7280")

        # Lista de produtos com scroll
        list_frame = tk.Frame(content, bg="white")
        list_frame.pack(fill="both", expand=True)

        # Canvas para scroll vertical
        self.produtos_canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0, height=300)
        produtos_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.produtos_canvas.yview)
        self.produtos_frame = tk.Frame(self.produtos_canvas, bg="white")

        self.produtos_frame.bind(
            "<Configure>",
            lambda e: self.produtos_canvas.configure(scrollregion=self.produtos_canvas.bbox("all"))
        )

        self.produtos_canvas.create_window((0, 0), window=self.produtos_frame, anchor="nw")
        self.produtos_canvas.configure(yscrollcommand=produtos_scrollbar.set)

        self.produtos_canvas.pack(side="left", fill="both", expand=True)
        produtos_scrollbar.pack(side="right", fill="y")

        # Bind scroll do mouse para produtos
        self.bind_mousewheel_produtos(self.produtos_canvas)

    def criar_secao_pedido(self, parent):
        """Cria seção do pedido atual"""
        content = self.criar_card_moderno(parent, "Pedido Atual", "🛒")

        # Header do pedido
        pedido_header = tk.Frame(content, bg="white")
        pedido_header.pack(fill="x", pady=(0, 15))

        # Total do pedido
        self.label_total = tk.Label(pedido_header, text="Total: R$ 0,00", 
                                   font=("Arial", 16, "bold"), bg="white", fg="#059669")
        self.label_total.pack(anchor="w")

        # Quantidade de itens
        self.label_itens = tk.Label(pedido_header, text="0 itens", 
                                   font=("Arial", 11), bg="white", fg="#6b7280")
        self.label_itens.pack(anchor="w")

        # Lista de itens do pedido
        self.frame_itens = tk.Frame(content, bg="white")
        self.frame_itens.pack(fill="both", expand=True)

        # Mensagem inicial
        self.criar_mensagem_pedido_vazio()

    def criar_secao_observacoes(self, parent):
        """Cria seção de observações"""
        content = self.criar_card_moderno(parent, "Observações", "📝")

        self.text_observacoes = tk.Text(content, height=4, font=("Arial", 11),
                                       bg="#f9fafb", relief="flat", bd=1,
                                       highlightthickness=1, highlightcolor="#4f46e5",
                                       highlightbackground="#d1d5db", wrap="word")
        self.text_observacoes.pack(fill="x", ipady=5)

        # Placeholder para observações
        self.text_observacoes.insert("1.0", "Adicione observações especiais sobre o pedido...")
        self.text_observacoes.bind("<FocusIn>", self.clear_obs_placeholder)
        self.text_observacoes.bind("<FocusOut>", self.add_obs_placeholder)
        self.text_observacoes.config(fg="#6b7280")

    def criar_botoes_acao(self, parent):
        """Cria botões de ação"""
        buttons_frame = tk.Frame(parent, bg="#f8fafc")
        buttons_frame.pack(fill="x", pady=(10, 20))

        # Botão Salvar Pedido
        btn_salvar = tk.Button(buttons_frame, text="💾 SALVAR PEDIDO", 
                            font=("Arial", 11, "bold"), bg="#059669", fg="white",
                            relief="flat", padx=30, pady=8, cursor="hand2",
                            command=self.salvar_pedido)
        btn_salvar.pack(side="left", padx=(0, 10))

        # Botão Pagar
        btn_pagar = tk.Button(buttons_frame, text="📄 GERAR CONTA", 
                            font=("Arial", 11, "bold"), bg="#2563eb", fg="white",
                            relief="flat", padx=30, pady=8, cursor="hand2",
                            command=self.gerar_conta)
        btn_pagar.pack(side="left", padx=(0, 10))

        # Botão Limpar
        btn_limpar = tk.Button(buttons_frame, text="🗑️ LIMPAR", 
                            font=("Arial", 11, "bold"), bg="#dc2626", fg="white",
                            relief="flat", padx=30, pady=8, cursor="hand2",
                            command=self.limpar_pedido)
        btn_limpar.pack(side="left", padx=(0, 10))

        # Botão Fechar
        btn_fechar = tk.Button(buttons_frame, text="❌ FECHAR", 
                            font=("Arial", 11, "bold"), bg="#6b7280", fg="white",
                            relief="flat", padx=30, pady=8, cursor="hand2",
                            command=self.destroy)
        btn_fechar.pack(side="right")

    def criar_mensagem_pedido_vazio(self):
        """Cria mensagem quando pedido está vazio"""
        empty_frame = tk.Frame(self.frame_itens, bg="white")
        empty_frame.pack(fill="both", expand=True)

        # Ícone
        icon_label = tk.Label(empty_frame, text="🛒", font=("Arial", 48), bg="white", fg="#d1d5db")
        icon_label.pack(pady=(40, 10))

        # Texto
        text_label = tk.Label(empty_frame, text="Nenhum item adicionado", 
                             font=("Arial", 12), bg="white", fg="#9ca3af")
        text_label.pack()

        sub_text = tk.Label(empty_frame, text="Selecione produtos para adicionar ao pedido", 
                           font=("Arial", 10), bg="white", fg="#d1d5db")
        sub_text.pack(pady=(5, 0))

    def criar_item_produto(self, produto):
        """Cria um item de produto na lista"""
        id_produto, nome, preco, estoque = produto
        
        # Container do item
        item_frame = tk.Frame(self.produtos_frame, bg="white", relief="flat")
        item_frame.pack(fill="x", pady=2)

        # Card do produto
        produto_card = tk.Frame(item_frame, bg="#f8fafc", relief="flat")
        produto_card.pack(fill="x", padx=2, pady=1)

        # Hover effects
        def on_enter(e):
            produto_card.config(bg="#e0e7ff")
        def on_leave(e):
            produto_card.config(bg="#f8fafc")

        produto_card.bind("<Enter>", on_enter)
        produto_card.bind("<Leave>", on_leave)

        # Conteúdo do produto
        content_frame = tk.Frame(produto_card, bg="#f8fafc")
        content_frame.pack(fill="x", padx=15, pady=10)

        # Nome e preço
        info_frame = tk.Frame(content_frame, bg="#f8fafc")
        info_frame.pack(fill="x")

        nome_label = tk.Label(info_frame, text=nome, font=("Arial", 11, "bold"),
                             bg="#f8fafc", fg="#1e293b", anchor="w")
        nome_label.pack(side="left", fill="x", expand=True)

        preco_label = tk.Label(info_frame, text=f"R$ {preco:.2f}", 
                              font=("Arial", 11, "bold"), bg="#f8fafc", fg="#059669")
        preco_label.pack(side="right")

        # Estoque e botão
        action_frame = tk.Frame(content_frame, bg="#f8fafc")
        action_frame.pack(fill="x", pady=(5, 0))

        estoque_label = tk.Label(action_frame, text=f"Estoque: {estoque}", 
                                font=("Arial", 9), bg="#f8fafc", fg="#6b7280")
        estoque_label.pack(side="left")

        # Botão adicionar
        if estoque > 0:
            btn_add = tk.Button(action_frame, text="+ Adicionar", 
                              font=("Arial", 9, "bold"), bg="#4f46e5", fg="white",
                              relief="flat", padx=15, pady=5, cursor="hand2",
                              command=lambda: self.adicionar_item(produto))
            btn_add.pack(side="right")
        else:
            btn_indisponivel = tk.Label(action_frame, text="Indisponível", 
                                      font=("Arial", 9), bg="#ef4444", fg="white",
                                      padx=15, pady=5)
            btn_indisponivel.pack(side="right")

    def adicionar_item(self, produto):
        """Adiciona item ao pedido"""
        id_produto, nome, preco, estoque = produto
        
        # Verificar se item já existe no pedido
        for i, item in enumerate(self.itens_pedido):
            if item['id'] == id_produto:
                if item['quantidade'] < estoque:
                    self.itens_pedido[i]['quantidade'] += 1
                    self.itens_pedido[i]['valor_total'] = self.itens_pedido[i]['quantidade'] * preco
                else:
                    messagebox.showwarning("Estoque Insuficiente", 
                                         f"Não há estoque suficiente para {nome}")
                self.atualizar_pedido()
                return

        # Adicionar novo item
        novo_item = {
            'id': id_produto,
            'nome': nome,
            'preco': preco,
            'quantidade': 1,
            'valor_total': preco
        }
        self.itens_pedido.append(novo_item)
        self.atualizar_pedido()

    def criar_item_pedido(self, item):
        """Cria um item na lista do pedido"""
        item_frame = tk.Frame(self.frame_itens, bg="#f1f5f9", relief="flat")
        item_frame.pack(fill="x", pady=2)

        # Conteúdo do item
        content_frame = tk.Frame(item_frame, bg="#f1f5f9")
        content_frame.pack(fill="x", padx=15, pady=8)

        # Nome do produto
        nome_label = tk.Label(content_frame, text=item['nome'], 
                             font=("Arial", 10, "bold"), bg="#f1f5f9", fg="#1e293b")
        nome_label.pack(anchor="w")

        # Quantidade e controles
        control_frame = tk.Frame(content_frame, bg="#f1f5f9")
        control_frame.pack(fill="x", pady=(5, 0))

        # Botão diminuir
        btn_menos = tk.Button(control_frame, text="−", font=("Arial", 12, "bold"),
                             bg="#ef4444", fg="white", relief="flat", width=3,
                             cursor="hand2", command=lambda: self.alterar_quantidade(item['id'], -1))
        btn_menos.pack(side="left")

        # Quantidade
        qty_label = tk.Label(control_frame, text=str(item['quantidade']), 
                            font=("Arial", 11, "bold"), bg="#f1f5f9", fg="#1e293b",
                            width=3)
        qty_label.pack(side="left", padx=5)

        # Botão aumentar
        btn_mais = tk.Button(control_frame, text="+", font=("Arial", 12, "bold"),
                            bg="#059669", fg="white", relief="flat", width=3,
                            cursor="hand2", command=lambda: self.alterar_quantidade(item['id'], 1))
        btn_mais.pack(side="left")

        # Subtotal
        subtotal_label = tk.Label(control_frame, text=f"R$ {item['valor_total']:.2f}", 
                                 font=("Arial", 11, "bold"), bg="#f1f5f9", fg="#059669")
        subtotal_label.pack(side="right")

        # Botão remover
        btn_remove = tk.Button(control_frame, text="🗑️", font=("Arial", 10),
                              bg="#dc2626", fg="white", relief="flat", cursor="hand2",
                              command=lambda: self.remover_item(item['id']))
        btn_remove.pack(side="right", padx=(0, 10))

    def alterar_quantidade(self, id_produto, delta):
        """Altera quantidade de um item"""
        for i, item in enumerate(self.itens_pedido):
            if item['id'] == id_produto:
                nova_qty = item['quantidade'] + delta
                if nova_qty <= 0:
                    self.remover_item(id_produto)
                else:
                    # Verificar estoque
                    produto_estoque = self.obter_estoque_produto(id_produto)
                    if nova_qty <= produto_estoque:
                        self.itens_pedido[i]['quantidade'] = nova_qty
                        self.itens_pedido[i]['valor_total'] = nova_qty * item['preco']
                    else:
                        messagebox.showwarning("Estoque Insuficiente", 
                                             f"Estoque disponível: {produto_estoque}")
                break
        self.atualizar_pedido()

    def remover_item(self, id_produto):
        """Remove item do pedido"""
        self.itens_pedido = [item for item in self.itens_pedido if item['id'] != id_produto]
        self.atualizar_pedido()

    def obter_estoque_produto(self, id_produto):
        """Obtém estoque atual do produto"""
        for produto in self.produtos:
            if produto[0] == id_produto:
                return produto[3]
        return 0

    def atualizar_pedido(self):
        """Atualiza a exibição do pedido"""
        # Limpar frame de itens
        for widget in self.frame_itens.winfo_children():
            widget.destroy()

        if not self.itens_pedido:
            self.criar_mensagem_pedido_vazio()
            self.total_pedido = 0.0
        else:
            # Calcular total
            self.total_pedido = sum(item['valor_total'] for item in self.itens_pedido)
            
            # Criar itens
            for item in self.itens_pedido:
                self.criar_item_pedido(item)

        # Atualizar labels
        self.label_total.config(text=f"Total: R$ {self.total_pedido:.2f}")
        total_itens = sum(item['quantidade'] for item in self.itens_pedido)
        self.label_itens.config(text=f"{total_itens} {'item' if total_itens == 1 else 'itens'}")

    def carregar_produtos(self):
        """Carrega produtos do banco de dados"""
        try:
            conexao = self.conectar_banco()
            if not conexao:
                return
            
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id, nome, preco, estoque
                FROM produtos 
                WHERE ativo = 1 
                ORDER BY nome
            """)
            self.produtos = cursor.fetchall()
            self.exibir_produtos()
        
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")
            self.produtos = []
        finally:
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def exibir_produtos(self, produtos_filtrados=None):
        """Exibe produtos na lista"""
        # Limpar produtos existentes
        for widget in self.produtos_frame.winfo_children():
            widget.destroy()

        produtos_para_exibir = produtos_filtrados if produtos_filtrados is not None else self.produtos
        
        if not produtos_para_exibir:
            # Mensagem de nenhum produto encontrado
            empty_frame = tk.Frame(self.produtos_frame, bg="white")
            empty_frame.pack(fill="both", expand=True, pady=50)
            
            tk.Label(empty_frame, text="🔍", font=("Arial", 32), 
                    bg="white", fg="#d1d5db").pack()
            tk.Label(empty_frame, text="Nenhum produto encontrado", 
                    font=("Arial", 12), bg="white", fg="#9ca3af").pack(pady=5)
        else:
            for produto in produtos_para_exibir:
                self.criar_item_produto(produto)

    def filtrar_produtos(self, event=None):
        """Filtra produtos conforme busca"""
        termo_busca = self.entry_busca.get().lower()
        
        # Ignorar placeholder
        if termo_busca == "buscar produtos...":
            self.exibir_produtos()
            return

        produtos_filtrados = [
            produto for produto in self.produtos
            if termo_busca in produto[1].lower()  # nome do produto
        ]
        
        self.exibir_produtos(produtos_filtrados)

    def clear_placeholder(self, event):
        """Remove placeholder do campo de busca"""
        if self.entry_busca.get() == "Buscar produtos...":
            self.entry_busca.delete(0, tk.END)
            self.entry_busca.config(fg="#374151")

    def add_placeholder(self, event):
        """Adiciona placeholder se campo estiver vazio"""
        if not self.entry_busca.get():
            self.entry_busca.insert(0, "Buscar produtos...")
            self.entry_busca.config(fg="#6b7280")

    def clear_obs_placeholder(self, event):
        """Remove placeholder das observações"""
        content = self.text_observacoes.get("1.0", tk.END).strip()
        if content == "Adicione observações especiais sobre o pedido...":
            self.text_observacoes.delete("1.0", tk.END)
            self.text_observacoes.config(fg="#374151")

    def add_obs_placeholder(self, event):
        """Adiciona placeholder se campo estiver vazio"""
        content = self.text_observacoes.get("1.0", tk.END).strip()
        if not content:
            self.text_observacoes.insert("1.0", "Adicione observações especiais sobre o pedido...")
            self.text_observacoes.config(fg="#6b7280")

    def salvar_pedido(self):
        """Salva o pedido e abre automaticamente a tela de pagamento"""
        # Validações
        if not self.entry_cliente.get().strip():
            messagebox.showerror("Erro", "Nome do cliente é obrigatório!")
            self.entry_cliente.focus()
            return

        if not self.itens_pedido:
            messagebox.showerror("Erro", "Adicione pelo menos um item ao pedido!")
            return

        nome_cliente = self.entry_cliente.get().strip()
        telefone_cliente = self.entry_telefone.get().strip()

        try:
            conexao = self.conectar_banco()
            if not conexao:
                messagebox.showerror("Erro", "Erro ao conectar com o banco de dados!")
                return
            
            cursor = conexao.cursor()

            # Verificar se cliente existe
            cursor.execute("SELECT id, telefone FROM clientes WHERE nome = %s", (nome_cliente,))
            cliente = cursor.fetchone()
        
            if not cliente:
                messagebox.showerror("Erro", "Cliente não cadastrado!")
                self.entry_cliente.focus()
                return
                
            # Fechar conexão temporária
            cursor.close()
            conexao.close()
            
            # Abrir automaticamente a tela de conta/pagamento
            self.gerar_conta()
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao validar dados: {e}")
            if conexao and conexao.is_connected():
                cursor.close()
                conexao.close()

    def conectar_banco(self):
        """Método da classe para conectar ao banco de dados"""
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor', 
                password='admin321@s',  
                database='lanchonete_db',
                charset='utf8mb4',
                collation='utf8mb4_0900_ai_ci'
            )
            return conexao
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None            

    def limpar_pedido(self):
        """Limpa o formulário"""
        # Limpar campos
        self.entry_cliente.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.text_observacoes.delete("1.0", tk.END)
        
        # Restaurar placeholders
        self.add_placeholder(None)
        self.add_obs_placeholder(None)
        
        # Limpar pedido
        self.itens_pedido = []
        self.total_pedido = 0.0
        self.numero_pedido = self.gerar_numero_pedido()
        
        # Atualizar interface
        self.atualizar_pedido()
        self.carregar_produtos()  # Recarregar para atualizar estoques
        
        # Esconder sugestões se visíveis
        self.hide_suggestions()

    def gerar_conta(self):
        """Gera a conta do pedido de viagem"""
        # Validar se há itens no pedido
        if not self.itens_pedido:
            messagebox.showwarning("Aviso", "Nenhum item no pedido para gerar conta.")
            return

        # Obter dados do cliente
        nome_cliente = self.entry_cliente.get().strip()
        telefone_cliente = self.entry_telefone.get().strip()
        
        if not nome_cliente:
            messagebox.showerror("Erro", "Nome do cliente é obrigatório para gerar a conta!")
            self.entry_cliente.focus()
            return

        # Obter observações
        observacoes = self.text_observacoes.get("1.0", tk.END).strip()
        if observacoes == "Adicione observações especiais sobre o pedido...":
            observacoes = ""

        # Criar janela da conta
        janela_conta = tk.Toplevel(self)
        janela_conta.title(f"Conta - Pedido {self.numero_pedido}")
        janela_conta.geometry("450x600")
        janela_conta.configure(bg="white")
        janela_conta.resizable(False, False)
        
        # Centralizar a janela
        janela_conta.transient(self)
        janela_conta.grab_set()
        
        # Centralizar na tela
        largura_janela = 450
        altura_janela = 600
        largura_tela = janela_conta.winfo_screenwidth()
        altura_tela = janela_conta.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_conta.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Cabeçalho com gradiente
        frame_header = tk.Frame(janela_conta, bg="#4f46e5", height=100)
        frame_header.pack(fill="x")
        frame_header.pack_propagate(False)

        # Canvas para gradiente no header
        header_canvas = tk.Canvas(frame_header, height=100, highlightthickness=0)
        header_canvas.pack(fill="both", expand=True)

        # Gradiente de roxo para azul
        for i in range(100):
            color = self.interpolar_cor("#4f46e5", "#06b6d4", i/100)
            header_canvas.create_line(0, i, 450, i, fill=color, width=1)

        # Conteúdo do header
        header_canvas.create_text(225, 20, text="🍽️ EMPÓRIO DO SABOR", 
                                font=("Arial", 16, "bold"), fill="white", anchor="center")
        header_canvas.create_text(225, 45, text="CONTA PARA VIAGEM", 
                                font=("Arial", 12), fill="#e0e7ff", anchor="center")
        header_canvas.create_text(225, 65, text=f"Pedido: {self.numero_pedido}", 
                                font=("Arial", 11, "bold"), fill="white", anchor="center")
        header_canvas.create_text(225, 80, text=datetime.now().strftime("%d/%m/%Y às %H:%M"), 
                                font=("Arial", 10), fill="#e0e7ff", anchor="center")

        # Frame principal com scroll
        main_frame = tk.Frame(janela_conta, bg="white")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Canvas para scroll
        canvas_conta = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar_conta = ttk.Scrollbar(main_frame, orient="vertical", command=canvas_conta.yview)
        scrollable_conta = tk.Frame(canvas_conta, bg="white")

        scrollable_conta.bind(
            "<Configure>",
            lambda e: canvas_conta.configure(scrollregion=canvas_conta.bbox("all"))
        )

        canvas_conta.create_window((0, 0), window=scrollable_conta, anchor="nw")
        canvas_conta.configure(yscrollcommand=scrollbar_conta.set)

        # Informações do cliente
        frame_cliente = tk.Frame(scrollable_conta, bg="#f8fafc", relief="solid", bd=1)
        frame_cliente.pack(fill="x", pady=(0, 15))
        
        tk.Label(frame_cliente, text="👤 DADOS DO CLIENTE", 
                font=("Arial", 11, "bold"), bg="#f8fafc", fg="#374151").pack(anchor="w", padx=10, pady=(8, 5))
        
        tk.Label(frame_cliente, text=f"Nome: {nome_cliente}", 
                font=("Arial", 10), bg="#f8fafc", fg="#1e293b").pack(anchor="w", padx=10)
        
        if telefone_cliente:
            tk.Label(frame_cliente, text=f"Telefone: {telefone_cliente}", 
                    font=("Arial", 10), bg="#f8fafc", fg="#1e293b").pack(anchor="w", padx=10, pady=(0, 8))
        else:
            tk.Label(frame_cliente, text=" ", bg="#f8fafc").pack(pady=(0, 8))

        # Linha separadora
        tk.Frame(scrollable_conta, height=2, bg="#e5e7eb").pack(fill="x", pady=10)

        # Itens do pedido
        tk.Label(scrollable_conta, text="🛍️ ITENS DO PEDIDO:", 
                font=("Arial", 12, "bold"), bg="white", fg="#1e293b").pack(anchor="w", pady=(5, 10))

        # Criar tabela de itens
        for i, item in enumerate(self.itens_pedido, 1):
            frame_item = tk.Frame(scrollable_conta, bg="white", relief="solid", bd=1)
            frame_item.pack(fill="x", pady=2)

            # Header do item
            frame_item_header = tk.Frame(frame_item, bg="#f1f5f9")
            frame_item_header.pack(fill="x")
            
            tk.Label(frame_item_header, text=f"{i:02d}. {item['nome']}", 
                    font=("Arial", 11, "bold"), bg="#f1f5f9", fg="#1e293b").pack(anchor="w", padx=10, pady=5)

            # Detalhes do item
            frame_detalhes = tk.Frame(frame_item, bg="white")
            frame_detalhes.pack(fill="x", padx=10, pady=5)
            
            # Linha com quantidade, preço unitário e total
            detalhes_frame = tk.Frame(frame_detalhes, bg="white")
            detalhes_frame.pack(fill="x")
            
            tk.Label(detalhes_frame, text=f"Quantidade: {item['quantidade']}", 
                    font=("Arial", 10), bg="white", fg="#6b7280").pack(side="left")
            
            tk.Label(detalhes_frame, text=f"Preço unit.: R$ {item['preco']:.2f}", 
                    font=("Arial", 10), bg="white", fg="#6b7280").pack(side="left", padx=(20, 0))
            
            tk.Label(detalhes_frame, text=f"Subtotal: R$ {item['valor_total']:.2f}", 
                    font=("Arial", 10, "bold"), bg="white", fg="#059669").pack(side="right")

        # Observações (se houver)
        if observacoes.strip():
            tk.Frame(scrollable_conta, height=2, bg="#e5e7eb").pack(fill="x", pady=15)
            
            frame_obs = tk.Frame(scrollable_conta, bg="#fef3c7", relief="solid", bd=1)
            frame_obs.pack(fill="x", pady=5)
            
            tk.Label(frame_obs, text="📝 OBSERVAÇÕES:", 
                    font=("Arial", 11, "bold"), bg="#fef3c7", fg="#92400e").pack(anchor="w", padx=10, pady=(8, 5))
            tk.Label(frame_obs, text=observacoes, 
                    font=("Arial", 10), bg="#fef3c7", fg="#78350f", 
                    wraplength=400, justify="left").pack(anchor="w", padx=10, pady=(0, 8))

        # Linha separadora final
        tk.Frame(scrollable_conta, height=3, bg="#d1d5db").pack(fill="x", pady=20)

        # Frame do total
        frame_total = tk.Frame(scrollable_conta, bg="#f0fdf4", relief="solid", bd=2)
        frame_total.pack(fill="x", pady=10)
        
        # Resumo do pedido
        resumo_frame = tk.Frame(frame_total, bg="#f0fdf4")
        resumo_frame.pack(fill="x", padx=15, pady=10)
        
        total_itens = sum(item['quantidade'] for item in self.itens_pedido)
        tk.Label(resumo_frame, text=f"Total de itens: {total_itens}", 
                font=("Arial", 11), bg="#f0fdf4", fg="#166534").pack(anchor="w")
        tk.Label(resumo_frame, text=f"Número de produtos: {len(self.itens_pedido)}", 
                font=("Arial", 11), bg="#f0fdf4", fg="#166534").pack(anchor="w")
        
        # Total principal
        tk.Label(frame_total, text="💰 TOTAL A PAGAR:", 
                font=("Arial", 14, "bold"), bg="#f0fdf4", fg="#166534").pack(pady=(10, 5))
        tk.Label(frame_total, text=f"R$ {self.total_pedido:.2f}", 
                font=("Arial", 20, "bold"), bg="#f0fdf4", fg="#059669").pack(pady=(0, 15))

        # Rodapé
        frame_rodape = tk.Frame(scrollable_conta, bg="white")
        frame_rodape.pack(fill="x", pady=15)
        
        tk.Label(frame_rodape, text="🙏 Obrigado pela preferência!", 
                font=("Arial", 12, "italic"), bg="white", fg="#6b7280").pack()
        tk.Label(frame_rodape, text="Volte sempre!", 
                font=("Arial", 10), bg="white", fg="#9ca3af").pack()

        # Configurar scroll
        canvas_conta.pack(side="left", fill="both", expand=True)
        scrollbar_conta.pack(side="right", fill="y")

        # Configurar scroll do mouse
        def _on_mousewheel(event):
            canvas_conta.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas_conta.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas_conta.unbind_all("<MouseWheel>")
        
        canvas_conta.bind('<Enter>', _bind_to_mousewheel)
        canvas_conta.bind('<Leave>', _unbind_from_mousewheel)

        # Frame de botões na parte inferior da janela principal
        frame_botoes = tk.Frame(janela_conta, bg="white")
        frame_botoes.pack(fill="x", pady=10, padx=15)

        # MODIFICAÇÃO PRINCIPAL: Apenas o botão de PAGAR
        tk.Button(frame_botoes, text="💳 PAGAR", 
                font=("Arial", 12, "bold"), bg="#16a34a", fg="white",
                relief="flat", padx=20, pady=10, cursor="hand2",
                command=lambda: self.pagar_conta(janela_conta)).pack(side="left", padx=(0, 10))

        tk.Button(frame_botoes, text="❌ Cancelar", 
                font=("Arial", 11, "bold"), bg="#dc2626", fg="white",
                relief="flat", padx=20, pady=8, cursor="hand2",
                command=janela_conta.destroy).pack(side="right")

        # Configurar tecla ESC para fechar
        janela_conta.bind("<Escape>", lambda e: janela_conta.destroy())

    def pagar_conta(self, janela_conta):
        """Função para processar o pagamento da conta"""
        # Criar janela de pagamento
        janela_pagamento = tk.Toplevel(janela_conta)
        janela_pagamento.title("Formas de Pagamento")
        janela_pagamento.geometry("500x350")
        janela_pagamento.configure(bg="white")
        janela_pagamento.resizable(False, False)
        
        # Centralizar a janela
        janela_pagamento.transient(janela_conta)
        janela_pagamento.grab_set()
        
        # Centralizar na tela
        largura_janela = 500
        altura_janela = 350
        largura_tela = janela_pagamento.winfo_screenwidth()
        altura_tela = janela_pagamento.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_pagamento.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Cabeçalho
        frame_header_pag = tk.Frame(janela_pagamento, bg="#16a34a", height=80)
        frame_header_pag.pack(fill="x")
        frame_header_pag.pack_propagate(False)

        tk.Label(frame_header_pag, text="💳 FORMA DE PAGAMENTO", 
                font=("Arial", 16, "bold"), bg="#16a34a", fg="white").pack(expand=True)

        # Frame principal
        frame_principal = tk.Frame(janela_pagamento, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Valor total
        tk.Label(frame_principal, text=f"Total a pagar: R$ {self.total_pedido:.2f}", 
                font=("Arial", 14, "bold"), bg="white", fg="#1e293b").pack(pady=(0, 20))

        # Título das opções
        tk.Label(frame_principal, text="Selecione a forma de pagamento:", 
                font=("Arial", 12), bg="white", fg="#374151").pack(pady=(0, 15))

        # Frame dos botões de pagamento
        frame_botoes_pag = tk.Frame(frame_principal, bg="white")
        frame_botoes_pag.pack(fill="x", pady=10)

        # FUNÇÃO PRINCIPAL MODIFICADA: Salvar no banco APENAS após pagamento
        def processar_pagamento(metodo, metodo_display):
            try:
                nome_cliente = self.entry_cliente.get().strip()
                telefone_cliente = self.entry_telefone.get().strip()
                
                # Obter observações
                observacoes = self.text_observacoes.get("1.0", tk.END).strip()
                if observacoes == "Adicione observações especiais sobre o pedido...":
                    observacoes = ""

                conexao = self.conectar_banco()
                if not conexao:
                    messagebox.showerror("Erro", "Erro ao conectar com o banco de dados!")
                    return
                
                cursor = conexao.cursor()

                # Verificar se cliente existe e obter dados
                cursor.execute("SELECT id, telefone FROM clientes WHERE nome = %s", (nome_cliente,))
                cliente = cursor.fetchone()
                
                if not cliente:
                    messagebox.showerror("Erro", "Cliente não cadastrado!")
                    cursor.close()
                    conexao.close()
                    return
                    
                id_cliente = cliente[0]
                telefone_bd = cliente[1] or ""
              
                cursor.execute("""
                    INSERT INTO pedidos (numero_pedido, id_cliente, cliente, telefone, tipo, total, 
                                    observacoes, status, forma_pagamento, data_pedido) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    self.numero_pedido,
                    id_cliente,
                    nome_cliente,
                    telefone_bd,
                    'viagem',
                    self.total_pedido,
                    observacoes,
                    'pendente', 
                    metodo,        # Forma de pagamento já definida
                    datetime.now()
                ))
            
                id_pedido = cursor.lastrowid

                # Inserir itens do pedido
                for item in self.itens_pedido:
                    cursor.execute("""
                        INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario, valor_total)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        id_pedido,
                        item['id'],
                        item['quantidade'],
                        item['preco'],
                        item['valor_total']
                    ))

                conexao.commit()
                cursor.close()
                conexao.close()
                
                # Fechar janelas
                janela_pagamento.destroy()
                janela_conta.destroy()
                
                # Mostrar confirmação de sucesso
                messagebox.showinfo(
                    "Pedido Finalizado", 
                    f"🎉 PEDIDO ENVIADO PARA COZINHA! 🎉\n\n"
                    f"Pedido: {self.numero_pedido}\n"
                    f"Cliente: {nome_cliente}\n"
                    f"Total: R$ {self.total_pedido:.2f}\n"
                    f"Pagamento: {metodo_display}\n"
                    f"Itens: {len(self.itens_pedido)}\n\n"
                    f"O pedido foi enviado para a cozinha e será preparado!"
                )
                
                # Limpar o pedido atual para novo pedido
                self.limpar_pedido()
                
            except Exception as e:
                print(f"Erro ao processar pagamento: {e}")
                messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}")
                if conexao and conexao.is_connected():
                    cursor.close()
                    conexao.close()

        # Botões de pagamento em grid 2x2
        botoes_frame = tk.Frame(frame_botoes_pag, bg="white")
        botoes_frame.pack(expand=True)

        # Definir funções específicas para cada botão
        def pagar_debito():
            processar_pagamento("debito", "Cartão de Débito")
        
        def pagar_credito():
            processar_pagamento("credito", "Cartão de Crédito")
        
        def pagar_pix():
            processar_pagamento("pix", "PIX")
        
        def pagar_dinheiro():
            processar_pagamento("dinheiro", "Dinheiro")

        # Botões com funções específicas
        tk.Button(botoes_frame, text="💳 Cartão de Débito", 
                font=("Arial", 11, "bold"), bg="#2563eb", fg="white",
                relief="flat", padx=20, pady=10, cursor="hand2", width=15,
                command=pagar_debito).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(botoes_frame, text="💳 Cartão de Crédito", 
                font=("Arial", 11, "bold"), bg="#7c3aed", fg="white",
                relief="flat", padx=20, pady=10, cursor="hand2", width=15,
                command=pagar_credito).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(botoes_frame, text="📱 PIX", 
                font=("Arial", 11, "bold"), bg="#059669", fg="white",
                relief="flat", padx=20, pady=10, cursor="hand2", width=15,
                command=pagar_pix).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(botoes_frame, text="💵 Dinheiro", 
                font=("Arial", 11, "bold"), bg="#dc2626", fg="white",
                relief="flat", padx=20, pady=10, cursor="hand2", width=15,
                command=pagar_dinheiro).grid(row=1, column=1, padx=5, pady=5)

        # Botão cancelar
        tk.Button(frame_principal, text="❌ Cancelar", 
                font=("Arial", 10), bg="#6b7280", fg="white",
                relief="flat", padx=15, pady=5, cursor="hand2",
                command=janela_pagamento.destroy).pack(pady=(20, 0))

        # Configurar tecla ESC para fechar
        janela_pagamento.bind("<Escape>", lambda e: janela_pagamento.destroy())

    def salvar_pdf_conta(self):
        """Função para salvar a conta em PDF (implementação básica)"""
        try:
            # Aqui você pode implementar a geração de PDF
            # Por exemplo, usando reportlab ou weasyprint
            messagebox.showinfo("PDF", "Função de geração de PDF não implementada ainda.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

    def configurar_bindings(self):
        """Configura bindings de teclado"""
        # Atalhos de teclado
        self.bind("<Control-s>", lambda e: self.salvar_pedido())
        self.bind("<Control-l>", lambda e: self.limpar_pedido())
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Binding para campo cliente - permitir navegação
        self.entry_cliente.bind("<Up>", self.on_cliente_keyrelease)
        self.entry_cliente.bind("<Down>", self.on_cliente_keyrelease)
        
        # Foco no campo cliente ao abrir
        self.after(100, lambda: self.entry_cliente.focus())

    def bind_mousewheel(self, canvas):
        """Configura scroll do mouse para canvas principal"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

    def bind_mousewheel_produtos(self, canvas):
        """Configura scroll do mouse para canvas de produtos"""
        def _on_mousewheel_produtos(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel_produtos(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel_produtos)
        
        def _unbind_from_mousewheel_produtos(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel_produtos)
        canvas.bind('<Leave>', _unbind_from_mousewheel_produtos)

    def interpolar_cor(self, cor1, cor2, fator):
        """Interpola entre duas cores para criar gradiente"""
        # Converter cores hex para RGB
        def hex_para_rgb(hex_cor):
            hex_cor = hex_cor.lstrip('#')
            return tuple(int(hex_cor[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_para_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        rgb1 = hex_para_rgb(cor1)
        rgb2 = hex_para_rgb(cor2)
        
        # Interpolar cada componente RGB
        rgb_interpolado = tuple(
            rgb1[i] + (rgb2[i] - rgb1[i]) * fator for i in range(3)
        )
        
        return rgb_para_hex(rgb_interpolado)

    def on_closing(self):
        """Evento de fechamento da janela"""
        if self.itens_pedido:
            resposta = messagebox.askyesno(
                "Confirmar", 
                "Há itens no pedido atual. Deseja realmente fechar sem salvar?"
            )
            if resposta:
                self.destroy()
        else:
            self.destroy()

# Exemplo de uso (para testes)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Esconder janela principal
    
    # Criar tela de pedido
    tela = TelaPedidoViagem(root)
    
    # Iniciar loop principal
    root.mainloop()