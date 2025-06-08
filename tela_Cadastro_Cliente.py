import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from pathlib import Path
import mysql.connector
from mysql.connector import Error
import re

class TelaCadastroCliente:
    def __init__(self, master):
        self.master = master
        
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
        
        self.master.title("Cadastro de Cliente - Empório do Sabor")
        self.master.geometry("650x620")
        self.master.resizable(False, False)
        
        # Centralizar janela
        self.centralizar_janela()
        
        # Cores modernas
        self.cores = {
            'bg_principal': '#f8f9fa',
            'bg_card': '#ffffff',
            'primary': '#4f46e5',
            'primary_hover': '#4338ca',
            'success': '#10b981',
            'success_hover': '#059669',
            'warning': '#f59e0b',
            'warning_hover': '#d97706',
            'danger': '#ef4444',
            'danger_hover': '#dc2626',
            'text_dark': '#1f2937',
            'text_light': '#6b7280',
            'border': '#e5e7eb',
            'input_bg': '#ffffff',
            'shadow': "#2B2B2B"
        }
        
        self.master.configure(bg=self.cores['bg_principal'])
        self.criar_widgets()
        self.aplicar_animacoes()
    
    def centralizar_janela(self):
        largura_janela = 650
        altura_janela = 620
        
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        
        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    
    def criar_widgets(self):
        # Container principal com sombra
        self.container_principal = tk.Frame(
            self.master, 
            bg=self.cores['bg_card'],
            relief='flat',
            bd=0
        )
        self.container_principal.place(x=30, y=30, width=590, height=560)
        
        # Simular sombra
        sombra = tk.Frame(
            self.master,
            bg=self.cores['shadow'],
            relief='flat'
        )
        sombra.place(x=35, y=35, width=590, height=560)
        self.container_principal.lift()
        
        # Header com gradiente simulado
        self.header = tk.Frame(
            self.container_principal,
            bg=self.cores['primary'],
            height=65
        )
        self.header.pack(fill='x', padx=0, pady=0)
        self.header.pack_propagate(False)
        
        # Título no header
        self.titulo = tk.Label(
            self.header,
            text="Cadastro de Cliente",
            font=("Segoe UI", 18, "bold"),
            bg=self.cores['primary'],
            fg='white'
        )
        self.titulo.pack(expand=True)
        
        # Subtítulo
        self.subtitulo = tk.Label(
            self.header,
            text="Preencha os dados do cliente",
            font=("Segoe UI", 9),
            bg=self.cores['primary'],
            fg='#e0e7ff'
        )
        self.subtitulo.pack(pady=(0, 10))
        
        # Container dos campos
        self.container_campos = tk.Frame(
            self.container_principal,
            bg=self.cores['bg_card']
        )
        self.container_campos.pack(fill='both', expand=True, padx=30, pady=20)
        
        self.criar_campos()
        self.criar_botoes()
    
    def criar_campo_moderno(self, parent, label_text, row, is_text_area=False):
        # Container para cada campo
        campo_frame = tk.Frame(parent, bg=self.cores['bg_card'])
        campo_frame.grid(row=row, column=0, sticky='ew', pady=(0, 15))
        
        # Label 
        label = tk.Label(
            campo_frame,
            text=label_text,
            font=("Segoe UI", 9, "bold"),
            bg=self.cores['bg_card'],
            fg=self.cores['text_dark'],
            anchor='w'
        )
        label.pack(fill='x', pady=(0, 5))
        
        if is_text_area:
            # Text area para endereço
            text_frame = tk.Frame(campo_frame, bg=self.cores['border'], height=60)
            text_frame.pack(fill='x')
            text_frame.pack_propagate(False)
            
            entry = tk.Text(
                text_frame,
                font=("Segoe UI", 9),
                bg=self.cores['input_bg'],
                fg=self.cores['text_dark'],
                relief='flat',
                bd=0,
                padx=12,
                pady=8,
                height=2,
                wrap=tk.WORD
            )
            entry.pack(fill='both', expand=True, padx=2, pady=2)
        else:
            # Entry normal
            entry_frame = tk.Frame(campo_frame, bg=self.cores['border'], height=38)
            entry_frame.pack(fill='x')
            entry_frame.pack_propagate(False)
            
            entry = tk.Entry(
                entry_frame,
                font=("Segoe UI", 9),
                bg=self.cores['input_bg'],
                fg=self.cores['text_dark'],
                relief='flat',
                bd=0
            )
            entry.pack(fill='both', expand=True, padx=2, pady=2)
            
            # Padding interno
            entry.configure(justify='left')
            entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry_frame))
            entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry_frame))
        
        return entry
    
    def on_entry_focus_in(self, frame):
        frame.configure(bg=self.cores['primary'])
    
    def on_entry_focus_out(self, frame):
        frame.configure(bg=self.cores['border'])
    
    def criar_campos(self):
        # Configurar grid - peso para a coluna principal
        self.container_campos.grid_columnconfigure(0, weight=1)
        
        # Criar os campos
        self.entry_nome = self.criar_campo_moderno(
            self.container_campos, "Nome Completo *", 0
        )
        
        self.entry_cpf = self.criar_campo_moderno(
            self.container_campos, "CPF *", 1
        )
        
        self.entry_telefone = self.criar_campo_moderno(
            self.container_campos, "Telefone *", 2
        )
        
        self.entry_endereco = self.criar_campo_moderno(
            self.container_campos, "Endereço Completo *", 3, is_text_area=True
        )
        
        # Máscara para CPF e telefone
        self.entry_cpf.bind('<KeyRelease>', self.aplicar_mascara_cpf)
        self.entry_telefone.bind('<KeyRelease>', self.aplicar_mascara_telefone)
    
    def aplicar_mascara_cpf(self, event):
        texto = self.entry_cpf.get()
        # Remove tudo que não é número
        numeros = re.sub(r'\D', '', texto)
        
        # Aplica máscara XXX.XXX.XXX-XX
        if len(numeros) <= 11:
            if len(numeros) > 3 and len(numeros) <= 6:
                texto_formatado = f"{numeros[:3]}.{numeros[3:]}"
            elif len(numeros) > 6 and len(numeros) <= 9:
                texto_formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
            elif len(numeros) > 9:
                texto_formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
            else:
                texto_formatado = numeros
            
            self.entry_cpf.delete(0, tk.END)
            self.entry_cpf.insert(0, texto_formatado)
    
    def aplicar_mascara_telefone(self, event):
        texto = self.entry_telefone.get()
        numeros = re.sub(r'\D', '', texto)
        
        # Aplica máscara (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
        if len(numeros) <= 11:
            if len(numeros) > 2 and len(numeros) <= 7:
                texto_formatado = f"({numeros[:2]}) {numeros[2:]}"
            elif len(numeros) > 7 and len(numeros) <= 10:
                texto_formatado = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
            elif len(numeros) > 10:
                texto_formatado = f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
            elif len(numeros) > 0:
                if len(numeros) <= 2:
                    texto_formatado = f"({numeros}"
                else:
                    texto_formatado = numeros
            else:
                texto_formatado = numeros
            
            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, texto_formatado)
    
    def criar_botao_moderno(self, parent, texto, cor_bg, cor_hover, comando, icone=None):
        botao = tk.Button(
            parent,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            bg=cor_bg,
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=comando
        )
        
        # Efeitos hover
        def on_enter(e):
            botao.configure(bg=cor_hover)
        
        def on_leave(e):
            botao.configure(bg=cor_bg)
        
        botao.bind('<Enter>', on_enter)
        botao.bind('<Leave>', on_leave)
        
        return botao
    
    def criar_botoes(self):
        # Container dos botões usando grid
        botoes_frame = tk.Frame(
            self.container_campos,
            bg=self.cores['bg_card']
        )
        botoes_frame.grid(row=4, column=0, sticky='ew', pady=(15, 0))
        
        # Configurar o grid do frame dos botões
        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)
        botoes_frame.grid_columnconfigure(2, weight=1)
        
        # Botão Cadastrar
        self.btn_cadastrar = self.criar_botao_moderno(
            botoes_frame, "✓ CADASTRAR", 
            self.cores['success'], self.cores['success_hover'],
            self.cadastrar_cliente
        )
        self.btn_cadastrar.grid(row=0, column=0, sticky='ew', padx=(0, 5), pady=8)
        
        # Botão Limpar
        self.btn_limpar = self.criar_botao_moderno(
            botoes_frame, "⟲ LIMPAR",
            self.cores['warning'], self.cores['warning_hover'],
            self.limpar_campos
        )
        self.btn_limpar.grid(row=0, column=1, sticky='ew', padx=5, pady=8)
        
        # Botão Voltar
        self.btn_voltar = self.criar_botao_moderno(
            botoes_frame, "← VOLTAR",
            self.cores['danger'], self.cores['danger_hover'],
            self.voltar
        )
        self.btn_voltar.grid(row=0, column=2, sticky='ew', padx=(5, 0), pady=8)
    
    def aplicar_animacoes(self):
        # Animação de entrada suave
        self.container_principal.configure(bg=self.cores['bg_card'])
        self.master.after(50, lambda: self.animar_entrada())
    
    def animar_entrada(self):
        # Efeito fade-in simulado
        pass
    
    def validar_cpf(self, cpf):
        """Valida se o CPF está no formato correto"""
        numeros = re.sub(r'\D', '', cpf)
        
        if len(numeros) != 11:
            return False
        
        if numeros == numeros[0] * 11:
            return False
        
        # Validação matemática do CPF
        def calcular_digito(cpf_base, multiplicadores):
            soma = sum(int(cpf_base[i]) * multiplicadores[i] for i in range(len(cpf_base)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        primeiro_digito = calcular_digito(numeros[:9], list(range(10, 1, -1)))
        segundo_digito = calcular_digito(numeros[:10], list(range(11, 1, -1)))
        
        return numeros[9] == str(primeiro_digito) and numeros[10] == str(segundo_digito)
    
    def validar_telefone(self, telefone):
        """Valida se o telefone está no formato correto"""
        numeros = re.sub(r'\D', '', telefone)
        return len(numeros) in [10, 11]
    
    def conectar_bd(self):
        """Conecta ao banco de dados MySQL"""
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                database='lanchonete_db',
                user='emporioDoSabor',
                password='admin321@s',
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            return conexao
        except Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados:\n{e}")
            return None
    
    def mostrar_notificacao(self, tipo, titulo, mensagem):
        """Mostra notificações modernas"""
        if tipo == "sucesso":
            messagebox.showinfo(titulo, mensagem)
        elif tipo == "erro":
            messagebox.showerror(titulo, mensagem)
        elif tipo == "aviso":
            messagebox.showwarning(titulo, mensagem)
    
    def cadastrar_cliente(self):
        """Cadastra o cliente no banco de dados"""
        # Obter dados dos campos
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get(1.0, tk.END).strip()
        
        # Validações
        if not nome:
            self.mostrar_notificacao("erro", "Campo Obrigatório", "Por favor, preencha o nome do cliente.")
            self.entry_nome.focus()
            return
        
        if not cpf:
            self.mostrar_notificacao("erro", "Campo Obrigatório", "Por favor, preencha o CPF do cliente.")
            self.entry_cpf.focus()
            return
        
        if not self.validar_cpf(cpf):
            self.mostrar_notificacao("erro", "CPF Inválido", "Por favor, digite um CPF válido.")
            self.entry_cpf.focus()
            return
        
        if not telefone:
            self.mostrar_notificacao("erro", "Campo Obrigatório", "Por favor, preencha o telefone do cliente.")
            self.entry_telefone.focus()
            return
        
        if not self.validar_telefone(telefone):
            self.mostrar_notificacao("erro", "Telefone Inválido", "Por favor, digite um telefone válido.")
            self.entry_telefone.focus()
            return
        
        if not endereco:
            self.mostrar_notificacao("erro", "Campo Obrigatório", "Por favor, preencha o endereço do cliente.")
            self.entry_endereco.focus()
            return
        
        # Conectar ao banco de dados
        conexao = self.conectar_bd()
        if not conexao:
            return
        
        try:
            cursor = conexao.cursor()
            
            # Verificar se CPF já existe
            cpf_numeros = re.sub(r'\D', '', cpf)
            cursor.execute("SELECT id FROM clientes WHERE cpf = %s", (cpf_numeros,))
            if cursor.fetchone():
                self.mostrar_notificacao("erro", "CPF Duplicado", "Este CPF já está cadastrado no sistema.")
                self.entry_cpf.focus()
                return
            
            # Inserir novo cliente
            query = """
                INSERT INTO clientes (nome, cpf, telefone, endereco)
                VALUES (%s, %s, %s, %s)
            """
            valores = (nome, cpf_numeros, re.sub(r'\D', '', telefone), endereco)
            
            cursor.execute(query, valores)
            conexao.commit()
            
            self.mostrar_notificacao("sucesso", "Sucesso!", f"Cliente '{nome}' cadastrado com sucesso!")
            self.limpar_campos()
            
        except Error as e:
            self.mostrar_notificacao("erro", "Erro no Banco", f"Erro ao cadastrar cliente:\n{e}")
            
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_endereco.delete(1.0, tk.END)
        self.entry_nome.focus()
    
    def voltar(self):
        """Fecha a janela de cadastro"""
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    TelaCadastroCliente(root)
    root.mainloop()