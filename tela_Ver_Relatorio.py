import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from pathlib import Path

class ModernButton(tk.Frame):
    def __init__(self, parent, text, command, bg_color="#4a9eff", hover_color="#6bb6ff", **kwargs):
        super().__init__(parent, bg=parent.cget('bg') if hasattr(parent, 'cget') else '#0d1117')
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        
        # Criar botão
        self.button = tk.Button(
            self,
            text=text,
            command=command,
            bg=bg_color,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.button.pack()
        
        # Bind para efeitos hover
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event):
        self.button.config(bg=self.hover_color)
        
    def on_leave(self, event):
        self.button.config(bg=self.bg_color)

class ModernCard(tk.Frame):
    def __init__(self, parent, title, value, description, icon, color="#4a9eff", **kwargs):
        super().__init__(parent, bg="#21262d", relief="raised", bd=1, **kwargs)
        self.color = color
        self.title = title
        self.value = value
        self.description = description
        self.icon = icon
        
        # Definir tamanho fixo para os cards
        self.configure(width=200, height=120)
        self.pack_propagate(False)
        
        self.create_card()
        
    def create_card(self):
        # Container principal
        main_container = tk.Frame(self, bg="#21262d")
        main_container.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Header do card 
        header_frame = tk.Frame(main_container, bg="#21262d")
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Ícone e título
        tk.Label(header_frame, text=self.icon, font=("Segoe UI", 14), 
                fg="white", bg="#21262d").pack(side="left")
        
        tk.Label(header_frame, text=self.title, font=("Segoe UI", 10, "bold"), 
                fg="white", bg="#21262d").pack(side="left", padx=(8, 0))
        
        # Valor principal
        self.value_label = tk.Label(main_container, text=self.value, 
                                   font=("Segoe UI", 14, "bold"), 
                                   fg="white", bg="#21262d")
        self.value_label.pack(pady=(5, 3))
        
        # Descrição
        self.desc_label = tk.Label(main_container, text=self.description, 
                                  font=("Segoe UI", 8), 
                                  fg="#8b949e", bg="#21262d")
        self.desc_label.pack()
        
        # Linha decorativa
        line_frame = tk.Frame(main_container, bg=self.color, height=2)
        line_frame.pack(fill="x", pady=(5, 0))
    
    def update_value(self, new_value):
        self.value = new_value
        self.value_label.config(text=new_value)
    
    def update_description(self, new_description):
        self.description = new_description
        self.desc_label.config(text=new_description)

