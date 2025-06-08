# Códigos do Sistema

Nesta página você encontra os principais trechos de código utilizados no sistema de gestão de lanchonete.

## Cadastro de Produtos

python
def cadastrar_produto(self):
        """Cadastra um novo produto"""
        # Obter valores dos campos
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get()
        preco_str = self.var_preco.get().replace("R$", "").replace(",", ".")
        preco = float(preco_str)
        estoque = int(self.entry_estoque.get())

# Controle e Registro de Pedidos

python
def carregar_pedidos_ativos(self):
        """Carrega todos os pedidos ativos do banco e atualiza o status das mesas"""
        try:
            conn = mysql.connector.connect(
                host="",
                user="",
                password="",
                database=""
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
                    
                    # Atualiza o indicador visual baseado no status do pedido
                    self.atualizar_indicador_status(numero_mesa, status_pedido)
            
            print(f"Carregados pedidos ativos para {len(mesas_ocupadas)} mesas")
            
        except mysql.connector.Error as error:
            print(f"Erro ao carregar pedidos ativos: {error}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# Relatório de Vendas

python
def exportar_relatorio(self):
        """
        Função para exportar relatório em PDF
        """
        try:
            # Verificar se há dados para exportar
            if not hasattr(self, 'dados_relatorio_atual') or not self.dados_relatorio_atual:
                messagebox.showwarning("Aviso", "Nenhum dado disponível para exportar. Atualize o relatório primeiro.")
                return
            
            # Abrir diálogo para escolher onde salvar
            filename = filedialog.asksaveasfilename(
                initialfile="relatorio.pdf", 
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )

            if not filename:
                return  # Usuário cancelou
            
            # Gerar o PDF
            self.gerar_pdf(filename)

            # Confirmar exportação
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n\nArquivo salvo em:\n{filename}")

            # Perguntar se quer abrir o arquivo
            if messagebox.askyesno("Abrir arquivo", "Deseja abrir o relatório PDF agora?"):
                try:
                    os.startfile(filename)  # Windows
                except:
                    try:
                        os.system(f"open '{filename}'")  # macOS
                    except:
                        try:
                            os.system(f"xdg-open '{filename}'")  # Linux
                        except:
                            messagebox.showinfo("Info", f"Arquivo salvo em: {filename}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório: {e}")

    def gerar_pdf(self, nome_arquivo):
        """Gera o arquivo PDF com os dados do relatório"""
        
        # Criar documento PDF
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        story = []
        
        # Configurar estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para título
        titulo_style = ParagraphStyle(
            'TituloCustom',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2E86AB'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Estilo para subtítulos
        subtitulo_style = ParagraphStyle(
            'SubtituloCustom',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#A23B72'),
            spaceBefore=20,
            spaceAfter=10
        )
        
        # Estilo para texto normal
        texto_style = ParagraphStyle(
            'TextoCustom',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        
        # CABEÇALHO DO RELATÓRIO
        story.append(Paragraph("🏪 EMPÓRIO DO SABOR", titulo_style))
        story.append(Paragraph("Relatório Analytics Completo", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Informações do relatório
        data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
        info_relatorio = f"""
        <b>Data de Geração:</b> {data_atual}<br/>
        <b>Período Analisado:</b> {self.periodo_selecionado}<br/>
        <b>Sistema:</b> Empório do Sabor - Analytics Dashboard
        """
        story.append(Paragraph(info_relatorio, texto_style))
        story.append(Spacer(1, 30))
        
        # RESUMO EXECUTIVO
        story.append(Paragraph("📊 RESUMO EXECUTIVO", subtitulo_style))
        
        # Tabela de métricas principais
        metricas_data = [
            ['Métrica', 'Valor', 'Descrição'],
            ['Receita Total', self.dados_relatorio_atual.get('receita_formatada', 'R$ 0,00'), 'Vendas finalizadas'],
            ['Clientes Cadastrados', str(self.dados_relatorio_atual.get('total_clientes', 0)), 'Base de clientes'],
            ['Funcionários Ativos', str(self.dados_relatorio_atual.get('total_funcionarios', 0)), 'Equipe atual'],
            ['Produto Top', self.dados_relatorio_atual.get('produto_mais_vendido', 'N/A'), f"Vendidos: {self.dados_relatorio_atual.get('quantidade_mais_vendido', 0)} un."]
        ]
        
        # Criar tabela de métricas
        tabela_metricas = Table(metricas_data, colWidths=[2*inch, 1.5*inch, 2*inch])
        tabela_metricas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        story.append(tabela_metricas)
        story.append(Spacer(1, 30))
        
        # TOP 5 PRODUTOS MAIS VENDIDOS
        if 'top_produtos' in self.dados_relatorio_atual and self.dados_relatorio_atual['top_produtos']:
            story.append(Paragraph("🔥 TOP 5 PRODUTOS MAIS VENDIDOS", subtitulo_style))
            
            produtos_data = [['Produto', 'Quantidade Vendida', 'Receita Gerada']]
            for produto in self.dados_relatorio_atual['top_produtos']:
                nome, quantidade, receita = produto
                receita_formatada = f"R$ {receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                produtos_data.append([nome, str(quantidade), receita_formatada])
            
            # Se tiver menos de 5 produtos, preencher com linhas vazias
            while len(produtos_data) < 6:
                produtos_data.append(['-', '-', '-'])
            
            tabela_produtos = Table(produtos_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            tabela_produtos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6B35')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(tabela_produtos)
            story.append(Spacer(1, 25))
        
        # ANÁLISE DE PEDIDOS POR STATUS
        if 'pedidos_status' in self.dados_relatorio_atual and self.dados_relatorio_atual['pedidos_status']:
            story.append(Paragraph("📋 ANÁLISE DE PEDIDOS POR STATUS", subtitulo_style))
            
            status_data = [['Status do Pedido', 'Quantidade', 'Percentual']]
            total_pedidos = sum([item[1] for item in self.dados_relatorio_atual['pedidos_status']])
            
            for status, quantidade in self.dados_relatorio_atual['pedidos_status']:
                percentual = (quantidade / total_pedidos * 100) if total_pedidos > 0 else 0
                status_formatado = status.replace('_', ' ').title() if status else 'Não definido'
                status_data.append([status_formatado, str(quantidade), f"{percentual:.1f}%"])
            
            tabela_status = Table(status_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            tabela_status.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A23B72')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(tabela_status)
            story.append(Spacer(1, 25))
        
        # VENDAS POR CATEGORIA (se disponível)
        if 'vendas_categoria' in self.dados_relatorio_atual and self.dados_relatorio_atual['vendas_categoria']:
            story.append(Paragraph("🏷️ VENDAS POR CATEGORIA", subtitulo_style))
            
            categoria_data = [['Categoria', 'Vendas', 'Receita']]
            for categoria, vendas, receita in self.dados_relatorio_atual['vendas_categoria']:
                if receita:  # Só mostrar categorias com vendas
                    receita_formatada = f"R$ {receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    categoria_data.append([categoria, str(vendas or 0), receita_formatada])
            
            if len(categoria_data) > 1:  # Se há dados além do cabeçalho
                tabela_categoria = Table(categoria_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
                tabela_categoria.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F18F01')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                
                story.append(tabela_categoria)
                story.append(Spacer(1, 25))
        
        # RODAPÉ INFORMATIVO
        story.append(Spacer(1, 40))
        story.append(Paragraph("📄 INFORMAÇÕES ADICIONAIS", subtitulo_style))
        
        info_adicional = f"""
        <b>Observações importantes:</b><br/>
        • Este relatório foi gerado automaticamente pelo sistema Empório do Sabor<br/>
        • Os dados apresentados refletem o período {self.periodo_selecionado} selecionado<br/>
        • Valores financeiros consideram apenas pedidos finalizados e pagos<br/>
        • Para dúvidas sobre os dados, consulte o administrador do sistema<br/><br/>
        
        <b>Período de Análise:</b> {self.periodo_selecionado}<br/>
        <b>Gerado em:</b> {data_atual}<br/>
        <b>Sistema:</b> Empório do Sabor v1.0
        """
        
        story.append(Paragraph(info_adicional, texto_style))
        story.append(Spacer(1, 20))
        
        # Linha final
        story.append(Paragraph("_" * 80, styles['Normal']))
        story.append(Paragraph("Empório do Sabor - Relatório Analytics", 
                             ParagraphStyle('Footer', parent=styles['Normal'], 
                                          alignment=TA_CENTER, fontSize=8, 
                                          textColor=colors.grey)))
        
        # Construir o PDF
        doc.build(story)


# Controle de Estoque

python
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



