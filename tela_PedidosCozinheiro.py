# tela_PedidosCozinheiro.py
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime
from pathlib import Path

class TelaPedidosCozinheiro:
    def __init__(self, master, ao_sair_callback, tela_garcom=None, tela_viagem=None):
        self.master = master
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")
        self.ao_sair_callback = ao_sair_callback
        self.tela_garcom = tela_garcom  # Referência para a tela do garçom
        self.tela_viagem = tela_viagem  # NOVO: Referência para a tela de viagem
        self.master.title("Pedidos da Cozinha - Empório do Sabor")
        self.master.geometry("900x700")  # Aumentado para acomodar novos elementos
        self.master.configure(bg="#f5f5f5")
        self.master.resizable(True, True)
        
        # Centralizar a janela
        self.centralizar_janela()
        
        # Configurar o protocolo de fechamento da janela
        self.master.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        
        # Criar interface
        self.criar_interface()
        
        # Atualizar pedidos inicialmente
        self.atualizar_comandas()
        
        # Configurar atualização automática a cada 10 segundos
        self.agendar_atualizacao()

    def centralizar_janela(self):
        largura_janela = 900
        altura_janela = 700
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    def criar_interface(self):
        # Frame do cabeçalho
        frame_cabecalho = tk.Frame(self.master, bg="#4E51F6", height=80)
        frame_cabecalho.pack(fill="x", padx=0, pady=0)
        frame_cabecalho.pack_propagate(False)
        
        # Título
        titulo = tk.Label(
            frame_cabecalho, 
            text="🍳 PEDIDOS DA COZINHA", 
            font=("Arial", 18, "bold"), 
            bg="#4E51F6", 
            fg="white"
        )
        titulo.pack(pady=20)
        
        # Frame para botões de controle
        frame_controles = tk.Frame(self.master, bg="#f5f5f5")
        frame_controles.pack(fill="x", padx=20, pady=10)
        
        # Botão de atualizar manual
        self.btn_atualizar = tk.Button(
            frame_controles,
            text="🔄 Atualizar",
            font=("Arial", 10, "bold"),
            bg="#28a745",
            fg="white",
            padx=15,
            pady=5,
            command=self.atualizar_comandas,
            relief="flat",
            cursor="hand2"
        )
        self.btn_atualizar.pack(side="left")
        
        # NOVO: Filtros de tipo de pedido
        frame_filtros = tk.Frame(frame_controles, bg="#f5f5f5")
        frame_filtros.pack(side="left", padx=(20, 0))
        
        tk.Label(
            frame_filtros,
            text="Mostrar:",
            font=("Arial", 10),
            bg="#f5f5f5"
        ).pack(side="left")
        
        self.var_mostrar_mesa = tk.BooleanVar(value=True)
        self.var_mostrar_viagem = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            frame_filtros,
            text="Mesa",
            variable=self.var_mostrar_mesa,
            command=self.atualizar_comandas,
            bg="#f5f5f5",
            font=("Arial", 9)
        ).pack(side="left", padx=5)
        
        tk.Checkbutton(
            frame_filtros,
            text="Viagem",
            variable=self.var_mostrar_viagem,
            command=self.atualizar_comandas,
            bg="#f5f5f5",
            font=("Arial", 9)
        ).pack(side="left")
        
        # Label de status
        self.label_status = tk.Label(
            frame_controles,
            text="Última atualização: Carregando...",
            font=("Arial", 9),
            bg="#f5f5f5",
            fg="#666"
        )
        self.label_status.pack(side="right")
        
        # Frame principal com scrollbar
        self.frame_principal = tk.Frame(self.master, bg="#f5f5f5")
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas e Scrollbar para rolagem
        self.canvas = tk.Canvas(self.frame_principal, bg="#f5f5f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame_principal, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f5f5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind do scroll do mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Frame de rodapé
        frame_rodape = tk.Frame(self.master, bg="#f5f5f5")
        frame_rodape.pack(fill="x", padx=20, pady=10)
        
        # Botão Fechar
        self.btn_fechar = tk.Button(
            frame_rodape,
            text="Fechar",
            font=("Arial", 12, "bold"),
            bg="#dc3545",
            fg="white",
            padx=20,
            pady=8,
            command=self.fechar_janela,
            relief="flat",
            cursor="hand2"
        )
        self.btn_fechar.pack(side="right")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def atualizar_comandas(self):
        # Limpar frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="emporioDoSabor",
                password="admin321@s",
                database="lanchonete_db"
            )
            cursor = conn.cursor(dictionary=True)

            # MODIFICADO: Query para incluir pedidos de viagem
            condicoes = []
            if self.var_mostrar_mesa.get():
                condicoes.append("p.numero_mesa IS NOT NULL")
            if self.var_mostrar_viagem.get():
                condicoes.append("p.numero_mesa IS NULL")
            
            if not condicoes:
                # Se nenhum filtro selecionado, mostrar mensagem
                self.mostrar_sem_pedidos()
                return
            
            where_clause = f"({' OR '.join(condicoes)})"
            
            cursor.execute(f"""
                SELECT p.* FROM pedidos p
                WHERE (p.status IS NULL OR p.status NOT IN ('finalizado', 'finalizado_cozinha'))
                AND {where_clause}
                ORDER BY 
                    CASE WHEN p.numero_mesa IS NULL THEN 0 ELSE 1 END,
                    p.id ASC
            """)
            pedidos = cursor.fetchall()

            if not pedidos:
                # Se não há pedidos, mostrar mensagem
                self.mostrar_sem_pedidos()
            else:
                for pedido in pedidos:
                    self.criar_card_pedido(pedido, cursor)
        
            # Atualizar status
            agora = datetime.now().strftime("%H:%M:%S")
            self.label_status.config(text=f"Última atualização: {agora}")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar pedidos:\n{e}", parent=self.master)
            self.label_status.config(text="Erro na atualização!")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def mostrar_sem_pedidos(self):
        frame_vazio = tk.Frame(self.scrollable_frame, bg="#f5f5f5")
        frame_vazio.pack(fill="x", pady=50)
        
        tk.Label(
            frame_vazio,
            text="🍽️ Nenhum pedido pendente na cozinha",
            font=("Arial", 16),
            bg="#f5f5f5",
            fg="#666"
        ).pack()
        
        tk.Label(
            frame_vazio,
            text="Todos os pedidos foram finalizados ou não há pedidos ativos!",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#999"
        ).pack(pady=5)

    def criar_card_pedido(self, pedido, cursor):
        id_pedido = pedido['id']
        numero_mesa = pedido.get('numero_mesa')
        cliente_nome = pedido.get('cliente', '')
        cliente_telefone = pedido.get('telefone', '')
        observacoes = pedido.get('observacoes', '')  # Obter observações do pedido
    
        # Determinar se é pedido de viagem ou mesa
        is_viagem = numero_mesa is None
    
        # Frame do card do pedido com cor diferente para viagem
        cor_fundo = "#fff3cd" if is_viagem else "white"  # Amarelo claro para viagem
        cor_borda = "#856404" if is_viagem else "#dee2e6"
    
        frame_card = tk.Frame(
            self.scrollable_frame, 
            bd=2, 
            relief="solid", 
            bg=cor_fundo,
            padx=15,
            pady=15,
            highlightbackground=cor_borda,
            highlightthickness=2
        )
        frame_card.pack(pady=8, fill="x", ipady=5)
    
        # Cabeçalho do pedido
        frame_cabecalho_pedido = tk.Frame(frame_card, bg=cor_fundo)
        frame_cabecalho_pedido.pack(fill="x", pady=(0, 10))
    
        # Título diferente para viagem
        if is_viagem:
            titulo_texto = "🚗 PEDIDO VIAGEM"
            info_adicional = f"Cliente: {cliente_nome.split()[0]}" if cliente_nome else "Cliente não informado"
        else:
            titulo_texto = f"🍽️ MESA {numero_mesa}"
            info_adicional = f"Pedido #{id_pedido}"
    
        tk.Label(
            frame_cabecalho_pedido, 
            text=titulo_texto, 
            font=("Arial", 16, "bold"), 
            bg=cor_fundo,
            fg="#2c3e50"
        ).pack(side="left")
    
        tk.Label(
            frame_cabecalho_pedido,
            text=info_adicional,
            font=("Arial", 10),
            bg=cor_fundo,
            fg="#7f8c8d"
        ).pack(side="right")
    
        # NOVO: Mostrar telefone para pedidos de viagem
        if is_viagem and cliente_telefone:
            tk.Label(
                frame_cabecalho_pedido,
                text=f"📱 {cliente_telefone}",
                font=("Arial", 9),
                bg=cor_fundo,
                fg="#7f8c8d"
            ).pack(side="right", padx=(10, 0))
    
        # NOVO: Exibir observações se existirem
        if observacoes and observacoes.strip():
            frame_observacoes = tk.Frame(frame_card, bg=cor_fundo)
            frame_observacoes.pack(fill="x", pady=(0, 10))
        
            tk.Label(
                frame_observacoes,
                text="📝 Observações:",
                font=("Arial", 10, "bold"),
                bg=cor_fundo,
                fg="#e67e22"  # Cor laranja para destacar
            ).pack(anchor="w")
        
            # Texto das observações com quebra de linha
            texto_obs = tk.Text(
                frame_observacoes,
                height=2,  # Altura mínima
                font=("Arial", 9),
                bg="#f8f9fa",
                fg="#2c3e50",
                wrap="word",
                relief="flat",
                padx=5,
                pady=5,
                state="disabled"  # Somente leitura
            )
            texto_obs.pack(fill="x", pady=(2, 0))
        
            # Inserir o texto das observações
            texto_obs.config(state="normal")
            texto_obs.insert("1.0", observacoes.strip())
            texto_obs.config(state="disabled")
        
            # Ajustar altura baseada no conteúdo
            linhas = observacoes.count('\n') + 1
            if linhas > 2:
                texto_obs.config(height=min(linhas, 4))  # Máximo 4 linhas
    
        # Separador
        separador = tk.Frame(frame_card, height=1, bg="#ecf0f1")
        separador.pack(fill="x", pady=(0, 10))
    
        # Buscar itens do pedido
        cursor.execute("""
            SELECT p.nome, i.quantidade, i.valor_total
            FROM itens_pedido i
            JOIN produtos p ON i.id_produto = p.id
            WHERE i.id_pedido = %s
        """, (id_pedido,))
        itens = cursor.fetchall()
    
        # Frame dos itens
        frame_itens = tk.Frame(frame_card, bg=cor_fundo)
        frame_itens.pack(fill="x", pady=(0, 15))
    
        total_pedido = 0
        for item in itens:
            frame_item = tk.Frame(frame_itens, bg=cor_fundo)
            frame_item.pack(fill="x", pady=2)
        
            # Nome e quantidade
            texto_item = f"• {item['nome']} x{item['quantidade']}"
            tk.Label(
                frame_item, 
                text=texto_item, 
                font=("Arial", 12, "bold"), 
                bg=cor_fundo,
                fg="#2c3e50"
            ).pack(side="left", anchor="w")
        
            # Valor
            tk.Label(
                frame_item,
                text=f"R$ {item['valor_total']:.2f}",
                font=("Arial", 12, "bold"),
                bg=cor_fundo,
                fg="#27ae60"
            ).pack(side="right")
        
            total_pedido += item['valor_total']
    
        # Total do pedido
        frame_total = tk.Frame(frame_card, bg=cor_fundo)
        frame_total.pack(fill="x", pady=(10, 15))
    
        separador2 = tk.Frame(frame_total, height=1, bg="#ecf0f1")
        separador2.pack(fill="x", pady=(0, 8))
    
        tk.Label(
            frame_total,
            text=f"TOTAL: R$ {total_pedido:.2f}",
            font=("Arial", 14, "bold"),
            bg=cor_fundo,
            fg="#e74c3c"
        ).pack(side="right")
    
        # Botão finalizar
        btn_finalizar = tk.Button(
            frame_card,
            text="✅ FINALIZAR PEDIDO",
            bg="#28a745",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2",
            command=lambda: self.finalizar_pedido(id_pedido, numero_mesa, frame_card, is_viagem)
        )
        btn_finalizar.pack(pady=(0, 5))

    def descontar_estoque(self, id_pedido, cursor):
        """
        Desconta os itens do pedido do estoque dos produtos e registra a saída na tabela 'estoque'
        """
        try:
            # CORRIGIDO: Agrupar itens por produto e somar as quantidades
            cursor.execute("""
                SELECT i.id_produto, SUM(i.quantidade) as quantidade_total, p.nome, p.estoque
                FROM itens_pedido i
                JOIN produtos p ON i.id_produto = p.id
                WHERE i.id_pedido = %s
                GROUP BY i.id_produto, p.nome, p.estoque
            """, (id_pedido,))
            
            itens_pedido = cursor.fetchall()
            produtos_sem_estoque = []
            
            # Verificar se há estoque suficiente para todos os itens
            for item in itens_pedido:
                id_produto = item['id_produto']
                quantidade_total = item['quantidade_total']  # MUDOU: agora usa quantidade_total
                estoque_atual = item['estoque']
                nome_produto = item['nome']
                
                if estoque_atual < quantidade_total:
                    produtos_sem_estoque.append(f"• {nome_produto}: Estoque atual ({estoque_atual}) menor que a quantidade total pedida ({quantidade_total})")
            
            # Se houver produtos sem estoque suficiente, mostrar erro
            if produtos_sem_estoque:
                erro_msg = "Não é possível finalizar o pedido. Estoque insuficiente:\n\n" + "\n".join(produtos_sem_estoque)
                messagebox.showerror("Estoque Insuficiente", erro_msg, parent=self.master)
                return False
            
            # Se chegou até aqui, há estoque suficiente para todos os itens
            for item in itens_pedido:
                id_produto = item['id_produto']
                quantidade_total = item['quantidade_total']  # MUDOU: agora usa quantidade_total
                estoque_atual = item['estoque']
                novo_estoque = estoque_atual - quantidade_total
                
                # Atualizar o estoque no produto
                cursor.execute("""
                    UPDATE produtos 
                    SET estoque = %s 
                    WHERE id = %s
                """, (novo_estoque, id_produto))

                # Inserir movimentação de saída na tabela 'estoque'
                cursor.execute("""
                    INSERT INTO estoque (id_produto, quantidade_entrada, quantidade_saida)
                    VALUES (%s, %s, %s)
                """, (id_produto, 0, quantidade_total))  # MUDOU: usa quantidade_total

            return True

        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao descontar estoque:\n{e}", parent=self.master)
            return False

    def finalizar_pedido(self, id_pedido, numero_mesa, frame_card, is_viagem=False):
        # Garantir que a janela de pedidos fique à frente
        self.master.lift()
        self.master.focus_force()
        
        # MODIFICADO: Mensagem diferente para pedidos de viagem
        tipo_pedido = "viagem" if is_viagem else f"Mesa {numero_mesa}"
        mensagem = f"Confirma a finalização do pedido #{id_pedido}"
        if is_viagem:
            mensagem += " (VIAGEM)?"
        else:
            mensagem += f" da {tipo_pedido}?"
        mensagem += "\n\nEste pedido será marcado como pronto e os itens serão descontados do estoque."
        
        resposta = messagebox.askyesno(
            "Finalizar Pedido",
            mensagem,
            parent=self.master
        )
        
        if resposta:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="emporioDoSabor",
                    password="admin321@s",
                    database="lanchonete_db"
                )
                cursor = conn.cursor(dictionary=True)
                
                # Primeiro, tentar descontar do estoque
                if not self.descontar_estoque(id_pedido, cursor):
                    # Se não conseguiu descontar do estoque, não finaliza o pedido
                    return
                
                # Se conseguiu descontar do estoque, atualizar status do pedido
                cursor.execute(
                    "UPDATE pedidos SET status = 'finalizado_cozinha' WHERE id = %s",
                    (id_pedido,)
                )
                conn.commit()
                
                # MODIFICADO: Notificar a tela apropriada sobre a mudança de status
                if is_viagem and self.tela_viagem:
                    # Notificar tela de viagem
                    self.tela_viagem.atualizar_status_pedido(id_pedido, 'pronto')
                elif not is_viagem and self.tela_garcom:
                    # Notificar tela do garçom
                    self.tela_garcom.atualizar_indicador_status(numero_mesa, 'finalizado_cozinha')
                
                # Remover visualmente o card
                frame_card.destroy()
                
                messagebox.showinfo(
                    "Sucesso", 
                    f"Pedido #{id_pedido} {'de viagem' if is_viagem else f'da {tipo_pedido}'} finalizado com sucesso!\nItens descontados do estoque.", 
                    parent=self.master
                )
                
                # Verificar se ainda há pedidos
                self.verificar_pedidos_restantes()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Erro", f"Erro ao finalizar pedido:\n{e}", parent=self.master)
                # Em caso de erro, fazer rollback se necessário
                if 'conn' in locals() and conn.is_connected():
                    conn.rollback()
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()

    def verificar_pedidos_restantes(self):
        # Se não há mais cards de pedidos, mostrar mensagem
        if not self.scrollable_frame.winfo_children():
            self.mostrar_sem_pedidos()

    def agendar_atualizacao(self):
        # Atualizar a cada 10 segundos (10000 ms)
        self.master.after(10000, self.atualizar_e_reagendar)

    def atualizar_e_reagendar(self):
        self.atualizar_comandas()
        self.agendar_atualizacao()

    # NOVO: Método para ser chamado pela tela de viagem quando um novo pedido é criado
    def novo_pedido_viagem_criado(self):
        """
        Método chamado quando um novo pedido de viagem é criado
        para atualizar imediatamente a tela da cozinha
        """
        self.atualizar_comandas()

    def fechar_janela(self):
        self.master.unbind_all("<MouseWheel>")  # Remove o bind do scroll
        self.ao_sair_callback()

if __name__ == "__main__":
    # Teste da tela
    root = tk.Tk()
    def fechar():
        root.destroy()
    
    TelaPedidosCozinheiro(root, fechar)
    root.mainloop()