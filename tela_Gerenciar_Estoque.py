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

        # Eventos de seleção
        self.lista_produtos.bind("<<ListboxSelect>>", self.selecionar_produto)
        self.lista_produtos.bind("<Double-Button-1>", self.abrir_edicao_produto)

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

        # Frame para os botões de ação principais (Confirmar e Desativar/Reativar)
        frame_acoes_principais = tk.Frame(self.frame_detalhes, bg="#050505")
        frame_acoes_principais.pack(pady=5)

        # Botão confirmar
        self.botao_confirmar = tk.Button(frame_acoes_principais, text="Confirmar", font=("Arial", 12), bg="green", fg="white", command=self.confirmar_estoque, width=10, height=1)
        self.botao_confirmar.pack(side=tk.LEFT, padx=5)

        # Botão excluir produto (que muda dinamicamente)
        self.botao_excluir = tk.Button(frame_acoes_principais, text="Desativar", font=("Arial", 12), bg="orange", fg="white", command=self.excluir_produto, width=10, height=1)
        self.botao_excluir.pack(side=tk.LEFT, padx=5)

        # Frame separado para o botão de editar (abaixo dos outros)
        frame_acao_secundaria = tk.Frame(self.frame_detalhes, bg="#050505")
        frame_acao_secundaria.pack(pady=(5, 0))

        # Botão editar produto (centralizado no seu próprio frame)
        self.botao_editar = tk.Button(frame_acao_secundaria, text="Editar", font=("Arial", 12), bg="blue", fg="white", command=self.abrir_edicao_produto, width=22, height=1)
        self.botao_editar.pack()

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
            # Carregar todos os produtos com informação sobre se estão ativos
            cursor.execute("""
                SELECT id, nome, estoque, COALESCE(ativo, TRUE) as ativo FROM produtos 
                ORDER BY COALESCE(ativo, TRUE) DESC, estoque ASC
            """)
            self.produtos = cursor.fetchall()
            self.atualizar_lista()
        except Error as e:
            # Se der erro (provavelmente porque a coluna 'ativo' não existe), carregar normalmente
            try:
                cursor.execute("SELECT id, nome, estoque, TRUE as ativo FROM produtos ORDER BY estoque ASC")
                self.produtos = cursor.fetchall()
                self.atualizar_lista()
            except Error as e2:
                messagebox.showerror("Erro", f"Erro ao carregar produtos: {e2}")
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def atualizar_lista(self, filtro=""):
        self.lista_produtos.delete(0, tk.END)
        
        # Índice para controlar a posição na lista
        index = 0
        
        for produto in self.produtos:
            nome, estoque, ativo = produto[1], produto[2], produto[3] if len(produto) > 3 else True
            if nome.lower().startswith(filtro.lower()):
                # Se o produto está inativo, mostrar estoque como 0
                estoque_exibido = 0 if not ativo else estoque
                status_texto = " (INATIVO)" if not ativo else ""
                
                # Adiciona o item na lista
                self.lista_produtos.insert(tk.END, f"{nome}{status_texto} - Estoque: {estoque_exibido}")
                
                # Definir cores baseadas no status e estoque
                if not ativo:
                    # Produto inativo - cinza
                    self.lista_produtos.itemconfig(index, {'bg': '#808080', 'fg': 'white'})
                elif estoque <= 10:
                    # Produto ativo com estoque baixo - vermelho
                    self.lista_produtos.itemconfig(index, {'bg': '#FF4444', 'fg': 'white'})
                else:
                    # Produto ativo com estoque normal - branco
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
            
            # Verificar se o produto está ativo
            produto_ativo = self.produto_selecionado[3] if len(self.produto_selecionado) > 3 else True
            
            self.label_nome.config(text=f"Nome: {self.produto_selecionado[1][:40]}")  # corta o nome se for muito grande
            self.entry_estoque.delete(0, tk.END)
            
            if produto_ativo:
                # Produto ativo - mostrar estoque real e permitir edição
                self.entry_estoque.insert(0, str(self.produto_selecionado[2]))
                self.entry_estoque.config(state='normal')
                self.botao_mais.config(state='normal')
                self.botao_menos.config(state='normal')
                self.botao_confirmar.config(state='normal')
                self.botao_excluir.config(text="Desativar", bg="orange", state='normal')
                self.botao_editar.config(state='normal')
            else:
                # Produto inativo - mostrar 0 e desabilitar edição de estoque
                self.entry_estoque.insert(0, "0")
                self.entry_estoque.config(state='disabled')
                self.botao_mais.config(state='disabled')
                self.botao_menos.config(state='disabled')
                self.botao_confirmar.config(state='disabled')
                self.botao_excluir.config(text="Reativar", bg="green", state='normal')
                self.botao_editar.config(state='normal')  # Permite editar produtos inativos

    def abrir_edicao_produto(self, event=None):
        """Abre a TelaCadastroProduto para editar o produto selecionado"""
        if not self.produto_selecionado:
            messagebox.showwarning("Nenhum produto selecionado", "Selecione um produto para editar.", parent=self)
            return

        try:
            # Buscar todas as informações do produto no banco
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )
            cursor = conexao.cursor()
            
            # Buscar todos os dados do produto
            cursor.execute("""
                SELECT id, nome, preco, categoria, estoque, 
                    COALESCE(ativo, TRUE) as ativo 
                FROM produtos WHERE id = %s
            """, (self.produto_selecionado[0],))
            
            produto_completo = cursor.fetchone()
            
            if produto_completo:
                # Importar e abrir a TelaCadastroProduto
                try:
                    from tela_Gerente import TelaCadastroProduto
                    
                    # Criar instância da TelaCadastroProduto em modo de edição
                    tela_cadastro = TelaCadastroProduto(self, produto_para_editar=produto_completo)
                    
                    # Aguardar o fechamento da tela de cadastro e recarregar os produtos
                    self.wait_window(tela_cadastro)
                    
                    # IMPORTANTE: Recarregar os dados após a edição
                    self.carregar_produtos()
                    
                    # Limpar seleção atual para forçar nova seleção
                    self.produto_selecionado = None
                    self.estoque_temp = None
                    
                    # Limpar campos de detalhes
                    self.label_nome.config(text="Nome: ")
                    self.entry_estoque.delete(0, tk.END)
                    self.entry_estoque.config(state='normal')
                    
                    # Desabilitar botões até nova seleção
                    self.botao_mais.config(state='disabled')
                    self.botao_menos.config(state='disabled')
                    self.botao_confirmar.config(state='disabled')
                    self.botao_excluir.config(state='disabled', text="Desativar", bg="orange")
                    self.botao_editar.config(state='disabled')
                    
                except ImportError:
                    messagebox.showerror("Erro", "Não foi possível importar TelaCadastroProduto.\nVerifique se o arquivo tela_Gerente.py existe e contém a classe TelaCadastroProduto.", parent=self)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao abrir tela de edição:\n{e}", parent=self)
            else:
                messagebox.showerror("Erro", "Produto não encontrado no banco de dados.", parent=self)
                
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados do produto:\n{e}", parent=self)
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

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
            # Verificar se o produto está ativo
            produto_ativo = self.produto_selecionado[3] if len(self.produto_selecionado) > 3 else True
            if not produto_ativo:
                return
                
            if self.estoque_temp is None:
                self.estoque_temp = self.produto_selecionado[2]
            self.estoque_temp += 10
            self.entry_estoque.delete(0, tk.END)
            self.entry_estoque.insert(0, str(self.estoque_temp))

    def diminuir_estoque(self):
        if self.produto_selecionado:
            # Verificar se o produto está ativo
            produto_ativo = self.produto_selecionado[3] if len(self.produto_selecionado) > 3 else True
            if not produto_ativo:
                return
                
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
            id_produto = self.produto_selecionado[0]
            estoque_anterior = self.produto_selecionado[2]  # Estoque atual antes da edição

            resposta = messagebox.askyesno(
                "Confirmar Alteração",
                f"Deseja realmente atualizar o estoque de {estoque_anterior} para {estoque_final}?",
                icon='warning',
                parent=self
            )

            if resposta:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="emporioDoSabor",
                        password="admin321@s",
                        database="lanchonete_db"
                    )
                    cursor = conn.cursor()

                    # Atualizar a quantidade total de estoque (substituir)
                    self.atualizar_estoque_no_banco(estoque_final)

                    # Calcular a diferença e registrar na tabela estoque
                    if estoque_final < estoque_anterior:
                        saida = estoque_anterior - estoque_final
                        cursor.execute("""
                            INSERT INTO estoque (id_produto, quantidade_saida)
                            VALUES (%s, %s)
                        """, (id_produto, saida))

                    elif estoque_final > estoque_anterior:
                        entrada = estoque_final - estoque_anterior
                        cursor.execute("""
                            INSERT INTO estoque (id_produto, quantidade_entrada)
                            VALUES (%s, %s)
                        """, (id_produto, entrada))

                    conn.commit()

                    # CORREÇÃO: Atualizar a lista de produtos para refletir a mudança
                    for i, produto in enumerate(self.produtos):
                        if produto[0] == id_produto:
                            # Atualizar o produto na lista mantendo a estrutura original
                            produto_ativo = produto[3] if len(produto) > 3 else True
                            self.produtos[i] = (id_produto, produto[1], estoque_final, produto_ativo)
                            break

                    # Atualizar estado interno do produto selecionado
                    produto_ativo = self.produto_selecionado[3] if len(self.produto_selecionado) > 3 else True
                    self.produto_selecionado = (id_produto, self.produto_selecionado[1], estoque_final, produto_ativo)
                    self.estoque_temp = None

                    messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso.", parent=self)
                    
                    # Atualizar a exibição da lista
                    self.atualizar_lista(self.entry_filtro.get())
                    
                    # Atualizar o campo de entrada para mostrar o novo valor
                    self.entry_estoque.delete(0, tk.END)
                    self.entry_estoque.insert(0, str(estoque_final))
                    
                    # CORREÇÃO: Reabilitar os botões após a confirmação
                    # (isso resolve o problema do botão Desativar ficar inativo)
                    if produto_ativo:
                        # Para produtos ativos
                        self.entry_estoque.config(state='normal')
                        self.botao_mais.config(state='normal')
                        self.botao_menos.config(state='normal')
                        self.botao_confirmar.config(state='normal')
                        self.botao_excluir.config(text="Desativar", bg="orange", state='normal')
                        self.botao_editar.config(state='normal')
                    else:
                        # Para produtos inativos (caso raro, mas por segurança)
                        self.entry_estoque.config(state='disabled')
                        self.botao_mais.config(state='disabled')
                        self.botao_menos.config(state='disabled')
                        self.botao_confirmar.config(state='disabled')
                        self.botao_excluir.config(text="Reativar", bg="green", state='normal')
                        self.botao_editar.config(state='normal')

                except mysql.connector.Error as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar o estoque:\n{e}", parent=self)
                    if 'conn' in locals() and conn.is_connected():
                        conn.rollback()
                finally:
                    if 'conn' in locals() and conn.is_connected():
                        cursor.close()
                        conn.close()

    def excluir_produto(self):
        """Desativa/Reativa o produto selecionado após confirmação"""
        if not self.produto_selecionado:
            messagebox.showwarning("Nenhum produto selecionado", "Selecione um produto para desativar/reativar.", parent=self)
            return

        nome_produto = self.produto_selecionado[1]
        id_produto = self.produto_selecionado[0]
        produto_ativo = self.produto_selecionado[3] if len(self.produto_selecionado) > 3 else True

        if produto_ativo:
            # Produto está ativo - desativar
            resposta = messagebox.askyesno(
                "Confirmar Desativação",
                f"Tem certeza que deseja desativar o produto '{nome_produto}'?\n\n• O produto ficará indisponível para vendas\n• O estoque será zerado na exibição\n• O histórico de vendas será mantido\n• Pode ser reativado a qualquer momento",
                icon='warning',
                parent=self
            )

            if resposta:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="emporioDoSabor",
                        password="admin321@s",
                        database="lanchonete_db"
                    )
                    cursor = conn.cursor()

                    # Verificar se a coluna 'ativo' existe na tabela produtos
                    cursor.execute("SHOW COLUMNS FROM produtos LIKE 'ativo'")
                    coluna_existe = cursor.fetchone()
                    
                    if not coluna_existe:
                        # Adicionar coluna 'ativo' se não existir
                        cursor.execute("ALTER TABLE produtos ADD COLUMN ativo BOOLEAN DEFAULT TRUE")
                        conn.commit()

                    # Marcar o produto como inativo
                    cursor.execute("UPDATE produtos SET ativo = FALSE WHERE id = %s", (id_produto,))
                    conn.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo("Sucesso", f"Produto '{nome_produto}' desativado com sucesso!", parent=self)
                        self.carregar_produtos()
                    else:
                        messagebox.showwarning("Aviso", "Nenhum produto foi desativado.", parent=self)

                except mysql.connector.Error as e:
                    messagebox.showerror("Erro", f"Erro ao desativar produto:\n{e}", parent=self)
                    if 'conn' in locals() and conn.is_connected():
                        conn.rollback()
                finally:
                    if 'conn' in locals() and conn.is_connected():
                        cursor.close()
                        conn.close()
        
        else:
            # Produto está inativo - reativar
            resposta = messagebox.askyesno(
                "Confirmar Reativação",
                f"Tem certeza que deseja reativar o produto '{nome_produto}'?\n\n• O produto voltará a ficar disponível para vendas\n• Você poderá definir um novo estoque\n• O produto aparecerá normalmente nas listas",
                icon='question',
                parent=self
            )

            if resposta:
                try:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="emporioDoSabor",
                        password="admin321@s",
                        database="lanchonete_db"
                    )
                    cursor = conn.cursor()

                    # Marcar o produto como ativo
                    cursor.execute("UPDATE produtos SET ativo = TRUE WHERE id = %s", (id_produto,))
                    conn.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo("Sucesso", f"Produto '{nome_produto}' reativado com sucesso!\n\nAgora você pode definir um novo estoque.", parent=self)
                        self.carregar_produtos()
                    else:
                        messagebox.showwarning("Aviso", "Nenhum produto foi reativado.", parent=self)

                except mysql.connector.Error as e:
                    messagebox.showerror("Erro", f"Erro ao reativar produto:\n{e}", parent=self)
                    if 'conn' in locals and conn.is_connected():
                        conn.rollback()
                finally:
                    if 'conn' in locals() and conn.is_connected():
                        cursor.close()
                        conn.close()

    def validar_numeros(self, valor):
        return valor.isdigit() or valor == ""

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = TelaGerenciarEstoque(root)
    app.mainloop()