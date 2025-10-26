import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from controllers.excluir_linhas_controller import ExcluirLinhasController

class ExcluirLinhas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.controller = ExcluirLinhasController()

        master.geometry("710x650")
        
        # Configuração de cores
        self.cor_primaria = "#238AD9"
        self.cor_sucesso = "#238AD9"
        self.cor_perigo = "#DC3545"
        self.cor_alerta = "#FFC107"

        # Variáveis
        self.arquivo_selecionado = None
        self.abas_disponiveis = []
        self.abas_selecionadas = []
        self.criterios_exclusao = []
        
        # Variável para controle de frames recolhíveis
        self.frame_abas_visivel = True
        self.frame_criterios_visivel = True
        self.frame_config_visivel = True

        # === LAYOUT PRINCIPAL COMPACTO ===
        # Frame principal com grid para melhor organização
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Botão Voltar (fixo no topo)
        self.btn_back = ctk.CTkButton(
            self.grid_frame, 
            text="←", 
            command=lambda: master.show_frame(master.menu_frame), 
            width=20,
            height=35,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_back.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Label principal
        self.label = ctk.CTkLabel(
            self.grid_frame,
            text="🗑️ Excluir Linhas de Planilhas",
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
            hover_color="#1A6BA6"
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

        # === LAYOUT EM COLUNAS: ABAS E CRITÉRIOS LADO A LADO ===
        # Frame para conter abas e critérios lado a lado
        self.frame_duas_colunas = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.frame_duas_colunas.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        # Coluna 1: Abas (40% da largura)
        self.frame_coluna_abas = ctk.CTkFrame(self.frame_duas_colunas)
        self.frame_coluna_abas.pack(side="left", fill="both", expand=True, padx=(5, 5))

        # Coluna 2: Critérios (60% da largura)
        self.frame_coluna_criterios = ctk.CTkFrame(self.frame_duas_colunas)
        self.frame_coluna_criterios.pack(side="right", fill="both", expand=True, padx=(5, 5))

        # === FRAME DE ABAS (COM BOTÃO DE RECOLHER) ===
        frame_titulo_abas = ctk.CTkFrame(self.frame_coluna_abas, fg_color="transparent")
        frame_titulo_abas.pack(fill="x", padx=5, pady=(5, 0))

        label_titulo_abas = ctk.CTkLabel(
            frame_titulo_abas,
            text="📊 Abas para Processar",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_abas.pack(side="left")

        # Botão para recolher/expandir frame de abas
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
            width=80,
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
            width=80,
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

        # Frame para a lista de abas (scrollable) - COMPACTO
        self.frame_lista_abas = ctk.CTkScrollableFrame(
            self.frame_coluna_abas,
            height=120,
            fg_color="transparent"
        )
        self.frame_lista_abas.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # === FRAME DE CRITÉRIOS (COM BOTÃO DE RECOLHER) ===
        frame_titulo_criterios = ctk.CTkFrame(self.frame_coluna_criterios, fg_color="transparent")
        frame_titulo_criterios.pack(fill="x", padx=5, pady=(5, 0))

        label_titulo_criterios = ctk.CTkLabel(
            frame_titulo_criterios,
            text="🎯 Critérios de Exclusão",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_criterios.pack(side="left")

        # Botão para recolher/expandir frame de critérios
        self.btn_toggle_criterios = ctk.CTkButton(
            frame_titulo_criterios,
            text="−",
            width=25,
            height=25,
            command=self.toggle_frame_criterios,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_toggle_criterios.pack(side="right")

        # Frame para adicionar novos critérios
        self.frame_novo_criterio = ctk.CTkFrame(self.frame_coluna_criterios, fg_color="transparent")
        self.frame_novo_criterio.pack(fill="x", padx=5, pady=5)

        # Inputs em linha única compacta
        subframe_inputs = ctk.CTkFrame(self.frame_novo_criterio, fg_color="transparent")
        subframe_inputs.pack(fill="x")

        # Valor a excluir
        self.entry_valor = ctk.CTkEntry(
            subframe_inputs,
            placeholder_text="Valor a excluir...",
            width=135,
            height=30
        )
        self.entry_valor.pack(side="left", padx=(0, 5))

        # Coluna específica
        self.entry_coluna = ctk.CTkEntry(
            subframe_inputs,
            placeholder_text="Coluna (opcional)...",
            width=135,
            height=30
        )
        self.entry_coluna.pack(side="left", padx=(0, 5))

        # Botão para adicionar critério
        self.btn_adicionar_criterio = ctk.CTkButton(
            subframe_inputs,
            text="➕",
            command=self.adicionar_criterio,
            width=40,
            height=30,
            fg_color=self.cor_sucesso,
            hover_color="#218838"
        )
        self.btn_adicionar_criterio.pack(side="left")

        # Frame para lista de critérios adicionados - COMPACTO
        self.frame_lista_criterios = ctk.CTkScrollableFrame(
            self.frame_coluna_criterios,
            height=80,
            fg_color="transparent"
        )
        self.frame_lista_criterios.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # === CONFIGURAÇÕES AVANÇADAS (COM BOTÃO DE RECOLHER) ===
        self.frame_config = ctk.CTkFrame(self.grid_frame)
        self.frame_config.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        frame_titulo_config = ctk.CTkFrame(self.frame_config, fg_color="transparent")
        frame_titulo_config.pack(fill="x", padx=10, pady=(5, 0))

        label_titulo_config = ctk.CTkLabel(
            frame_titulo_config,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_config.pack(side="left")

        # Botão para recolher/expandir configurações
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

        # Frame para opções avançadas
        self.frame_opcoes = ctk.CTkFrame(self.frame_config, fg_color="transparent")
        self.frame_opcoes.pack(fill="x", padx=10, pady=5)

        # Opções em linha única para economizar espaço
        self.check_var_vazias = ctk.BooleanVar(value=True)
        self.check_duplicatas = ctk.BooleanVar(value=False)
        self.radio_var = ctk.StringVar(value="contem")

        self.check_vazias = ctk.CTkCheckBox(
            self.frame_opcoes,
            text="Linhas vazias",
            variable=self.check_var_vazias,
            font=ctk.CTkFont(size=12)
        )
        self.check_vazias.pack(side="left", padx=(0, 15))

        self.check_duplicatas = ctk.CTkCheckBox(
            self.frame_opcoes,
            text="Duplicatas",
            variable=self.check_duplicatas,
            font=ctk.CTkFont(size=12)
        )
        self.check_duplicatas.pack(side="left", padx=(0, 15))

        self.radio_contem = ctk.CTkRadioButton(
            self.frame_opcoes,
            text="Contém",
            variable=self.radio_var,
            value="contem",
            font=ctk.CTkFont(size=12)
        )
        self.radio_contem.pack(side="left", padx=(0, 10))

        self.radio_exato = ctk.CTkRadioButton(
            self.frame_opcoes,
            text="Exato",
            variable=self.radio_var,
            value="exato",
            font=ctk.CTkFont(size=12)
        )
        self.radio_exato.pack(side="left")

        # === BOTÃO EXECUTAR E STATUS ===
        self.btn_executar = ctk.CTkButton(
            self.grid_frame,
            text="🚀 Executar Exclusão",
            command=self.executar_exclusao,
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

        # Barra de progresso (inicialmente oculta)
        self.progress_bar = ctk.CTkProgressBar(self.frame_status)
        self.progress_bar.set(0)

        # Configurar pesos do grid para responsividade
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)
        self.grid_frame.columnconfigure(2, weight=1)

        # Inicialmente esconder frames que dependem de arquivo
        self.frame_duas_colunas.grid_remove()
        self.frame_config.grid_remove()

    # NOVOS MÉTODOS PARA RECOLHER/EXPANDIR FRAMES
    def toggle_frame_abas(self):
        """Recolhe ou expande o frame de abas"""
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

    def toggle_frame_criterios(self):
        """Recolhe ou expande o frame de critérios"""
        if self.frame_criterios_visivel:
            self.frame_lista_criterios.pack_forget()
            self.frame_novo_criterio.pack_forget()
            self.btn_toggle_criterios.configure(text="+")
            self.frame_criterios_visivel = False
        else:
            self.frame_novo_criterio.pack(fill="x", padx=5, pady=5)
            self.frame_lista_criterios.pack(fill="both", expand=True, padx=5, pady=(0, 5))
            self.btn_toggle_criterios.configure(text="−")
            self.frame_criterios_visivel = True
        self.ajustar_tamanho_janela()

    def toggle_frame_config(self):
        """Recolhe ou expande o frame de configurações"""
        if self.frame_config_visivel:
            self.frame_opcoes.pack_forget()
            self.btn_toggle_config.configure(text="+")
            self.frame_config_visivel = False
        else:
            self.frame_opcoes.pack(fill="x", padx=10, pady=5)
            self.btn_toggle_config.configure(text="−")
            self.frame_config_visivel = True
        self.ajustar_tamanho_janela()

    # MÉTODOS EXISTENTES (mantenha todos os outros métodos como estão)
    def adicionar_criterio(self):
        """Adiciona um novo critério à lista"""
        valor = self.entry_valor.get().strip()
        coluna = self.entry_coluna.get().strip()

        if not valor:
            messagebox.showwarning("Aviso", "Digite um valor para excluir!")
            return

        # Criar critério
        criterio = {
            'valor': valor,
            'coluna': coluna if coluna else None,
            'tipo_busca': self.radio_var.get()
        }

        # Adicionar à lista
        self.criterios_exclusao.append(criterio)

        # Atualizar interface
        self.atualizar_lista_criterios()

        # Limpar campos
        self.entry_valor.delete(0, 'end')
        self.entry_coluna.delete(0, 'end')

        self.label_status.configure(text=f"Critério adicionado! Total: {len(self.criterios_exclusao)}", text_color="blue")

    def atualizar_lista_criterios(self):
        """Atualiza a lista visual de critérios"""
        # Limpar lista atual
        for widget in self.frame_lista_criterios.winfo_children():
            widget.destroy()

        # Adicionar cada critério
        for i, criterio in enumerate(self.criterios_exclusao):
            frame_criterio = ctk.CTkFrame(self.frame_lista_criterios, fg_color="gray")
            frame_criterio.pack(fill="x", pady=1, padx=2)

            # Texto do critério
            if criterio['coluna']:
                texto = f"🔍 {criterio['valor']} → Coluna: {criterio['coluna']}"
            else:
                texto = f"🔍 {criterio['valor']} → Todas as colunas"

            label_criterio = ctk.CTkLabel(
                frame_criterio,
                text=texto,
                font=ctk.CTkFont(size=10, weight="bold"),
                anchor="w",
                text_color="black"
            )
            label_criterio.pack(side="left", padx=5, pady=2, fill="x", expand=True)

            # Botão para remover critério
            btn_remover = ctk.CTkButton(
                frame_criterio,
                text="✕",
                width=25,
                height=20,
                fg_color="red",
                hover_color="darkred",
                command=lambda idx=i: self.remover_criterio(idx)
            )
            btn_remover.pack(side="right", padx=2)

    def remover_criterio(self, index):
        """Remove um critério da lista"""
        if 0 <= index < len(self.criterios_exclusao):
            self.criterios_exclusao.pop(index)
            self.atualizar_lista_criterios()
            self.label_status.configure(text=f"Critério removido! Total: {len(self.criterios_exclusao)}", text_color="orange")

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
            
            # Carregar abas do arquivo
            self.carregar_abas(arquivo)
            
            # Mostrar frames adicionais
            self.frame_duas_colunas.grid()
            self.frame_config.grid()
            
            self.label_status.configure(text="Arquivo carregado com sucesso! Selecione as abas e adicione critérios.", text_color="green")
            self.btn_selecionar_todas.configure(state="normal")
            self.btn_limpar_selecao.configure(state="normal")

    def carregar_abas(self, arquivo):
        """Carrega todas as abas do arquivo Excel"""
        try:
            # Limpar lista anterior
            for widget in self.frame_lista_abas.winfo_children():
                widget.destroy()
            
            # Ler abas do Excel
            excel_file = pd.ExcelFile(arquivo)
            self.abas_disponiveis = excel_file.sheet_names
            self.abas_selecionadas = []
            
            # Criar checkboxes para cada aba
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
        
        # Armazenar referência
        checkbox.var = var
        checkbox.nome_aba = nome_aba

    def atualizar_selecao_aba(self, nome_aba, selecionada):
        """Atualiza a lista de abas selecionadas"""
        if selecionada and nome_aba not in self.abas_selecionadas:
            self.abas_selecionadas.append(nome_aba)
        elif not selecionada and nome_aba in self.abas_selecionadas:
            self.abas_selecionadas.remove(nome_aba)
        
        self.atualizar_label_selecao()
        self.verificar_pronto_execucao()

    def selecionar_todas_abas(self):
        """Seleciona todas as abas disponíveis"""
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
        """Limpa a seleção de todas as abas"""
        for widget in self.frame_lista_abas.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkCheckBox):
                        child.var.set(False)
        
        self.abas_selecionadas = []
        self.atualizar_label_selecao()
        self.verificar_pronto_execucao()

    def atualizar_label_selecao(self):
        """Atualiza o label que mostra quantas abas estão selecionadas"""
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
        """Verifica se pode habilitar o botão executar"""
        if (self.arquivo_selecionado and 
            self.abas_selecionadas and 
            (self.criterios_exclusao or self.check_var_vazias.get() or self.check_duplicatas.get())):
            
            self.btn_executar.configure(state="normal")
            
            if self.criterios_exclusao:
                status_text = f"Pronto! {len(self.abas_selecionadas)} aba(s) e {len(self.criterios_exclusao)} critério(s)"
            else:
                status_text = f"Pronto! {len(self.abas_selecionadas)} aba(s) com filtros básicos"
                
            self.label_status.configure(text=status_text, text_color="green")
        else:
            self.btn_executar.configure(state="disabled")
            if self.arquivo_selecionado and self.abas_selecionadas:
                self.label_status.configure(text="Adicione pelo menos um critério de exclusão", text_color="orange")

    def executar_exclusao(self):
        """Executa o processo de exclusão de linhas"""
        if not self.arquivo_selecionado or not self.abas_selecionadas:
            messagebox.showwarning("Aviso", "Selecione um arquivo e pelo menos uma aba!")
            return

        if not self.criterios_exclusao and not self.check_var_vazias.get() and not self.check_duplicatas.get():
            messagebox.showwarning("Aviso", "Adicione pelo menos um critério de exclusão!")
            return

        # Mostrar barra de progresso
        self.progress_bar.pack(fill="x", pady=(5, 0))
        self.progress_bar.set(0.1)
        
        # Atualizar status
        self.label_status.configure(text="Iniciando processo de exclusão...", text_color="orange")
        self.btn_executar.configure(state="disabled")

        try:
            # Coletar configurações
            config = {
                'excluir_vazias': self.check_var_vazias.get(),
                'excluir_duplicatas': self.check_duplicatas.get(),
                'criterios_personalizados': self.criterios_exclusao,
                'tipo_busca': self.radio_var.get(),
                'abas_selecionadas': self.abas_selecionadas
            }

            # Processar arquivo
            self.progress_bar.set(0.3)
            
            # Chamar o controller para processar
            resultado = self.controller.processar_arquivo(
                self.arquivo_selecionado, 
                config
            )

            self.progress_bar.set(0.8)

            if resultado:
                # Salvar arquivo processado
                self.salvar_arquivo_processado(resultado)
            else:
                raise Exception("Nenhum dado processado")

        except Exception as e:
            self.label_status.configure(text="❌ Erro no processamento!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")
            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")

    def ajustar_tamanho_janela(self):
        """
        Ajusta o tamanho da janela conforme os frames visíveis.
        """
        todos_recolhidos = (
            not self.frame_abas_visivel and
            not self.frame_criterios_visivel and
            not self.frame_config_visivel
        )

        if todos_recolhidos:
            self.master.geometry("750x360+100+50")
        else:
            self.master.geometry("770x650+100+50")



    def salvar_arquivo_processado(self, dados_processados):
        """Salva o arquivo com as linhas excluídas"""
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
            # Salvar o arquivo processado
            with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
                for aba, df in dados_processados.items():
                    df.to_excel(writer, sheet_name=aba, index=False)
            
            self.progress_bar.set(1.0)
            
            # Mensagem de resumo
            total_criterios = len(self.criterios_exclusao)
            total_abas = len(self.abas_selecionadas)
            
            self.label_status.configure(
                text=f"✅ Sucesso! {total_abas} aba(s) processada(s) com {total_criterios} critério(s)", 
                text_color="green"
            )
            
            messagebox.showinfo(
                "Concluído", 
                f"Arquivo processado com sucesso!\n\n"
                f"• Abas processadas: {total_abas}\n"
                f"• Critérios aplicados: {total_criterios}\n"
                f"• Local: {caminho}"
            )
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro ao salvar arquivo!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")
        
        finally:
            # Esconder barra de progresso após 3 segundos
            self.after(3000, self.progress_bar.pack_forget)
            self.btn_executar.configure(state="normal")