class TelaVerRelatorioModerna(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatórios Analytics - Empório do Sabor")
        self.geometry("1000x700")
        self.configure(bg="#0d1117")
        
        # Definir o ícone da janela
        try:
            caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
            if caminho_icone.exists():
                icone = tk.PhotoImage(file=str(caminho_icone))
                self.iconphoto(False, icone)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Centralizar janela
        self.centralizar_janela()
        
        # Período selecionado (padrão: Diário)
        self.periodo_selecionado = "Diário"
        
        # Cores do tema
        self.colors = {
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22',
            'bg_card': '#21262d',
            'accent_blue': '#58a6ff',
            'accent_green': '#3fb950',
            'accent_orange': '#ff7b00',
            'accent_purple': '#a855f7',
            'accent_red': '#f85149',
            'text_primary': '#f0f6fc',
            'text_secondary': '#8b949e'
        }
        
        # Criar interface
        self.criar_interface()
        
        # Carregar dados após a interface estar pronta
        self.after(100, self.atualizar_relatorio)

    def centralizar_janela(self):
        self.update_idletasks()
        largura_janela = 1000
        altura_janela = 700
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    def criar_interface(self):
        # Frame principal sem scroll - tudo em uma tela
        self.main_frame = tk.Frame(self, bg=self.colors['bg_primary'])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Header 
        self.criar_header()
        
        # Controles de período 
        self.criar_controles_periodo()
        
        # Cards de métricas
        self.criar_cards_metricas()
        
        # Seção de gráficos
        self.criar_secao_graficos()
        
        # Rodapé
        self.criar_rodape()

    def criar_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_secondary'], height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Título
        tk.Label(header_frame, text="📊 PAINEL DE CONTROLE", 
                font=("Segoe UI", 18, "bold"), fg=self.colors['text_primary'], 
                bg=self.colors['bg_secondary']).pack(expand=True)
        
        tk.Label(header_frame, text="Empório do Sabor", 
                font=("Segoe UI", 10), fg=self.colors['text_secondary'], 
                bg=self.colors['bg_secondary']).pack()

    def criar_controles_periodo(self):
        controles_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        controles_frame.pack(pady=10)
        
        tk.Label(controles_frame, text="📅 Período de Análise", 
                font=("Segoe UI", 12, "bold"), fg=self.colors['text_primary'], 
                bg=self.colors['bg_primary']).pack(pady=(0, 8))
        
        # Container para botões
        botoes_frame = tk.Frame(controles_frame, bg=self.colors['bg_primary'])
        botoes_frame.pack()
        
        # Botões de período compactos
        periodos = [
            ("Diário", self.colors['accent_red']),
            ("Semanal", self.colors['accent_orange']), 
            ("Mensal", self.colors['accent_blue']),
            ("Anual", self.colors['accent_purple'])
        ]
        
        self.botoes_periodo = {}
        for periodo, cor in periodos:
            hover_cor = self.lighten_color(cor, 0.2)
            btn = ModernButton(botoes_frame, periodo, 
                             lambda p=periodo: self.selecionar_periodo(p),
                             cor, hover_cor)
            btn.pack(side="left", padx=8)
            self.botoes_periodo[periodo] = btn
        
        # Label do período atual compacto
        self.label_periodo_atual = tk.Label(
            controles_frame,
            text=f"🔍 Visualizando: {self.periodo_selecionado}",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['accent_green'],
            bg=self.colors['bg_primary']
        )
        self.label_periodo_atual.pack(pady=(8, 0))

    def criar_cards_metricas(self):
        metricas_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        metricas_frame.pack(pady=15, fill="x")
        
        tk.Label(metricas_frame, text="📈 Métricas Principais", 
                font=("Segoe UI", 14, "bold"), fg=self.colors['text_primary'], 
                bg=self.colors['bg_primary']).pack(pady=(0, 10))
        
        # Container para cards - todos em linha horizontal
        cards_container = tk.Frame(metricas_frame, bg=self.colors['bg_primary'])
        cards_container.pack(expand=True)
        
        # Todos os cards em uma única linha horizontal
        self.card_financeiro = ModernCard(
            cards_container, "RECEITA", "Carregando...", "Total em pedidos", 
            "💰", self.colors['accent_green']
        )
        self.card_financeiro.pack(side="left", padx=8, fill="both", expand=True)
        
        self.card_clientes = ModernCard(
            cards_container, "CLIENTES", "Carregando...", "Cadastrados", 
            "👥", self.colors['accent_blue']
        )
        self.card_clientes.pack(side="left", padx=8, fill="both", expand=True)
        
        self.card_produtos = ModernCard(
            cards_container, "TOP PRODUTO", "Carregando...", "Mais vendido", 
            "🔥", self.colors['accent_orange']
        )
        self.card_produtos.pack(side="left", padx=8, fill="both", expand=True)
        
        self.card_funcionarios = ModernCard(
            cards_container, "EQUIPE", "Carregando...", "Funcionários", 
            "👨‍💼", self.colors['accent_purple']
        )
        self.card_funcionarios.pack(side="left", padx=8, fill="both", expand=True)

    def criar_secao_graficos(self):
        graficos_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        graficos_frame.pack(pady=15, fill="x")
        
        tk.Label(graficos_frame, text="📊 Análise de Tendências", 
                font=("Segoe UI", 14, "bold"), fg=self.colors['text_primary'], 
                bg=self.colors['bg_primary']).pack(pady=(0, 10))
        
        # Área do gráfico compacta
        grafico_frame = tk.Frame(graficos_frame, bg=self.colors['bg_card'], height=120)
        grafico_frame.pack(fill="x", padx=20)
        grafico_frame.pack_propagate(False)
        
        tk.Label(grafico_frame, text="📈 Gráfico de Pedidos por Período", 
                font=("Segoe UI", 12), fg=self.colors['text_primary'], 
                bg=self.colors['bg_card']).pack(expand=True)

    def criar_rodape(self):
        rodape_frame = tk.Frame(self.main_frame, bg=self.colors['bg_secondary'])
        rodape_frame.pack(fill="x", pady=(15, 0))
        
        acoes_frame = tk.Frame(rodape_frame, bg=self.colors['bg_secondary'])
        acoes_frame.pack(pady=15)
        
        # Botões de ação compactos
        ModernButton(acoes_frame, "📄 Exportar", self.exportar_relatorio,
                    self.colors['accent_blue']).pack(side="left", padx=8)
        
        ModernButton(acoes_frame, "🔄 Atualizar", self.atualizar_relatorio,
                    self.colors['accent_green']).pack(side="left", padx=8)
        
        ModernButton(acoes_frame, "❌ Fechar", self.destroy,
                    self.colors['accent_red']).pack(side="left", padx=8)

    def lighten_color(self, color, factor):
        """Clarear uma cor por um fator"""
        try:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = min(255, int(r + (255 - r) * factor))
            g = min(255, int(g + (255 - g) * factor))
            b = min(255, int(b + (255 - b) * factor))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color

    def selecionar_periodo(self, periodo):
        self.periodo_selecionado = periodo
        self.label_periodo_atual.config(text=f"🔍 Visualizando: {periodo}")
        self.atualizar_relatorio()

    def get_data_filtro(self):
        """Retorna as datas de início e fim baseadas no período selecionado"""
        hoje = datetime.now()
        
        if self.periodo_selecionado == "Diário":
            inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
            fim = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif self.periodo_selecionado == "Semanal":
            inicio = hoje - timedelta(days=hoje.weekday())
            inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
            fim = inicio + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        elif self.periodo_selecionado == "Mensal":
            inicio = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if hoje.month == 12:
                fim = hoje.replace(year=hoje.year+1, month=1, day=1) - timedelta(microseconds=1)
            else:
                fim = hoje.replace(month=hoje.month+1, day=1) - timedelta(microseconds=1)
        elif self.periodo_selecionado == "Anual":
            inicio = hoje.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            fim = hoje.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        
        return inicio, fim

    def atualizar_relatorio(self):
        """Atualiza todas as informações do relatório"""
        try:
            # Mostrar loading nos cards
            self.card_financeiro.update_value("Carregando...")
            self.card_clientes.update_value("Carregando...")
            self.card_produtos.update_value("Carregando...")
            self.card_funcionarios.update_value("Carregando...")
            
            # Atualizar interface
            self.update()
            
            # Conectar ao banco de dados
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor', 
                password='admin321@s', 
                database='lanchonete_db',  
                connection_timeout=5
            )
            cursor = conexao.cursor()

            # Obter filtro de data
            data_inicio, data_fim = self.get_data_filtro()

            # Atualizar todos os cards
            self.atualizar_financeiro(cursor, data_inicio, data_fim)
            self.atualizar_clientes(cursor)
            self.atualizar_produtos_alta(cursor, data_inicio, data_fim)
            self.atualizar_funcionarios(cursor)

        except Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar com o banco de dados:\n{e}")
            # Mostrar valores padrão em caso de erro
            self.card_financeiro.update_value("R$ 0,00")
            self.card_clientes.update_value("0")
            self.card_produtos.update_value("Sem dados")
            self.card_funcionarios.update_value("0")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def atualizar_financeiro(self, cursor, data_inicio, data_fim):
        """
        Como não há campo de data nos pedidos, vamos calcular o total geral
        Para implementar filtro por data, seria necessário adicionar uma coluna
        data_pedido na tabela pedidos
        """
        try:
            # Query para calcular receita total baseada nos itens dos pedidos
            cursor.execute("""
                SELECT COALESCE(SUM(ip.valor_total), 0) as total_receita 
                FROM itens_pedido ip
                INNER JOIN pedidos p ON ip.id_pedido = p.id
                WHERE p.status IN ('finalizado', 'pago')
            """)
            
            resultado = cursor.fetchone()
            total = resultado[0] if resultado else 0
            valor_formatado = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            self.card_financeiro.update_value(valor_formatado)
            self.card_financeiro.update_description("Total em pedidos finalizados")
        except Error as e:
            print(f"Erro ao atualizar financeiro: {e}")
            self.card_financeiro.update_value("R$ 0,00")

    def atualizar_clientes(self, cursor):
        try:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            resultado = cursor.fetchone()
            total_clientes = resultado[0] if resultado else 0
            
            self.card_clientes.update_value(str(total_clientes))
            self.card_clientes.update_description("Total cadastrados")
        except Error as e:
            print(f"Erro ao atualizar clientes: {e}")
            self.card_clientes.update_value("0")

    def atualizar_produtos_alta(self, cursor, data_inicio, data_fim):
        """
        Produto mais vendido baseado na quantidade total vendida
        """
        try:
            cursor.execute("""
                SELECT p.nome, SUM(ip.quantidade) as total_vendido
                FROM produtos p
                INNER JOIN itens_pedido ip ON p.id = ip.id_produto
                INNER JOIN pedidos ped ON ip.id_pedido = ped.id
                WHERE ped.status IN ('finalizado', 'pago')
                GROUP BY p.id, p.nome
                ORDER BY total_vendido DESC
                LIMIT 1
            """)
            
            resultado = cursor.fetchone()
            if resultado:
                produto_nome, quantidade = resultado
                # Limitar o nome do produto para caber no card
                if len(produto_nome) > 15:
                    produto_nome = produto_nome[:12] + "..."
                self.card_produtos.update_value(produto_nome)
                self.card_produtos.update_description(f"Vendidos: {quantidade} un.")
            else:
                self.card_produtos.update_value("Sem dados")
                self.card_produtos.update_description("Nenhuma venda registrada")
        except Error as e:
            print(f"Erro ao atualizar produtos: {e}")
            self.card_produtos.update_value("Sem dados")

    def atualizar_funcionarios(self, cursor):
        try:
            cursor.execute("SELECT COUNT(*) FROM funcionarios")
            resultado = cursor.fetchone()
            total_funcionarios = resultado[0] if resultado else 0
            
            self.card_funcionarios.update_value(str(total_funcionarios))
            self.card_funcionarios.update_description("Total na equipe")
        except Error as e:
            print(f"Erro ao atualizar funcionários: {e}")
            self.card_funcionarios.update_value("0")

    def exportar_relatorio(self):
        """
        Função para exportar relatório - implementação básica
        Você pode expandir para exportar para PDF, Excel, etc.
        """
        try:
            # Conectar ao banco
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            
            # Coletar dados para exportação
            dados_relatorio = self.coletar_dados_exportacao(cursor)
            
            # Por enquanto, apenas mostrar uma mensagem
            messagebox.showinfo("Exportar", 
                               f"Relatório coletado com sucesso!\n"
                               f"Clientes: {dados_relatorio['total_clientes']}\n"
                               f"Funcionários: {dados_relatorio['total_funcionarios']}\n"
                               f"Produtos cadastrados: {dados_relatorio['total_produtos']}\n"
                               f"Pedidos: {dados_relatorio['total_pedidos']}")
            
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {e}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def coletar_dados_exportacao(self, cursor):
        """Coleta dados para exportação"""
        dados = {}
        
        # Total de clientes
        cursor.execute("SELECT COUNT(*) FROM clientes")
        dados['total_clientes'] = cursor.fetchone()[0]
        
        # Total de funcionários
        cursor.execute("SELECT COUNT(*) FROM funcionarios")
        dados['total_funcionarios'] = cursor.fetchone()[0]
        
        # Total de produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        dados['total_produtos'] = cursor.fetchone()[0]
        
        # Total de pedidos
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        dados['total_pedidos'] = cursor.fetchone()[0]
        
        return dados

# Teste da aplicação
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    tela = TelaVerRelatorioModerna(root)
    tela.mainloop()