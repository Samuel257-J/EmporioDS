import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
import mysql.connector
from mysql.connector import Error
from tela_Admin import TelaAdmin
import os
from pathlib import Path

class TelaLogin:
    def __init__(self, master, ao_logar_callback=None):  
        self.master = master
        # Definir o ícone da janela
        caminho_icone = Path(__file__).parent / "ImagensProjeto" / "iconEmporio.png"
        try:
            icone = tk.PhotoImage(file=str(caminho_icone))
            self.master.iconphoto(False, icone)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ícone:\n{e}")

        self.ao_logar_callback = ao_logar_callback
        self.master.title("LOGIN - Empório do Sabor")	
        self.master.geometry("425x582")
        self.master.resizable(False, False)
        
        # Centralizar janela na tela
        largura_janela = 425
        altura_janela = 582

        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)

        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")


        script_dir = Path(__file__).parent
        caminho_imagem = script_dir / "ImagensProjeto" / "telaLogin.png"

        try:
            imagem_fundo = Image.open(str(caminho_imagem)).resize((425, 582))
            self.fundo = ImageTk.PhotoImage(imagem_fundo)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{e}")
            self.master.destroy()
            return

        self.canvas = tk.Canvas(self.master, width=425, height=582, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.fundo, anchor="nw")

        self.entry_usuario = tk.Entry(self.master, font=("Arial", 14))
        self.entry_senha = tk.Entry(self.master, font=("Arial", 14), show="*")
        self.botao_login = tk.Button(self.master, text="Entrar", font=("Arial", 10, "bold"),
                                     bg="#ebb501", fg="white", cursor="hand2", command=self.fazer_login)
        self.botao_cadastrar = tk.Button(self.master, text="Cadastrar", font=("Arial", 10, "bold"),
                                         bg="#4E51F6", fg="white", cursor="hand2", command=self.abrir_cadastro)
        self.label_esqueceu = tk.Label(self.master, text="Esqueceu a senha?",
                                       font=("Arial", 9), fg="#A6A0A0", bg="#030101", cursor="hand2")
        self.canvas.create_window(167, 463, window=self.label_esqueceu)
        self.label_esqueceu.bind("<Button-1>", self.redefinir_senha)

        
        self.canvas.create_text(137, 355, text="Usuário", font=("Arial", 10, "bold"), fill="white")
        self.canvas.create_text(132, 410, text="Senha", font=("Arial", 10, "bold"), fill="white")

        self.canvas.create_window(212, 380, window=self.entry_usuario, width=200, height=30)
        self.canvas.create_window(212, 435, window=self.entry_senha, width=200, height=30)
        self.canvas.create_window(340, 520, window=self.botao_login, width=100, height=30)
        self.canvas.create_window(230, 520, window=self.botao_cadastrar, width=100, height=30)
        self.botao_mostrar_senha = tk.Button(
            self.master, 
                text="👁",
                font=("Segoe UI Emoji", 12),
                width=3,
                height=1,
                bg="#2c2c2c",
                fg="#ffffff",
                activebackground="#404040",
                activeforeground="#ffffff",
                relief="flat",
                cursor="hand2",
                command=self.toggle_senha
            )
        self.canvas.create_window(325, 435, window=self.botao_mostrar_senha, width=30, height=30)
        
    def toggle_senha(self):
        """Alternar visibilidade da senha"""
        if self.entry_senha.cget('show') == '*':
            # Mostrar senha
            self.entry_senha.config(show='')
            self.botao_mostrar_senha.config(
                text='🙈',
                bg="#ff6b6b",
                activebackground="#ff5252"
            )
        else:
            # Ocultar senha
            self.entry_senha.config(show='*')
            self.botao_mostrar_senha.config(
                text='👁',
                bg="#2c2c2c",
                activebackground="#404040"
            )

    # Versão alternativa com ícones de texto (caso os emojis não funcionem bem)
    def toggle_senha_alternativo(self):
        """Versão alternativa com ícones de texto"""
        if self.entry_senha.cget('show') == '*':
            # Mostrar senha
            self.entry_senha.config(show='')
            self.botao_mostrar_senha.config(
                text='HIDE',
                font=("Arial", 8, "bold"),
                bg="#ff6b6b",
                activebackground="#ff5252"
            )
        else:
            # Ocultar senha
            self.entry_senha.config(show='*')
            self.botao_mostrar_senha.config(
                text='SHOW',
                font=("Arial", 8, "bold"),
                bg="#2c2c2c",
                activebackground="#404040"
            )

    # Versão com ícones SVG-like usando caracteres Unicode
    def criar_botao_moderno_unicode(self):
        """Criar botão com caracteres Unicode mais modernos"""
        self.botao_mostrar_senha = tk.Button(
            self.master,
            text="◉",  # ou use "●" ou "○"
            font=("Arial", 14),
            width=2,
            height=1,
            bg="#4a90e2",
            fg="#ffffff",
            activebackground="#357abd",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.toggle_senha_unicode
        )
        
    def toggle_senha_unicode(self):
        """Toggle com caracteres Unicode"""
        if self.entry_senha.cget('show') == '*':
            self.entry_senha.config(show='')
            self.botao_mostrar_senha.config(
                text="◎",
                bg="#e74c3c",
                activebackground="#c0392b"
            )
        else:
            self.entry_senha.config(show='*')
            self.botao_mostrar_senha.config(
                text="◉",
                bg="#4a90e2",
                activebackground="#357abd"
            )
        
    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

    # Conta fixa de admin
        USUARIO_ADMIN_FIXO = "admin"
        SENHA_ADMIN_FIXO = "123456"

        if usuario == USUARIO_ADMIN_FIXO and senha == SENHA_ADMIN_FIXO:
            messagebox.showinfo("Login", "Bem-vindo, ADMINISTRADOR!")
            self.master.withdraw()  # Esconde a tela de login
            janela_admin = tk.Toplevel(self.master)
        
            def ao_sair_admin():
                janela_admin.destroy()
                self.limpar_campos()
                self.master.deiconify()

            TelaAdmin(janela_admin, ao_sair_admin)  
            return

        if not usuario or not senha:
            messagebox.showwarning("Campos vazios", "Preencha usuário e senha.")
            return
        
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='emporioDoSabor',
                password='admin321@s',
                database='lanchonete_db'
            )

            if conexao.is_connected():
                cursor = conexao.cursor()
                sql = "SELECT * FROM funcionarios WHERE usuario = %s AND senha = %s"
                valores = (usuario, senha)
                cursor.execute(sql, valores)
                resultado = cursor.fetchone()

                if resultado:
                    id, nome, cpf, cargo, usuario, senha = resultado
                    messagebox.showinfo("Login", f"Bem-vindo, {cargo}!")
                    self.master.withdraw()

                    cargo = cargo.strip().lower()

                    if cargo == "garçom":
                        from tela_Garcom import TelaGarcom
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaGarcom(janela, ao_sair, tela_cozinheiro=None)

                    elif cargo == "atendente":
                        from tela_Atendente import TelaAtendente
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaAtendente(janela, ao_sair)

                    elif cargo == "cozinheiro":
                        from tela_Cozinheiro import TelaCozinheiro
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaCozinheiro(janela, ao_sair)

                    elif cargo == "gerente":
                        from tela_Gerente import TelaGerente
                        janela = tk.Toplevel(self.master)

                        def ao_sair():
                            janela.destroy()
                            self.limpar_campos()
                            self.master.deiconify()

                        TelaGerente(janela, ao_sair)

                    else:
                        messagebox.showerror("Erro", f"Cargo '{cargo}' não reconhecido.")
                        self.master.deiconify()


        except Error as e:
            messagebox.showerror("Erro", f"Erro ao acessar o banco de dados:\n{e}")

        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

    def abrir_cadastro(self):
        def verificar_admin():
            usuario = entry_admin_usuario.get()
            senha = entry_admin_senha.get()

            USUARIO_ADMIN_FIXO = "admin"
            SENHA_ADMIN_FIXO = "123456"

            if usuario == USUARIO_ADMIN_FIXO and senha == SENHA_ADMIN_FIXO:
                messagebox.showinfo("Acesso liberado", "Administrador autenticado.")
                janela_admin_login.destroy()

                from tela_Cadastro import TelaCadastro

                def ao_voltar():
                    self.master.deiconify()
                    self.master.lift()
                    self.master.focus_force()
                    self.master.update_idletasks()

                janela_cadastro = tk.Toplevel(self.master)
                app_cadastro = TelaCadastro(janela_cadastro, ao_voltar)
                janela_cadastro.grab_set()
                self.master.withdraw()

            else:
                messagebox.showerror("Acesso negado", "Usuário ou senha do administrador incorretos.")

        # Criar janela de autenticação de admin
        janela_admin_login = tk.Toplevel(self.master)
        janela_admin_login.title("Autenticação do Administrador")
        janela_admin_login.geometry("300x180")
        janela_admin_login.resizable(False, False)
        janela_admin_login.grab_set()

        # Centralizar na tela
        largura_janela = 300
        altura_janela = 180 
        largura_tela = janela_admin_login.winfo_screenwidth()
        altura_tela = janela_admin_login.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_admin_login.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Função para voltar à tela de login
        def voltar_para_login():
            janela_admin_login.destroy()
            self.master.deiconify()  # Mostra novamente a janela principal (TelaLogin)

        tk.Label(janela_admin_login, text="Usuário Admin:").pack(pady=(10, 0))
        entry_admin_usuario = tk.Entry(janela_admin_login)
        entry_admin_usuario.pack()

        tk.Label(janela_admin_login, text="Senha Admin:").pack(pady=(10, 0))
        entry_admin_senha = tk.Entry(janela_admin_login, show="*")
        entry_admin_senha.pack()

        # Frame para os botões (para organizá-los lado a lado)
        frame_botoes = tk.Frame(janela_admin_login)
        frame_botoes.pack(pady=15)

        tk.Button(frame_botoes, text="Autenticar", bg="#47AF06", fg="white",
                font=("Arial", 10, "bold"), command=verificar_admin).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(frame_botoes, text="Voltar", bg="#DC3545", fg="white",
                font=("Arial", 10, "bold"), command=voltar_para_login).pack(side=tk.LEFT)

        self.master.withdraw()

    def redefinir_senha(self, event):
        # Verificar se o campo usuário está preenchido
        usuario = self.entry_usuario.get().strip()
        if not usuario:
            messagebox.showwarning("Campo vazio", "Digite seu usuário primeiro.")
            return

        # Criar janela de redefinição de senha
        janela_redefinir = tk.Toplevel(self.master)
        janela_redefinir.title("Redefinir Senha")
        janela_redefinir.geometry("400x350")
        janela_redefinir.resizable(False, False)
        janela_redefinir.grab_set()

        # Centralizar janela na tela
        largura_janela = 400
        altura_janela = 350
        largura_tela = janela_redefinir.winfo_screenwidth()
        altura_tela = janela_redefinir.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        janela_redefinir.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Configurar cor de fundo
        janela_redefinir.configure(bg="#f0f0f0")

        # Título
        tk.Label(janela_redefinir, text="Redefinir Senha", 
                font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=(15, 10))

        # Frame principal
        frame_principal = tk.Frame(janela_redefinir, bg="#f0f0f0")
        frame_principal.pack(pady=5, padx=20, fill="both", expand=True)

        # Campo CPF
        tk.Label(frame_principal, text="Digite seu CPF:", 
                font=("Arial", 12), bg="#f0f0f0").pack(pady=(5, 3))
        entry_cpf = tk.Entry(frame_principal, font=("Arial", 12), width=20)
        entry_cpf.pack(pady=(0, 10))

        # Campo Nova Senha
        tk.Label(frame_principal, text="Nova senha:", 
                font=("Arial", 12), bg="#f0f0f0").pack(pady=(5, 3))
        
        frame_nova_senha = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_nova_senha.pack(pady=(0, 10))
        
        entry_nova_senha = tk.Entry(frame_nova_senha, font=("Arial", 12), show="*", width=20)
        entry_nova_senha.pack(side="left", padx=(0, 5))
        
        # Botão para mostrar/ocultar nova senha
        btn_mostrar_nova = tk.Button(frame_nova_senha, text="👁", font=("Arial", 10), 
                                    width=3, cursor="hand2", bg="#e0e0e0")
        btn_mostrar_nova.pack(side="left")

        # Campo Confirmar Senha
        tk.Label(frame_principal, text="Confirmar nova senha:", 
                font=("Arial", 12), bg="#f0f0f0").pack(pady=(5, 3))
        
        frame_confirmar_senha = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_confirmar_senha.pack(pady=(0, 15))
        
        entry_confirmar_senha = tk.Entry(frame_confirmar_senha, font=("Arial", 12), show="*", width=20)
        entry_confirmar_senha.pack(side="left", padx=(0, 5))
        
        # Botão para mostrar/ocultar confirmação de senha
        btn_mostrar_confirmar = tk.Button(frame_confirmar_senha, text="👁", font=("Arial", 10), 
                                        width=3, cursor="hand2", bg="#e0e0e0")
        btn_mostrar_confirmar.pack(side="left")

        def processar_redefinicao():
            cpf = entry_cpf.get().strip()
            nova_senha = entry_nova_senha.get()
            confirmar_senha = entry_confirmar_senha.get()

            # Validações básicas
            if not cpf:
                messagebox.showwarning("Campo vazio", "Digite seu CPF.")
                return

            if not nova_senha:
                messagebox.showwarning("Campo vazio", "Digite a nova senha.")
                return

            if not confirmar_senha:
                messagebox.showwarning("Campo vazio", "Confirme a nova senha.")
                return

            if nova_senha != confirmar_senha:
                messagebox.showerror("Senhas diferentes", "As senhas não coincidem.")
                return

            if len(nova_senha) < 4:
                messagebox.showwarning("Senha muito curta", "A senha deve ter pelo menos 4 caracteres.")
                return

            # Validar CPF e usuário no banco de dados
            try:
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='emporioDoSabor',
                    password='admin321@s',
                    database='lanchonete_db'
                )

                if conexao.is_connected():
                    cursor = conexao.cursor()
                    
                    # Verificar se existe um funcionário com esse usuário e CPF
                    sql_verificar = "SELECT id, nome FROM funcionarios WHERE usuario = %s AND cpf = %s"
                    cursor.execute(sql_verificar, (usuario, cpf))
                    resultado = cursor.fetchone()

                    if not resultado:
                        messagebox.showerror("Dados inválidos", 
                                        "Usuário ou CPF não encontrados no sistema.")
                        return

                    funcionario_id, nome_funcionario = resultado

                    # Confirmar a alteração
                    resposta = messagebox.askyesno("Confirmar alteração", 
                                                f"Deseja alterar a senha do usuário '{nome_funcionario}'?")
                    
                    if resposta:
                        # Atualizar a senha no banco de dados
                        sql_atualizar = "UPDATE funcionarios SET senha = %s WHERE id = %s"
                        cursor.execute(sql_atualizar, (nova_senha, funcionario_id))
                        conexao.commit()

                        if cursor.rowcount > 0:
                            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
                            janela_redefinir.destroy()
                            # Limpar apenas o campo de senha na tela de login
                            self.entry_senha.delete(0, tk.END)
                        else:
                            messagebox.showerror("Erro", "Não foi possível alterar a senha. Tente novamente.")

            except Error as e:
                messagebox.showerror("Erro", f"Erro ao acessar o banco de dados:\n{e}")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado:\n{e}")

            finally:
                if 'conexao' in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()

        def cancelar_redefinicao():
            janela_redefinir.destroy()

        # Funções para mostrar/ocultar senhas
        def toggle_nova_senha():
            if entry_nova_senha.cget('show') == '*':
                entry_nova_senha.config(show='')
                btn_mostrar_nova.config(text='🙈', bg="#ffcccc")
            else:
                entry_nova_senha.config(show='*')
                btn_mostrar_nova.config(text='👁', bg="#e0e0e0")

        def toggle_confirmar_senha():
            if entry_confirmar_senha.cget('show') == '*':
                entry_confirmar_senha.config(show='')
                btn_mostrar_confirmar.config(text='🙈', bg="#ffcccc")
            else:
                entry_confirmar_senha.config(show='*')
                btn_mostrar_confirmar.config(text='👁', bg="#e0e0e0")

        # Configurar comandos dos botões de mostrar/ocultar
        btn_mostrar_nova.config(command=toggle_nova_senha)
        btn_mostrar_confirmar.config(command=toggle_confirmar_senha)

        # Frame para botões
        frame_botoes = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_botoes.pack(pady=15, side="bottom")

        # Botões
        tk.Button(frame_botoes, text="Alterar Senha", bg="#47AF06", fg="white",
                font=("Arial", 10, "bold"), command=processar_redefinicao,
                cursor="hand2", width=12, height=1).pack(side="left", padx=(0, 10))

        tk.Button(frame_botoes, text="Cancelar", bg="#dc3545", fg="white",
                font=("Arial", 10, "bold"), command=cancelar_redefinicao,
                cursor="hand2", width=10, height=1).pack(side="left")

        # Focar no campo CPF
        entry_cpf.focus_set()

        # Bind Enter para facilitar navegação
        def on_enter_cpf(event):
            entry_nova_senha.focus_set()
        
        def on_enter_nova_senha(event):
            entry_confirmar_senha.focus_set()
        
        def on_enter_confirmar_senha(event):
            processar_redefinicao()

        entry_cpf.bind('<Return>', on_enter_cpf)
        entry_nova_senha.bind('<Return>', on_enter_nova_senha)
        entry_confirmar_senha.bind('<Return>', on_enter_confirmar_senha)

    def limpar_campos(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app_login = TelaLogin(root)
    root.mainloop()

