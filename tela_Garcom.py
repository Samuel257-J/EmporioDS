import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
from pathlib import Path
from utilitarios import carregar_imagem_tk  

class TelaGarcom:
    def __init__(self, master, ao_sair_callback, tela_cozinheiro):
        self.master = master
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")
        self.ao_sair_callback = ao_sair_callback
        self.tela_cozinheiro = tela_cozinheiro
        self.master.title("GARÇOM - Empório do Sabor")
        self.master.geometry("425x582")
        self.master.resizable(False, False)
        print("TelaGarcom aberta")

        largura_janela = 425
        altura_janela = 582
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        try:
            self.fundo = carregar_imagem_tk("telaGarcom.png", (425, 582))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=425, height=582, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        try:
            self.img_mesa_padrao = carregar_imagem_tk("mesaEmporio.png", (80, 80))
            self.img_mesa_vermelha = carregar_imagem_tk("mesaEmporioVermelha.png", (80, 80))
            self.img_mesa_verde = carregar_imagem_tk("mesaEmporioVerde.png", (80, 80))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagens das mesas:\n{e}")
            return

        self.status_mesas = {}
        self.pedidos_por_mesa = {}
        self.observacoes_por_mesa = {}  # Para armazenar observações por mesa
        self.botoes_mesa = []
        self.indicadores_status = {}  # Rara armazenar os indicadores visuais

        largura_mesa = 50
        altura_mesa = 50
        espacamento_x = 40
        espacamento_y = 40
        inicio_x = 123
        inicio_y = 225

        mesa_numero = 1

        for linha in range(3):
            for coluna in range(3):
                x = inicio_x + coluna * (largura_mesa + espacamento_x)
                y = inicio_y + linha * (altura_mesa + espacamento_y)

                frame_mesa = tk.Frame(self.canvas, width=largura_mesa, height=altura_mesa)
                frame_mesa.pack_propagate(False)

                num_mesa = mesa_numero
                self.status_mesas[num_mesa] = "livre"

                botao = tk.Button(
                    frame_mesa,
                    image=self.img_mesa_padrao,
                    bd=0,
                    highlightthickness=0,
                    relief="flat",
                    command=lambda m=num_mesa: self.abrir_mesa(m)
                )
                botao.pack()

                label_numero = tk.Label(
                    frame_mesa,
                    text=str(mesa_numero).zfill(2),
                    font=("Arial", 9, "bold"),
                    bg="#C9772E",
                    fg="black"
                )
                label_numero.place(relx=0.5, rely=0.8, anchor="center")

                # NOVO: Criar indicador de status (inicialmente invisível)
                indicador = tk.Label(
                    frame_mesa,
                    text="",
                    font=("Arial", 12, "bold"),
                    bg="white",
                    fg="black",
                    width=3,
                    height=1,
                    relief="solid",
                    bd=1
                )
                indicador.place(relx=0.85, rely=0.15, anchor="center")
                indicador.place_forget()  # Inicialmente invisível
                
                self.indicadores_status[num_mesa] = indicador

                self.canvas.create_window(x, y, window=frame_mesa, width=largura_mesa, height=altura_mesa)
                self.botoes_mesa.append((botao, num_mesa, label_numero))

                mesa_numero += 1

        self.botao_sair_conta = tk.Button(
            self.canvas,
            text="Sair",
            font=("Arial", 8, "bold"),
            bg="#CE0707",
            fg="white",
            width=8,
            height=1,
            command=self.sair_conta
        )
        self.canvas.create_window(50, 30, window=self.botao_sair_conta)
        
        # NOVA FUNCIONALIDADE: Carrega os pedidos ativos ao inicializar
        self.carregar_pedidos_ativos()
        
        # NOVO: Iniciar verificação automática do status dos pedidos
        self.verificar_status_pedidos()

    def carregar_pedidos_ativos(self):
        """Carrega todos os pedidos ativos do banco e atualiza o status das mesas"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="emporioDoSabor",
                password="admin321@s",
                database="lanchonete_db"
            )
            cursor = conn.cursor(dictionary=True)
            
            # Busca todas as mesas que têm pedidos ativos (não finalizados)
            cursor.execute("""
                SELECT DISTINCT numero_mesa, status, observacoes
                FROM pedidos 
                WHERE status IS NULL OR status NOT IN ('finalizado')
            """)
            
            mesas_ocupadas = cursor.fetchall()
            
            for mesa in mesas_ocupadas:
                numero_mesa = mesa['numero_mesa']
                status_pedido = mesa['status']
                observacoes = mesa['observacoes'] or ""  # Carrega observações
                
                # Carrega os pedidos desta mesa
                pedidos = self.carregar_pedido_do_banco(numero_mesa)
                
                if pedidos:
                    # Atualiza o status e os pedidos da mesa
                    self.status_mesas[numero_mesa] = "ocupada"
                    self.pedidos_por_mesa[numero_mesa] = pedidos
                    self.observacoes_por_mesa[numero_mesa] = observacoes  # Armazena observações
                    
                    # Atualiza a cor da mesa para vermelha (ocupada)
                    self.atualizar_cor_mesa(numero_mesa)
                    
                    # NOVO: Atualiza o indicador visual baseado no status do pedido
                    self.atualizar_indicador_status(numero_mesa, status_pedido)
            
            print(f"Carregados pedidos ativos para {len(mesas_ocupadas)} mesas")
            
        except mysql.connector.Error as error:
            print(f"Erro ao carregar pedidos ativos: {error}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def atualizar_indicador_status(self, numero_mesa, status):
        """Atualiza o indicador visual da mesa baseado no status do pedido"""
        indicador = self.indicadores_status[numero_mesa]
    
        # Só atualiza o indicador se a mesa estiver ocupada
        if self.status_mesas[numero_mesa] != "ocupada":
            indicador.place_forget()
            return
    
        if status is None:
            # Pedido enviado para cozinha (preparando)
            indicador.config(text="...", bg="#FFA500", fg="black")  # Laranja com reticências
            indicador.place(relx=0.85, rely=0.15, anchor="center")
            print(f"Mesa {numero_mesa}: Indicador definido para preparando (...)")
        elif status == "finalizado_cozinha":
            # Pedido pronto na cozinha
            indicador.config(text="✓", bg="#28a745", fg="white")  # Verde com check
            indicador.place(relx=0.85, rely=0.15, anchor="center")
            print(f"Mesa {numero_mesa}: Indicador definido para pronto (✓)")
        elif status == "finalizado":
            # Pedido completamente finalizado
            indicador.place_forget()
            print(f"Mesa {numero_mesa}: Indicador removido (finalizado)")
        else:
            # Para debug: mostra status desconhecidos
            print(f"Mesa {numero_mesa}: Status desconhecido: {status}")
            # Mantém o indicador atual se o status for desconhecido

    def verificar_status_pedidos(self):
        """Verifica periodicamente o status dos pedidos no banco para atualizar os indicadores"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="emporioDoSabor",
                password="admin321@s",
                database="lanchonete_db"
            )
            cursor = conn.cursor(dictionary=True)
        
            # Busca o status atual de todas as mesas ocupadas
            for numero_mesa in self.status_mesas:
                if self.status_mesas[numero_mesa] == "ocupada":
                    cursor.execute("""
                        SELECT status FROM pedidos 
                        WHERE numero_mesa = %s 
                        AND (status IS NULL OR status != 'finalizado')
                        ORDER BY id DESC 
                        LIMIT 1
                    """, (numero_mesa,))
                
                    resultado = cursor.fetchone()
                    if resultado:
                        status_atual = resultado['status']
                        self.atualizar_indicador_status(numero_mesa, status_atual)
                    else:
                        # ALTERAÇÃO: Só remove o indicador se a mesa foi marcada como livre
                        # Isso evita que o indicador suma antes do cozinheiro finalizar
                        if self.status_mesas[numero_mesa] == "livre":
                            self.indicadores_status[numero_mesa].place_forget()
        
        except mysql.connector.Error as error:
            print(f"Erro ao verificar status dos pedidos: {error}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
        # Reagendar a verificação para daqui a 5 segundos
        self.master.after(5000, self.verificar_status_pedidos)

    def sair_conta(self):
        if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
            self.master.destroy()
            self.ao_sair_callback()

    def carregar_pedido_do_banco(self, numero_mesa):
        """Carrega o pedido mais recente da mesa do banco de dados"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="emporioDoSabor",
                password="admin321@s",
                database="lanchonete_db"
            )
            cursor = conn.cursor(dictionary=True)
            
            # Busca o pedido mais recente da mesa que ainda não foi finalizado
            cursor.execute("""
                SELECT p.id, p.numero_mesa, p.status, p.observacoes
                FROM pedidos p 
                WHERE p.numero_mesa = %s 
                AND (p.status IS NULL OR p.status != 'finalizado')
                ORDER BY p.id DESC 
                LIMIT 1
            """, (numero_mesa,))
            
            pedido = cursor.fetchone()
            
            if not pedido:
                return []
            
            # NOVO: Armazena as observações
            self.observacoes_por_mesa[numero_mesa] = pedido['observacoes'] or ""
            
            # Busca os itens do pedido
            cursor.execute("""
                SELECT pr.nome, ip.quantidade, ip.valor_total
                FROM itens_pedido ip
                JOIN produtos pr ON ip.id_produto = pr.id
                WHERE ip.id_pedido = %s
            """, (pedido['id'],))
            
            itens = cursor.fetchall()
            
            # Converte para o formato esperado
            pedidos = []
            for item in itens:
                pedidos.append({
                    "nome": item['nome'],
                    "qtd": int(item['quantidade']),
                    "total": float(item['valor_total'])
                })
            
            return pedidos
            
        except mysql.connector.Error as error:
            print(f"Erro ao carregar pedido do banco: {error}")
            return []
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def abrir_mesa(self, numero):
        from PIL import Image, ImageTk

        largura = 450  # AUMENTADO para acomodar observações
        altura = 650   # AUMENTADO para acomodar observações
        pos_x = self.master.winfo_x()
        pos_y = self.master.winfo_y()

        janela_pedido = tk.Toplevel(self.master)
        janela_pedido.title(f"Pedido - Mesa {numero}")
        janela_pedido.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        janela_pedido.resizable(False, False)

        # Frame principal com scroll
        main_frame = tk.Frame(janela_pedido, bg="#0A0B0A")
        main_frame.pack(fill="both", expand=True)

        # Canvas para o scroll
        canvas = tk.Canvas(main_frame, bg="#0A0B0A", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0A0B0A")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título
        tk.Label(scrollable_frame, text=f"Pedido para Mesa {numero}", 
                font=("Arial", 14, "bold"), bg="#0A0B0A", fg="white").pack(pady=10)

        # Frame para entrada de produtos
        frame_entrada = tk.Frame(scrollable_frame, bg="#0A0B0A")
        frame_entrada.pack(pady=10, padx=20, fill="x")

        # Campo de busca de produto com filtro melhorado
        tk.Label(frame_entrada, text="🔍 Buscar Produto:", 
                font=("Arial", 10, "bold"), bg="#0A0B0A", fg="white").pack(anchor="w")
        
        entrada_produto = tk.Entry(frame_entrada, font=("Arial", 10), width=40)
        entrada_produto.pack(pady=5, fill="x")

        # Frame para quantidade
        frame_qtd = tk.Frame(frame_entrada, bg="#0A0B0A")
        frame_qtd.pack(fill="x", pady=5)
        
        tk.Label(frame_qtd, text="Quantidade:", 
                font=("Arial", 10, "bold"), bg="#0A0B0A", fg="white").pack(side="left")
        entrada_qtd = tk.Entry(frame_qtd, font=("Arial", 10), width=8)
        entrada_qtd.pack(side="left", padx=(10, 0))
        entrada_qtd.insert(0, "1")  # Valor padrão

        # Listbox para sugestões de produtos
        frame_sugestoes = tk.Frame(scrollable_frame, bg="#0A0B0A")
        frame_sugestoes.pack(pady=5, padx=20, fill="x")
        
        sugestoes = tk.Listbox(frame_sugestoes, height=4, font=("Arial", 9))
        sugestoes.pack(fill="x")
        sugestoes.pack_forget()  # Inicialmente oculto

        # Frame para observações
        frame_observacoes = tk.Frame(scrollable_frame, bg="#0A0B0A")
        frame_observacoes.pack(pady=10, padx=20, fill="x")
        
        tk.Label(frame_observacoes, text="📝 Observações do Pedido:", 
                font=("Arial", 10, "bold"), bg="#0A0B0A", fg="white").pack(anchor="w")
        
        texto_observacoes = tk.Text(frame_observacoes, height=3, font=("Arial", 9), 
                                   wrap="word", bg="white", fg="black")
        texto_observacoes.pack(fill="x", pady=5)
        
        # Carrega observações existentes
        observacoes_existentes = self.observacoes_por_mesa.get(numero, "")
        if observacoes_existentes:
            texto_observacoes.insert("1.0", observacoes_existentes)

        # Frame para lista de pedidos
        frame_pedidos = tk.Frame(scrollable_frame, bg="#0A0B0A")
        frame_pedidos.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(frame_pedidos, text="🛒 Itens do Pedido:", 
                font=("Arial", 10, "bold"), bg="#0A0B0A", fg="white").pack(anchor="w")
        
        texto_pedido = tk.Text(frame_pedidos, height=10, font=("Arial", 9), 
                              bg="white", fg="black", state="disabled")
        texto_pedido.pack(fill="both", expand=True, pady=5)

        # Total
        total_var = tk.StringVar(value="Total: R$ 0,00")
        label_total = tk.Label(scrollable_frame, textvariable=total_var, 
                              font=("Arial", 12, "bold"), fg="#00FF00", bg="#0A0B0A")
        label_total.pack(pady=10)

        # Carrega pedidos existentes
        if self.status_mesas[numero] == "ocupada":
            pedidos = self.carregar_pedido_do_banco(numero)
            if pedidos:
                self.pedidos_por_mesa[numero] = pedidos
        else:
            pedidos = self.pedidos_por_mesa.get(numero, [])

        def buscar_produtos_filtro(termo):
            """Busca produtos no banco com filtro"""
            if not termo.strip():
                return []
            
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="emporioDoSabor",
                    password="admin321@s",
                    database="lanchonete_db"
                )
                cursor = conn.cursor(dictionary=True)
                
                # Busca por nome ou ID
                if termo.isdigit():
                    cursor.execute("SELECT * FROM produtos WHERE id = %s", (termo,))
                else:
                    cursor.execute("SELECT * FROM produtos WHERE nome LIKE %s ORDER BY nome", (f"%{termo}%",))
                
                return cursor.fetchall()
                
            except mysql.connector.Error as error:
                print(f"Erro ao buscar produtos: {error}")
                return []
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

        def atualizar_sugestoes(event):
            """Atualiza lista de sugestões conforme digitação"""
            termo = entrada_produto.get().strip()
            sugestoes.delete(0, tk.END)
            
            if not termo:
                sugestoes.pack_forget()
                return
            
            produtos = buscar_produtos_filtro(termo)
            
            if produtos:
                for produto in produtos[:10]:  # Limita a 10 resultados
                    texto = f"{produto['id']} - {produto['nome']} - R$ {produto['preco']:.2f}"
                    sugestoes.insert(tk.END, texto)
                
                sugestoes.pack(fill="x", pady=5)
            else:
                sugestoes.pack_forget()

        def selecionar_produto(event):
            """Seleciona produto da lista de sugestões"""
            if sugestoes.curselection():
                texto_selecionado = sugestoes.get(sugestoes.curselection())
                nome_produto = texto_selecionado.split(' - ')[1]
                entrada_produto.delete(0, tk.END)
                entrada_produto.insert(0, nome_produto)
                sugestoes.pack_forget()
                entrada_qtd.focus()

        # Bind eventos
        entrada_produto.bind("<KeyRelease>", atualizar_sugestoes)
        sugestoes.bind("<<ListboxSelect>>", selecionar_produto)
        
        # Enter para adicionar produto
        def adicionar_com_enter(event):
            adicionar_produto()
        
        entrada_qtd.bind("<Return>", adicionar_com_enter)

        def atualizar_total():
            total = sum(item["total"] for item in pedidos)
            total_var.set(f"Total: R$ {total:.2f}")

        def atualizar_texto():
            texto_pedido.config(state="normal")
            texto_pedido.delete(1.0, tk.END)
            
            if not pedidos:
                texto_pedido.insert(tk.END, "Nenhum item adicionado ainda...")
            else:
                for i, item in enumerate(pedidos, 1):
                    linha = f"{i:02d}. {item['nome']} x{item['qtd']} - R$ {item['total']:.2f}\n"
                    texto_pedido.insert(tk.END, linha)
            
            texto_pedido.config(state="disabled")
            atualizar_total()

        def adicionar_produto():
            termo = entrada_produto.get().strip()
            qtd_texto = entrada_qtd.get().strip()
            
            if not termo:
                messagebox.showwarning("Atenção", "Digite o nome ou ID do produto.")
                entrada_produto.focus()
                return
            
            if not qtd_texto.isdigit() or int(qtd_texto) <= 0:
                messagebox.showwarning("Atenção", "Digite uma quantidade válida.")
                entrada_qtd.focus()
                return

            produtos_encontrados = buscar_produtos_filtro(termo)
            
            if not produtos_encontrados:
                messagebox.showerror("Erro", "Produto não encontrado.")
                entrada_produto.focus()
                return
            
            # Se encontrou mais de um, pega o primeiro ou o que tem nome exato
            produto = None
            for p in produtos_encontrados:
                if p['nome'].lower() == termo.lower():
                    produto = p
                    break
            
            if not produto:
                produto = produtos_encontrados[0]

            qtd = int(qtd_texto)
            total_item = float(produto['preco']) * qtd
            
            # Verifica se o produto já existe no pedido
            produto_existente = None
            for item in pedidos:
                if item['nome'] == produto['nome']:
                    produto_existente = item
                    break
            
            if produto_existente:
                # Atualiza quantidade do produto existente
                produto_existente['qtd'] += qtd
                produto_existente['total'] += total_item
            else:
                # Adiciona novo produto
                pedidos.append({
                    "nome": produto['nome'], 
                    "qtd": qtd, 
                    "total": total_item
                })
            
            self.pedidos_por_mesa[numero] = pedidos
            atualizar_texto()

            # Limpa campos
            entrada_produto.delete(0, tk.END)
            entrada_qtd.delete(0, tk.END)
            entrada_qtd.insert(0, "1")
            entrada_produto.focus()
            sugestoes.pack_forget()

        def remover_ultimo():
            if pedidos:
                pedidos.pop()
                self.pedidos_por_mesa[numero] = pedidos
                atualizar_texto()
            else:
                messagebox.showinfo("Info", "Nenhum item para remover.")

        def salvar_observacoes():
            """Salva as observações no dicionário local"""
            obs = texto_observacoes.get("1.0", tk.END).strip()
            self.observacoes_por_mesa[numero] = obs

        def obter_id_pedido_ativo(numero_mesa):
            """Obtém o ID do pedido ativo da mesa"""
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="emporioDoSabor",
                    password="admin321@s",
                    database="lanchonete_db"
                )
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id FROM pedidos 
                    WHERE numero_mesa = %s 
                    AND (status IS NULL OR status != 'finalizado')
                    ORDER BY id DESC 
                    LIMIT 1
                """, (numero_mesa,))
                
                resultado = cursor.fetchone()
                return resultado[0] if resultado else None
                
            except mysql.connector.Error as error:
                print(f"Erro ao buscar pedido ativo: {error}")
                return None
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

        def enviar_para_cozinha():
            if not pedidos:
                messagebox.showwarning("Aviso", "Nenhum item no pedido para enviar.")
                return

            # Salva observações antes de enviar
            salvar_observacoes()
            observacoes = self.observacoes_por_mesa.get(numero, "")

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="emporioDoSabor",
                    password="admin321@s",
                    database="lanchonete_db"
                )
                cursor = conn.cursor()

                # Verifica se já existe um pedido ativo para esta mesa
                id_pedido_existente = obter_id_pedido_ativo(numero)
                
                if id_pedido_existente:
                    # Mesa já tem pedido ativo, adiciona novos itens ao pedido existente
                    # Primeiro atualiza as observações
                    cursor.execute("""
                        UPDATE pedidos 
                        SET observacoes = %s 
                        WHERE id = %s
                    """, (observacoes, id_pedido_existente))
                    
                    novos_itens = []
                    
                    # Identifica quais são os novos itens (comparando com o que já está no banco)
                    cursor.execute("""
                        SELECT pr.nome, ip.quantidade
                        FROM itens_pedido ip
                        JOIN produtos pr ON ip.id_produto = pr.id
                        WHERE ip.id_pedido = %s
                    """, (id_pedido_existente,))
                    
                    itens_existentes = {}
                    for nome, qtd in cursor.fetchall():
                        itens_existentes[nome] = itens_existentes.get(nome, 0) + qtd
                    
                    # Calcula novos itens
                    itens_atuais = {}
                    for item in pedidos:
                        itens_atuais[item['nome']] = itens_atuais.get(item['nome'], 0) + item['qtd']
                    
                    # Identifica itens novos ou com quantidade aumentada
                    for nome, qtd_atual in itens_atuais.items():
                        qtd_existente = itens_existentes.get(nome, 0)
                        if qtd_atual > qtd_existente:
                            qtd_nova = qtd_atual - qtd_existente
                            # Busca o item original para calcular o preço
                            for item in pedidos:
                                if item['nome'] == nome:
                                    preco_unitario = float(item['total']) / item['qtd']
                                    novos_itens.append({
                                        'nome': nome,
                                        'qtd': qtd_nova,
                                        'total': float(preco_unitario * qtd_nova)
                                    })
                                    break
                    
                    if not novos_itens:
                        messagebox.showinfo("Info", "Pedido atualizado com as observações.")
                        conn.commit()
                    else:
                        # Adiciona os novos itens ao pedido existente
                        for item in novos_itens:
                            cursor.execute("SELECT id, preco FROM produtos WHERE nome = %s", (item['nome'],))
                            produto = cursor.fetchone()
                            if not produto:
                                raise Exception(f"Produto '{item['nome']}' não encontrado no banco.")
                            id_produto, preco = produto
                            cursor.execute(
                                "INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, valor_total) VALUES (%s, %s, %s, %s)",
                                (id_pedido_existente, id_produto, item['qtd'], float(item['total']))
                            )
                        
                        conn.commit()
                        messagebox.showinfo("Sucesso", f"Novos itens adicionados ao pedido da Mesa {numero}!")
                else:
                    # Cria um novo pedido
                    total_pedido = sum(item["total"] for item in pedidos)
                    cursor.execute(
                        "INSERT INTO pedidos (numero_mesa, total, observacoes) VALUES (%s, %s, %s)",
                        (numero, total_pedido, observacoes)
                    )
                    id_pedido = cursor.lastrowid

                    # Adiciona os itens do pedido
                    for item in pedidos:
                        cursor.execute("SELECT id FROM produtos WHERE nome = %s", (item['nome'],))
                        resultado = cursor.fetchone()
                        if not resultado:
                            raise Exception(f"Produto '{item['nome']}' não encontrado no banco.")
                        id_produto = resultado[0]
                        cursor.execute(
                            "INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, valor_total) VALUES (%s, %s, %s, %s)",
                            (id_pedido, id_produto, item['qtd'], float(item['total']))
                        )

                    conn.commit()
                    messagebox.showinfo("Sucesso", f"Pedido da Mesa {numero} enviado para a cozinha!")

                # Atualiza status da mesa
                self.status_mesas[numero] = "ocupada"
                self.atualizar_cor_mesa(numero)
                
                # NOVO: Atualiza o indicador para "preparando"
                self.atualizar_indicador_status(numero, None)  # None = preparando

                janela_pedido.destroy()

            except mysql.connector.Error as error:
                messagebox.showerror("Erro", f"Erro ao salvar pedido:\n{error}")
                conn.rollback()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado:\n{e}")
                conn.rollback()
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

        def finalizar_mesa():
            if not pedidos:
                messagebox.showwarning("Aviso", "Nenhum pedido para finalizar.")
                return

            # Salva observações antes de finalizar
            salvar_observacoes()

            if messagebox.askyesno("Confirmar", f"Finalizar atendimento da Mesa {numero}?"):
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="emporioDoSabor",
                        password="admin321@s",
                        database="lanchonete_db"
                    )
                    cursor = conn.cursor()

                    # Atualiza o status do pedido para finalizado
                    cursor.execute("""
                        UPDATE pedidos 
                        SET status = 'finalizado' 
                        WHERE numero_mesa = %s 
                        AND (status IS NULL OR status != 'finalizado')
                    """, (numero,))

                    conn.commit()

                    # Libera a mesa
                    self.status_mesas[numero] = "livre"
                    self.pedidos_por_mesa[numero] = []
                    self.observacoes_por_mesa[numero] = ""  # NOVO: Limpa observações
                    self.atualizar_cor_mesa(numero)
                    
                    # NOVO: Remove o indicador visual
                    self.indicadores_status[numero].place_forget()

                    messagebox.showinfo("Sucesso", f"Mesa {numero} finalizada e liberada!")
                    janela_pedido.destroy()

                except mysql.connector.Error as error:
                    messagebox.showerror("Erro", f"Erro ao finalizar mesa:\n{error}")
                    conn.rollback()
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

        def cancelar_pedido():
            if messagebox.askyesno("Confirmar", f"Cancelar pedido da Mesa {numero}?"):
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="emporioDoSabor",
                        password="admin321@s",
                        database="lanchonete_db"
                    )
                    cursor = conn.cursor()

                    # Remove os itens do pedido ativo
                    cursor.execute("""
                        DELETE ip FROM itens_pedido ip
                        JOIN pedidos p ON ip.id_pedido = p.id
                        WHERE p.numero_mesa = %s 
                        AND (p.status IS NULL OR p.status != 'finalizado')
                    """, (numero,))

                    # Remove o pedido
                    cursor.execute("""
                        DELETE FROM pedidos 
                        WHERE numero_mesa = %s 
                        AND (status IS NULL OR status != 'finalizado')
                    """, (numero,))

                    conn.commit()

                    # Libera a mesa
                    self.status_mesas[numero] = "livre"
                    self.pedidos_por_mesa[numero] = []
                    self.observacoes_por_mesa[numero] = ""  # NOVO: Limpa observações
                    self.atualizar_cor_mesa(numero)
                    
                    # NOVO: Remove o indicador visual
                    self.indicadores_status[numero].place_forget()

                    messagebox.showinfo("Sucesso", f"Pedido da Mesa {numero} cancelado!")
                    janela_pedido.destroy()

                except mysql.connector.Error as error:
                    messagebox.showerror("Erro", f"Erro ao cancelar pedido:\n{error}")
                    conn.rollback()
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

        def gerar_conta():
            """Gera e exibe a conta da mesa"""
            if not pedidos:
                messagebox.showwarning("Aviso", "Nenhum pedido para gerar conta.")
                return

            # Salva observações antes de gerar conta
            salvar_observacoes()
            observacoes = self.observacoes_por_mesa.get(numero, "")

            # Cria janela da conta
            janela_conta = tk.Toplevel(janela_pedido)
            janela_conta.title(f"Conta - Mesa {numero}")
            janela_conta.geometry("400x500")
            janela_conta.configure(bg="white")
            
            # Centraliza a janela
            janela_conta.transient(janela_pedido)
            janela_conta.grab_set()

            # Cabeçalho
            frame_header = tk.Frame(janela_conta, bg="#2E7D32", height=80)
            frame_header.pack(fill="x")
            frame_header.pack_propagate(False)

            tk.Label(frame_header, text="EMPÓRIO DO SABOR", 
                    font=("Arial", 16, "bold"), bg="#2E7D32", fg="white").pack(pady=5)
            tk.Label(frame_header, text="Conta da Mesa", 
                    font=("Arial", 12), bg="#2E7D32", fg="white").pack()
            tk.Label(frame_header, text=f"Mesa: {numero:02d}", 
                    font=("Arial", 14, "bold"), bg="#2E7D32", fg="white").pack()

            # Frame principal com scroll
            main_frame = tk.Frame(janela_conta, bg="white")
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Área de conteúdo
            canvas_conta = tk.Canvas(main_frame, bg="white", highlightthickness=0)
            scrollbar_conta = tk.Scrollbar(main_frame, orient="vertical", command=canvas_conta.yview)
            scrollable_conta = tk.Frame(canvas_conta, bg="white")

            scrollable_conta.bind(
                "<Configure>",
                lambda e: canvas_conta.configure(scrollregion=canvas_conta.bbox("all"))
            )

            canvas_conta.create_window((0, 0), window=scrollable_conta, anchor="nw")
            canvas_conta.configure(yscrollcommand=scrollbar_conta.set)

            canvas_conta.pack(side="left", fill="both", expand=True)
            scrollbar_conta.pack(side="right", fill="y")

            # Data e hora
            from datetime import datetime
            agora = datetime.now()
            tk.Label(scrollable_conta, text=f"Data: {agora.strftime('%d/%m/%Y %H:%M')}", 
                    font=("Arial", 10), bg="white").pack(anchor="w", pady=5)

            # Linha separadora
            tk.Frame(scrollable_conta, height=2, bg="#CCCCCC").pack(fill="x", pady=10)

            # Itens do pedido
            tk.Label(scrollable_conta, text="ITENS CONSUMIDOS:", 
                    font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=5)

            total_geral = 0
            for i, item in enumerate(pedidos, 1):
                frame_item = tk.Frame(scrollable_conta, bg="white")
                frame_item.pack(fill="x", pady=2)

                tk.Label(frame_item, text=f"{i:02d}. {item['nome']}", 
                        font=("Arial", 10), bg="white").pack(anchor="w")
                
                frame_detalhes = tk.Frame(frame_item, bg="white")
                frame_detalhes.pack(fill="x")
                
                valor_unitario = item['total'] / item['qtd']
                tk.Label(frame_detalhes, text=f"     Qtd: {item['qtd']} x R$ {valor_unitario:.2f}", 
                        font=("Arial", 9), bg="white", fg="#666666").pack(anchor="w")
                tk.Label(frame_detalhes, text=f"R$ {item['total']:.2f}", 
                        font=("Arial", 10, "bold"), bg="white").pack(anchor="e")
                
                total_geral += item['total']

            # Observações (se houver)
            if observacoes.strip():
                tk.Frame(scrollable_conta, height=2, bg="#CCCCCC").pack(fill="x", pady=10)
                tk.Label(scrollable_conta, text="OBSERVAÇÕES:", 
                        font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
                tk.Label(scrollable_conta, text=observacoes, 
                        font=("Arial", 9), bg="white", fg="#666666", 
                        wraplength=350, justify="left").pack(anchor="w", pady=2)

            # Linha separadora
            tk.Frame(scrollable_conta, height=2, bg="#CCCCCC").pack(fill="x", pady=15)

            # Total
            frame_total = tk.Frame(scrollable_conta, bg="#F5F5F5", relief="solid", bd=1)
            frame_total.pack(fill="x", pady=10)
            
            tk.Label(frame_total, text="TOTAL A PAGAR:", 
                    font=("Arial", 14, "bold"), bg="#F5F5F5").pack(pady=5)
            tk.Label(frame_total, text=f"R$ {total_geral:.2f}", 
                    font=("Arial", 18, "bold"), bg="#F5F5F5", fg="#2E7D32").pack(pady=5)

            # Rodapé
            tk.Label(scrollable_conta, text="Obrigado pela preferência!", 
                    font=("Arial", 10, "italic"), bg="white", fg="#666666").pack(pady=20)

            # Botão fechar
            tk.Button(janela_conta, text="Fechar", font=("Arial", 12, "bold"), 
                     bg="#DC3545", fg="white", command=janela_conta.destroy).pack(pady=10)

        # Atualiza a exibição inicial
        atualizar_texto()

        # Frame de botões
        frame_botoes = tk.Frame(scrollable_frame, bg="#0A0B0A")
        frame_botoes.pack(pady=15, padx=20, fill="x")

        # Primeira linha de botões
        frame_linha1 = tk.Frame(frame_botoes, bg="#0A0B0A")
        frame_linha1.pack(fill="x", pady=5)

        tk.Button(frame_linha1, text="➕ Adicionar", font=("Arial", 10, "bold"), 
                 bg="#28a745", fg="white", command=adicionar_produto).pack(side="left", padx=5)

        tk.Button(frame_linha1, text="❌ Remover Último", font=("Arial", 10, "bold"), 
                 bg="#dc3545", fg="white", command=remover_ultimo).pack(side="left", padx=5)

        tk.Button(frame_linha1, text="💾 Salvar Obs.", font=("Arial", 10, "bold"), 
                 bg="#17a2b8", fg="white", command=salvar_observacoes).pack(side="right", padx=5)

        # Segunda linha de botões
        frame_linha2 = tk.Frame(frame_botoes, bg="#0A0B0A")
        frame_linha2.pack(fill="x", pady=5)

        tk.Button(frame_linha2, text="🍳 Enviar p/ Cozinha", font=("Arial", 10, "bold"), 
                 bg="#ff8c00", fg="white", command=enviar_para_cozinha).pack(side="left", padx=5)

        tk.Button(frame_linha2, text="📄 Gerar Conta", font=("Arial", 10, "bold"), 
                 bg="#6f42c1", fg="white", command=gerar_conta).pack(side="left", padx=5)

        # Terceira linha de botões
        frame_linha3 = tk.Frame(frame_botoes, bg="#0A0B0A")
        frame_linha3.pack(fill="x", pady=5)

        tk.Button(frame_linha3, text="✅ Finalizar Mesa", font=("Arial", 10, "bold"), 
                 bg="#28a745", fg="white", command=finalizar_mesa).pack(side="left", padx=5)

        tk.Button(frame_linha3, text="🗑️ Cancelar Pedido", font=("Arial", 10, "bold"), 
                 bg="#dc3545", fg="white", command=cancelar_pedido).pack(side="left", padx=5)

        tk.Button(frame_linha3, text="❌ Fechar", font=("Arial", 10, "bold"), 
                 bg="#6c757d", fg="white", command=janela_pedido.destroy).pack(side="right", padx=5)

        # Foco inicial no campo de busca
        entrada_produto.focus()

    def atualizar_cor_mesa(self, numero_mesa):
        """Atualiza a cor visual da mesa baseada no seu status"""
        for botao, num, label in self.botoes_mesa:
            if num == numero_mesa:
                if self.status_mesas[numero_mesa] == "livre":
                    botao.config(image=self.img_mesa_padrao)
                elif self.status_mesas[numero_mesa] == "ocupada":
                    botao.config(image=self.img_mesa_vermelha)
                break

if __name__ == "__main__":
    def callback_sair():
        print("Voltando ao menu principal")
    
    def tela_cozinheiro_mock():
        print("Tela do cozinheiro não implementada neste teste")
    
    root = tk.Tk()
    app = TelaGarcom(root, callback_sair, tela_cozinheiro_mock)
    root.mainloop()