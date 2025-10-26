# views/substituir_valores.py
import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from controllers.substituir_valores_controller import SubstituirValoresController

class SubstituirValores(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.controller = SubstituirValoresController()
        master.geometry("1000x650")
        
        # Configuração de cores
        self.cor_primaria = "#238AD9"
        self.cor_sucesso = "#238AD9"
        self.cor_perigo = "#DC3545"
        self.cor_alerta = "#FFC107"

        # Variáveis
        self.arquivo_selecionado = None
        self.abas_disponiveis = []
        self.abas_selecionadas = []
        self.substituicoes = []
        
        # Variável para controle de frames recolhíveis
        self.frame_abas_visivel = True
        self.frame_substituicoes_visivel = True
        self.frame_config_visivel = True

        # === LAYOUT PRINCIPAL COMPACTO ===
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Botão Voltar
        self.btn_back = ctk.CTkButton(
            self.grid_frame, 
            text="←", 
            command=lambda: master.show_frame(master.menu_frame), 
            width=20,
            height=30,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_back.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Label principal
        self.label = ctk.CTkLabel(
            self.grid_frame,
            text="🔁 Substituir Valores em Planilhas",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.cor_primaria
        )
        self.label.grid(row=0, column=1, columnspan=2, pady=(0, 20))

        # === SELEÇÃO DE ARQUIVO ===
        self.frame_arquivo = ctk.CTkFrame(self.grid_frame)
        self.frame_arquivo.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        label_titulo_arquivo = ctk.CTkLabel(
            self.frame_arquivo,
            text="📁 Selecionar Arquivo Excel",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_arquivo.pack(anchor="w", pady=(10, 5), padx=10)

        subframe_arquivo = ctk.CTkFrame(self.frame_arquivo, fg_color="transparent")
        subframe_arquivo.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_selecionar_arquivo = ctk.CTkButton(
            subframe_arquivo,
            text="Procurar",
            command=self.selecionar_arquivo,
            width=100,
            height=32,
            fg_color=self.cor_primaria,
            hover_color="#218838"
        )
        self.btn_selecionar_arquivo.pack(side="left", padx=(0, 10))

        self.entry_arquivo = ctk.CTkEntry(
            subframe_arquivo,
            width=300,
            height=32,
            placeholder_text="Nenhum arquivo selecionado",
            state="readonly"
        )
        self.entry_arquivo.pack(side="left", fill="x", expand=True)

        # === LAYOUT EM COLUNAS: ABAS E SUBSTITUIÇÕES LADO A LADO ===
        self.frame_duas_colunas = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.frame_duas_colunas.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        # Coluna 1: Abas (40% da largura)
        self.frame_coluna_abas = ctk.CTkFrame(self.frame_duas_colunas)
        self.frame_coluna_abas.pack(side="left", fill="both", expand=True, padx=(5, 5))

        # Coluna 2: Substituições (60% da largura)
        self.frame_coluna_substituicoes = ctk.CTkFrame(self.frame_duas_colunas)
        self.frame_coluna_substituicoes.pack(side="right", fill="both", expand=True, padx=(5, 5))

        # === FRAME DE ABAS (COM BOTÃO DE RECOLHER) ===
        frame_titulo_abas = ctk.CTkFrame(self.frame_coluna_abas, fg_color="transparent")
        frame_titulo_abas.pack(fill="x", padx=5, pady=(5, 0))

        label_titulo_abas = ctk.CTkLabel(
            frame_titulo_abas,
            text="📊 Abas para Processar",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_abas.pack(side="left")

        self.btn_toggle_abas = ctk.CTkButton(
            frame_titulo_abas,
            text="−",
            width=25,
            height=25,
            command=self.toggle_frame_abas,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_toggle_abas.pack(side="right")

        # Frame para controles de seleção de abas
        self.frame_controles_abas = ctk.CTkFrame(self.frame_coluna_abas, fg_color="transparent")
        self.frame_controles_abas.pack(fill="x", padx=5, pady=5)

        self.btn_selecionar_todas = ctk.CTkButton(
            self.frame_controles_abas,
            text="✅ Todas",
            command=self.selecionar_todas_abas,
            width=150,
            height=28,
            fg_color=self.cor_sucesso,
            hover_color="#218838",
            state="disabled"
        )
        self.btn_selecionar_todas.pack(side="left", padx=(0, 5))

        self.btn_limpar_selecao = ctk.CTkButton(
            self.frame_controles_abas,
            text="🗑️ Limpar",
            command=self.limpar_selecao_abas,
            width=150,
            height=28,
            fg_color=self.cor_perigo,
            hover_color="#C82333",
            state="disabled"
        )
        self.btn_limpar_selecao.pack(side="left")

        # Label para mostrar seleção
        self.label_selecao_abas = ctk.CTkLabel(
            self.frame_controles_abas,
            text="Nenhuma selecionada",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            width=150
        )
        self.label_selecao_abas.pack(side="right")

        # Frame para a lista de abas
        self.frame_lista_abas = ctk.CTkScrollableFrame(
            self.frame_coluna_abas,
            height=120,
            fg_color="transparent"
        )
        self.frame_lista_abas.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # === FRAME DE SUBSTITUIÇÕES (COM BOTÃO DE RECOLHER) ===
        frame_titulo_substituicoes = ctk.CTkFrame(self.frame_coluna_substituicoes, fg_color="transparent")
        frame_titulo_substituicoes.pack(fill="x", padx=5, pady=(5, 0))

        label_titulo_substituicoes = ctk.CTkLabel(
            frame_titulo_substituicoes,
            text="🔄 Regras de Substituição",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_substituicoes.pack(side="left")

        self.btn_toggle_substituicoes = ctk.CTkButton(
            frame_titulo_substituicoes,
            text="−",
            width=25,
            height=25,
            command=self.toggle_frame_substituicoes,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_toggle_substituicoes.pack(side="right")

        # Frame para adicionar novas substituições
        self.frame_nova_substituicao = ctk.CTkFrame(self.frame_coluna_substituicoes, fg_color="transparent")
        self.frame_nova_substituicao.pack(fill="x", padx=5, pady=5)

        # Inputs para substituição
        subframe_inputs = ctk.CTkFrame(self.frame_nova_substituicao, fg_color="transparent")
        subframe_inputs.pack(fill="x")

        # Valor antigo
        self.entry_valor_antigo = ctk.CTkEntry(
            subframe_inputs,
            placeholder_text="Valor antigo...",
            width=135,
            height=30
        )
        self.entry_valor_antigo.pack(side="left", padx=(0, 5))

        # Valor novo
        self.entry_valor_novo = ctk.CTkEntry(
            subframe_inputs,
            placeholder_text="Valor novo...",
            width=135,
            height=30
        )
        self.entry_valor_novo.pack(side="left", padx=(0, 5))

        # Coluna específica
        self.entry_coluna = ctk.CTkEntry(
            subframe_inputs,
            placeholder_text="Coluna (opcional)...",
            width=140,
            height=30
        )
        self.entry_coluna.pack(side="left", padx=(0, 5))

        # Botão para adicionar substituição
        self.btn_adicionar_substituicao = ctk.CTkButton(
            subframe_inputs,
            text="➕",
            command=self.adicionar_substituicao,
            width=40,
            height=30,
            fg_color=self.cor_sucesso,
            hover_color="#218838"
        )
        self.btn_adicionar_substituicao.pack(side="left")

        # Frame para lista de substituições adicionadas
        self.frame_lista_substituicoes = ctk.CTkScrollableFrame(
            self.frame_coluna_substituicoes,
            height=80,
            fg_color="transparent"
        )
        self.frame_lista_substituicoes.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # === CONFIGURAÇÕES (COM BOTÃO DE RECOLHER) ===
        self.frame_config = ctk.CTkFrame(self.grid_frame)
        self.frame_config.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        frame_titulo_config = ctk.CTkFrame(self.frame_config, fg_color="transparent")
        frame_titulo_config.pack(fill="x", padx=10, pady=(5, 0))

        label_titulo_config = ctk.CTkLabel(
            frame_titulo_config,
            text="⚙️ Configurações de Substituição",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_config.pack(side="left")

        self.btn_toggle_config = ctk.CTkButton(
            frame_titulo_config,
            text="−",
            width=25,
            height=25,
            command=self.toggle_frame_config,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_toggle_config.pack(side="right")

        # Frame para opções
        self.frame_opcoes = ctk.CTkFrame(self.frame_config, fg_color="transparent")
        self.frame_opcoes.pack(fill="x", padx=10, pady=5)

        # Opções de busca
        self.radio_var = ctk.StringVar(value="contem")
        self.check_case_sensitive = ctk.BooleanVar(value=False)

        self.radio_contem = ctk.CTkRadioButton(
            self.frame_opcoes,
            text="Valor contém",
            variable=self.radio_var,
            value="contem",
            font=ctk.CTkFont(size=12)
        )
        self.radio_contem.pack(side="left", padx=(0, 15))

        self.radio_exato = ctk.CTkRadioButton(
            self.frame_opcoes,
            text="Valor exato",
            variable=self.radio_var,
            value="exato",
            font=ctk.CTkFont(size=12)
        )
        self.radio_exato.pack(side="left", padx=(0, 15))

        self.check_case = ctk.CTkCheckBox(
            self.frame_opcoes,
            text="Case Sensitive",
            variable=self.check_case_sensitive,
            font=ctk.CTkFont(size=12)
        )
        self.check_case.pack(side="left")

        # === BOTÃO EXECUTAR E STATUS ===
        self.btn_executar = ctk.CTkButton(
            self.grid_frame,
            text="🚀 Executar Substituições",
            command=self.executar_substituicoes,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.cor_sucesso,
            hover_color="#218838",
            state="disabled"
        )
        self.btn_executar.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(10, 5), padx=5)

        # Frame para status
        self.frame_status = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.frame_status.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        self.label_status = ctk.CTkLabel(
            self.frame_status,
            text="Selecione um arquivo Excel para começar",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.label_status.pack()

        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self.frame_status)
        self.progress_bar.set(0)

        # Configurar pesos do grid
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)
        self.grid_frame.columnconfigure(2, weight=1)

        # Inicialmente esconder frames que dependem de arquivo
        self.frame_duas_colunas.grid_remove()
        self.frame_config.grid_remove()

    # MÉTODOS PARA RECOLHER/EXPANDIR FRAMES
    def toggle_frame_abas(self):
        if self.frame_abas_visivel:
            self.frame_lista_abas.pack_forget()
            self.frame_controles_abas.pack_forget()
            self.btn_toggle_abas.configure(text="+")
            self.frame_abas_visivel = False
        else:
            self.frame_controles_abas.pack(fill="x", padx=5, pady=5)
            self.frame_lista_abas.pack(fill="both", expand=True, padx=5, pady=(0, 5))
            self.btn_toggle_abas.configure(text="−")
            self.frame_abas_visivel = True
        self.ajustar_tamanho_janela()

    def toggle_frame_substituicoes(self):
        if self.frame_substituicoes_visivel:
            self.frame_lista_substituicoes.pack_forget()
            self.frame_nova_substituicao.pack_forget()
            self.btn_toggle_substituicoes.configure(text="+")
            self.frame_substituicoes_visivel = False
        else:
            self.frame_nova_substituicao.pack(fill="x", padx=5, pady=5)
            self.frame_lista_substituicoes.pack(fill="both", expand=True, padx=5, pady=(0, 5))
            self.btn_toggle_substituicoes.configure(text="−")
            self.frame_substituicoes_visivel = True
        self.ajustar_tamanho_janela()

    def toggle_frame_config(self):
        if self.frame_config_visivel:
            self.frame_opcoes.pack_forget()
            self.btn_toggle_config.configure(text="+")
            self.frame_config_visivel = False
        else:
            self.frame_opcoes.pack(fill="x", padx=10, pady=5)
            self.btn_toggle_config.configure(text="−")
            self.frame_config_visivel = True
        self.ajustar_tamanho_janela()

    def ajustar_tamanho_janela(self):
        todos_recolhidos = (
            not self.frame_abas_visivel and
            not self.frame_substituicoes_visivel and
            not self.frame_config_visivel
        )

        if todos_recolhidos:
            self.master.geometry("1000x370+100+50")
        else:
            self.master.geometry("1000x650+100+50")

    # MÉTODOS PRINCIPAIS
    def adicionar_substituicao(self):
        """Adiciona uma nova regra de substituição"""
        valor_antigo = self.entry_valor_antigo.get().strip()
        valor_novo = self.entry_valor_novo.get().strip()
        coluna = self.entry_coluna.get().strip()

        if not valor_antigo:
            messagebox.showwarning("Aviso", "Digite o valor a ser substituído!")
            return

        # Criar regra de substituição
        substituicao = {
            'valor_antigo': valor_antigo,
            'valor_novo': valor_novo,
            'coluna': coluna if coluna else None,
            'tipo_busca': self.radio_var.get(),
            'case_sensitive': self.check_case_sensitive.get()
        }

        # Adicionar à lista
        self.substituicoes.append(substituicao)

        # Atualizar interface
        self.atualizar_lista_substituicoes()

        # Limpar campos
        self.entry_valor_antigo.delete(0, 'end')
        self.entry_valor_novo.delete(0, 'end')
        self.entry_coluna.delete(0, 'end')

        self.label_status.configure(
            text=f"Regra adicionada! Total: {len(self.substituicoes)}", 
            text_color="blue"
        )

    def atualizar_lista_substituicoes(self):
        """Atualiza a lista visual de substituições"""
        for widget in self.frame_lista_substituicoes.winfo_children():
            widget.destroy()

        for i, substituicao in enumerate(self.substituicoes):
            frame_substituicao = ctk.CTkFrame(self.frame_lista_substituicoes, fg_color="gray")
            frame_substituicao.pack(fill="x", pady=1, padx=2)

            # Texto da substituição
            if substituicao['coluna']:
                texto = f"🔄 {substituicao['valor_antigo']} → {substituicao['valor_novo']} (Coluna: {substituicao['coluna']})"
            else:
                texto = f"🔄 {substituicao['valor_antigo']} → {substituicao['valor_novo']} (Todas as colunas)"

            label_substituicao = ctk.CTkLabel(
                frame_substituicao,
                text=texto,
                font=ctk.CTkFont(size=10, weight="bold"),
                anchor="w",
                text_color="black"
            )
            label_substituicao.pack(side="left", padx=5, pady=2, fill="x", expand=True)

            # Botão para remover
            btn_remover = ctk.CTkButton(
                frame_substituicao,
                text="✕",
                width=25,
                height=20,
                fg_color="red",
                hover_color="darkred",
                command=lambda idx=i: self.remover_substituicao(idx)
            )
            btn_remover.pack(side="right", padx=2)

    def remover_substituicao(self, index):
        """Remove uma substituição da lista"""
        if 0 <= index < len(self.substituicoes):
            self.substituicoes.pop(index)
            self.atualizar_lista_substituicoes()
            self.label_status.configure(
                text=f"Regra removida! Total: {len(self.substituicoes)}", 
                text_color="orange"
            )

    def selecionar_arquivo(self):
        """Seleciona um arquivo Excel e carrega suas abas"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        
        if arquivo:
            self.arquivo_selecionado = arquivo
            self.entry_arquivo.configure(state="normal")
            self.entry_arquivo.delete(0, "end")
            self.entry_arquivo.insert(0, arquivo.split("/")[-1])
            self.entry_arquivo.configure(state="readonly")
            
            self.carregar_abas(arquivo)
            
            self.frame_duas_colunas.grid()
            self.frame_config.grid()
            
            self.label_status.configure(
                text="Arquivo carregado com sucesso! Selecione as abas e adicione regras de substituição.", 
                text_color="green"
            )
            self.btn_selecionar_todas.configure(state="normal")
            self.btn_limpar_selecao.configure(state="normal")

    def carregar_abas(self, arquivo):
        """Carrega todas as abas do arquivo Excel"""
        try:
            for widget in self.frame_lista_abas.winfo_children():
                widget.destroy()
            
            excel_file = pd.ExcelFile(arquivo)
            self.abas_disponiveis = excel_file.sheet_names
            self.abas_selecionadas = []
            
            for aba in self.abas_disponiveis:
                self.criar_checkbox_aba(aba)
            
            self.atualizar_label_selecao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo Excel:\n{str(e)}")

    def criar_checkbox_aba(self, nome_aba):
        """Cria um checkbox para uma aba específica"""
        var = ctk.BooleanVar(value=False)
        
        frame_aba = ctk.CTkFrame(self.frame_lista_abas, fg_color="gray")
        frame_aba.pack(fill="x", pady=1, padx=2)
        
        checkbox = ctk.CTkCheckBox(
            frame_aba,
            text=nome_aba,
            variable=var,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self.atualizar_selecao_aba(nome_aba, var.get()),
            text_color="black",
        )
        checkbox.pack(side="left", padx=5, pady=2)
        
        checkbox.var = var
        checkbox.nome_aba = nome_aba

    # Os métodos restantes (selecionar_todas_abas, limpar_selecao_abas, atualizar_selecao_aba, 
    # atualizar_label_selecao, verificar_pronto_execucao) são praticamente idênticos aos da classe anterior

    def atualizar_selecao_aba(self, nome_aba, selecionada):
        if selecionada and nome_aba not in self.abas_selecionadas:
            self.abas_selecionadas.append(nome_aba)
        elif not selecionada and nome_aba in self.abas_selecionadas:
            self.abas_selecionadas.remove(nome_aba)
        
        self.atualizar_label_selecao()
        self.verificar_pronto_execucao()

    def selecionar_todas_abas(self):
        for widget in self.frame_lista_abas.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkCheckBox):
                        child.var.set(True)
                        if child.nome_aba not in self.abas_selecionadas:
                            self.abas_selecionadas.append(child.nome_aba)
        
        self.atualizar_label_selecao()
        self.verificar_pronto_execucao()

    def limpar_selecao_abas(self):
        for widget in self.frame_lista_abas.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkCheckBox):
                        child.var.set(False)
        
        self.abas_selecionadas = []
        self.atualizar_label_selecao()
        self.verificar_pronto_execucao()

    def atualizar_label_selecao(self):
        total = len(self.abas_disponiveis)
        selecionadas = len(self.abas_selecionadas)
        
        if selecionadas == 0:
            texto = "Nenhuma aba selecionada"
            cor = "gray"
        elif selecionadas == total:
            texto = f"Todas as {total} abas"
            cor = "green"
        else:
            texto = f"{selecionadas}/{total} abas"
            cor = "blue"
        
        self.label_selecao_abas.configure(text=texto, text_color=cor)

    def verificar_pronto_execucao(self):
        if (self.arquivo_selecionado and 
            self.abas_selecionadas and 
            self.substituicoes):
            
            self.btn_executar.configure(state="normal")
            status_text = f"Pronto! {len(self.abas_selecionadas)} aba(s) e {len(self.substituicoes)} regra(s)"
            self.label_status.configure(text=status_text, text_color="green")
        else:
            self.btn_executar.configure(state="disabled")
            if self.arquivo_selecionado and self.abas_selecionadas:
                self.label_status.configure(text="Adicione pelo menos uma regra de substituição", text_color="orange")

    def executar_substituicoes(self):
        """Executa o processo de substituição de valores"""
        if not self.arquivo_selecionado or not self.abas_selecionadas:
            messagebox.showwarning("Aviso", "Selecione um arquivo e pelo menos uma aba!")
            return

        if not self.substituicoes:
            messagebox.showwarning("Aviso", "Adicione pelo menos uma regra de substituição!")
            return

        self.progress_bar.pack(fill="x", pady=(5, 0))
        self.progress_bar.set(0.1)
        
        self.label_status.configure(text="Iniciando processo de substituição...", text_color="orange")
        self.btn_executar.configure(state="disabled")

        try:
            config = {
                'substituicoes': self.substituicoes,
                'abas_selecionadas': self.abas_selecionadas
            }

            self.progress_bar.set(0.3)
            
            resultado = self.controller.processar_arquivo(
                self.arquivo_selecionado, 
                config
            )

            self.progress_bar.set(0.8)

            if resultado:
                self.salvar_arquivo_processado(resultado)
            else:
                raise Exception("Nenhum dado processado")

        except Exception as e:
            self.label_status.configure(text="❌ Erro no processamento!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")
            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")

    def salvar_arquivo_processado(self, dados_processados):
        caminho = filedialog.asksaveasfilename(
            title="Salvar arquivo processado", 
            defaultextension=".xlsx", 
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )

        if not caminho:
            self.label_status.configure(text="Operação cancelada pelo usuário", text_color="gray")
            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")
            return

        try:
            with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
                for aba, df in dados_processados.items():
                    df.to_excel(writer, sheet_name=aba, index=False)
            
            self.progress_bar.set(1.0)
            
            total_regras = len(self.substituicoes)
            total_abas = len(self.abas_selecionadas)
            
            self.label_status.configure(
                text=f"✅ Sucesso! {total_abas} aba(s) processada(s) com {total_regras} regra(s)", 
                text_color="green"
            )
            
            messagebox.showinfo(
                "Concluído", 
                f"Arquivo processado com sucesso!\n\n"
                f"• Abas processadas: {total_abas}\n"
                f"• Regras aplicadas: {total_regras}\n"
                f"• Local: {caminho}"
            )
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro ao salvar arquivo!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")
        
        finally:
            self.after(3000, self.progress_bar.pack_forget)
            self.btn_executar.configure(state="normal")