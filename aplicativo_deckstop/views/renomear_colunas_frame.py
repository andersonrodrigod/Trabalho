# views/renomear_colunas.py
import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from controllers.renomear_colunas_controller import RenomearColunasController

class RenomearColunas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.controller = RenomearColunasController()
        master.geometry("850x750+100+50")
        
        # Configuração de cores
        self.cor_primaria = "#17A2B8"  # Azul para diferenciar das abas
        self.cor_sucesso = "#28A745"
        self.cor_perigo = "#DC3545"
        self.cor_alerta = "#FFC107"
        self.cor_info = "#6F42C1"

        # Variáveis
        self.arquivo_selecionado = None
        self.renomeacoes_colunas = []  # Lista de tuplas (aba, antigo, novo)

        # === LAYOUT PRINCIPAL ===
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Botão Voltar
        self.btn_back = ctk.CTkButton(
            self.grid_frame, 
            text="← Voltar", 
            command=lambda: master.show_frame(master.menu_frame), 
            width=80,
            height=30,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_back.grid(row=0, column=0, sticky="w", pady=(0, 15))

        # Label principal
        self.label = ctk.CTkLabel(
            self.grid_frame,
            text="📊 Renomear Colunas",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.cor_primaria
        )
        self.label.grid(row=0, column=1, columnspan=2, pady=(0, 15))

        # === SELEÇÃO DE ARQUIVO ===
        self.frame_arquivo = ctk.CTkFrame(self.grid_frame)
        self.frame_arquivo.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 15), padx=5)

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
            text="Procurar Arquivo",
            command=self.selecionar_arquivo,
            width=120,
            height=32,
            fg_color=self.cor_primaria,
            hover_color="#138496"
        )
        self.btn_selecionar_arquivo.pack(side="left", padx=(0, 10))

        self.entry_arquivo = ctk.CTkEntry(
            subframe_arquivo,
            width=400,
            height=32,
            placeholder_text="Nenhum arquivo selecionado",
            state="readonly"
        )
        self.entry_arquivo.pack(side="left", fill="x", expand=True)

        # === RENOMEAR COLUNAS - LAYOUT EM COLUNAS ===
        self.frame_colunas = ctk.CTkFrame(self.grid_frame)
        self.frame_colunas.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 15), padx=5)
        
        # Configurar pesos para expandir
        self.grid_frame.rowconfigure(2, weight=1)

        # Frame principal com duas colunas
        frame_colunas_principal = ctk.CTkFrame(self.frame_colunas, fg_color="transparent")
        frame_colunas_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # === COLUNA 1: CONTROLES DE ENTRADA ===
        frame_coluna_controles = ctk.CTkFrame(frame_colunas_principal)
        frame_coluna_controles.pack(side="left", fill="both", expand=True, padx=(0, 10))

        label_titulo_controles = ctk.CTkLabel(
            frame_coluna_controles,
            text="📝 Adicionar Renomeação",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_controles.pack(anchor="w", pady=(0, 15))

        # Combobox para selecionar aba
        self.label_aba = ctk.CTkLabel(
            frame_coluna_controles,
            text="Selecionar aba:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_aba.pack(anchor="w", pady=(0, 5))

        self.combobox_abas = ctk.CTkComboBox(
            frame_coluna_controles,
            values=[],
            state="readonly",
            width=250,
            height=35,
            command=self.atualizar_colunas_aba
        )
        self.combobox_abas.pack(anchor="w", pady=(0, 15), fill="x")

        # Combobox para selecionar coluna
        self.label_coluna = ctk.CTkLabel(
            frame_coluna_controles,
            text="Coluna para renomear:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_coluna.pack(anchor="w", pady=(0, 5))

        self.combobox_colunas = ctk.CTkComboBox(
            frame_coluna_controles,
            values=[],
            state="readonly",
            width=250,
            height=35
        )
        self.combobox_colunas.pack(anchor="w", pady=(0, 15), fill="x")

        # Input para novo nome da coluna
        self.label_nova_coluna = ctk.CTkLabel(
            frame_coluna_controles,
            text="Novo nome da coluna:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_nova_coluna.pack(anchor="w", pady=(0, 5))

        self.entry_nova_coluna = ctk.CTkEntry(
            frame_coluna_controles,
            placeholder_text="Digite o novo nome...",
            width=250,
            height=35
        )
        self.entry_nova_coluna.pack(anchor="w", pady=(0, 20), fill="x")

        # Botão para adicionar renomeação de coluna
        self.btn_adicionar_coluna = ctk.CTkButton(
            frame_coluna_controles,
            text="➕ Adicionar Renomeação",
            command=self.adicionar_renomeacao_coluna,
            width=200,
            height=38,
            fg_color=self.cor_sucesso,
            hover_color="#218838",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_adicionar_coluna.pack(anchor="w", pady=(0, 15))

        # === COLUNA 2: LISTA DE ALTERAÇÕES ===
        frame_coluna_lista = ctk.CTkFrame(frame_colunas_principal)
        frame_coluna_lista.pack(side="right", fill="both", expand=True, padx=(10, 0))

        label_titulo_lista = ctk.CTkLabel(
            frame_coluna_lista,
            text="📋 Alterações Pendentes",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_lista.pack(anchor="w", pady=(0, 10))

        self.frame_lista_colunas = ctk.CTkScrollableFrame(
            frame_coluna_lista,
            height=180,
            fg_color="#f8f9fa"
        )
        self.frame_lista_colunas.pack(fill="both", expand=True, pady=(0, 10))

        # Label quando não há renomeações
        self.label_lista_vazia = ctk.CTkLabel(
            self.frame_lista_colunas,
            text="Nenhuma renomeação adicionada\n\nUse o painel ao lado para adicionar renomeações de colunas.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            justify="center"
        )
        self.label_lista_vazia.pack(expand=True, pady=20)

        # === OPÇÕES DE SALVAMENTO ===
        self.frame_opcoes_salvamento = ctk.CTkFrame(self.grid_frame)
        self.frame_opcoes_salvamento.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        label_titulo_salvamento = ctk.CTkLabel(
            self.frame_opcoes_salvamento,
            text="💾 Opções de Salvamento",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_salvamento.pack(anchor="w", pady=(10, 8), padx=10)

        frame_radio_salvamento = ctk.CTkFrame(self.frame_opcoes_salvamento, fg_color="transparent")
        frame_radio_salvamento.pack(fill="x", padx=10, pady=(0, 10))

        self.radio_var_salvamento = ctk.StringVar(value="novo")

        self.radio_novo_arquivo = ctk.CTkRadioButton(
            frame_radio_salvamento,
            text="🆕 Salvar como NOVO arquivo (Recomendado)",
            variable=self.radio_var_salvamento,
            value="novo",
            font=ctk.CTkFont(size=12)
        )
        self.radio_novo_arquivo.pack(side="left", padx=(0, 20))

        self.radio_mesmo_arquivo = ctk.CTkRadioButton(
            frame_radio_salvamento,
            text="💾 Sobrescrever MESMO arquivo",
            variable=self.radio_var_salvamento,
            value="mesmo",
            font=ctk.CTkFont(size=12)
        )
        self.radio_mesmo_arquivo.pack(side="left")

        # === BOTÃO EXECUTAR ===
        self.btn_executar = ctk.CTkButton(
            self.grid_frame,
            text="🚀 Executar Renomeações de Colunas",
            command=self.executar_renomeacoes,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.cor_primaria,
            hover_color="#138496",
            state="disabled"
        )
        self.btn_executar.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(10, 8), padx=5)

        # === STATUS ===
        self.frame_status = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.frame_status.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 5))

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

        # Inicialmente esconder frames
        self.frame_colunas.grid_remove()
        self.frame_opcoes_salvamento.grid_remove()

    # MÉTODOS PRINCIPAIS
    def selecionar_arquivo(self):
        """Seleciona o arquivo Excel"""
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
            
            # Carregar arquivo no controller
            self.carregar_arquivo()

    def carregar_arquivo(self):
        """Carrega o arquivo no controller e atualiza a interface"""
        try:
            self.progress_bar.pack(fill="x", pady=(5, 0))
            self.progress_bar.set(0.3)
            
            self.label_status.configure(text="Carregando arquivo...", text_color="orange")
            
            resultado = self.controller.carregar_arquivo(self.arquivo_selecionado)
            
            self.progress_bar.set(1.0)
            
            if resultado['sucesso']:
                # Atualizar combobox de abas
                self.combobox_abas.configure(values=resultado['abas'])
                
                if resultado['abas']:
                    self.combobox_abas.set(resultado['abas'][0])
                    # Atualizar colunas da primeira aba
                    self.atualizar_colunas_aba(resultado['abas'][0])
                
                # Mostrar frames
                self.frame_colunas.grid()
                self.frame_opcoes_salvamento.grid()
                
                # Habilitar controles
                self.btn_adicionar_coluna.configure(state="normal")
                
                self.label_status.configure(
                    text=f"✅ Arquivo carregado! {resultado['total_abas']} aba(s) encontrada(s).",
                    text_color="green"
                )
                
            else:
                self.label_status.configure(text="❌ Erro ao carregar arquivo!", text_color="red")
                messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{resultado['erro']}")
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro no carregamento!", text_color="red")
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")
        finally:
            self.after(1000, self.progress_bar.pack_forget)

    def atualizar_colunas_aba(self, aba_selecionada):
        """Atualiza a lista de colunas quando uma aba é selecionada"""
        if hasattr(self.controller, 'colunas_por_aba') and aba_selecionada in self.controller.colunas_por_aba:
            colunas = self.controller.colunas_por_aba[aba_selecionada]
            self.combobox_colunas.configure(values=colunas)
            if colunas:
                self.combobox_colunas.set(colunas[0])

    def adicionar_renomeacao_coluna(self):
        """Adiciona uma renomeação de coluna à lista"""
        aba = self.combobox_abas.get()
        coluna_antiga = self.combobox_colunas.get()
        coluna_nova = self.entry_nova_coluna.get().strip()

        if not coluna_nova:
            messagebox.showwarning("Aviso", "Digite o novo nome da coluna!")
            return

        if coluna_antiga == coluna_nova:
            messagebox.showwarning("Aviso", "O novo nome deve ser diferente do nome atual!")
            return

        # Verificar se já existe esta renomeação
        for aba_existente, antiga, nova in self.renomeacoes_colunas:
            if aba_existente == aba and antiga == coluna_antiga:
                messagebox.showwarning("Aviso", f"A coluna '{coluna_antiga}' na aba '{aba}' já tem uma renomeação pendente!")
                return

        # Adicionar à lista
        self.renomeacoes_colunas.append((aba, coluna_antiga, coluna_nova))
        self.atualizar_lista_colunas()

        # Limpar campo
        self.entry_nova_coluna.delete(0, 'end')

        self.label_status.configure(
            text=f"Renomeação de coluna adicionada: {aba}.{coluna_antiga} → {coluna_nova}",
            text_color="blue"
        )

        # Habilitar botão executar se houver renomeações
        self.verificar_renomeacoes()

    def atualizar_lista_colunas(self):
        """Atualiza a lista visual de renomeações de colunas"""
        # Esconder label de lista vazia se houver itens
        if self.renomeacoes_colunas:
            self.label_lista_vazia.pack_forget()
        else:
            self.label_lista_vazia.pack(expand=True, pady=20)
            return

        # Limpar widgets antigos (exceto o label de lista vazia)
        for widget in self.frame_lista_colunas.winfo_children():
            if widget != self.label_lista_vazia:
                widget.destroy()

        for i, (aba, antiga, nova) in enumerate(self.renomeacoes_colunas):
            frame_renomeacao = ctk.CTkFrame(self.frame_lista_colunas, fg_color="#E8F5E8", height=35)
            frame_renomeacao.pack(fill="x", pady=2, padx=2)

            label_renomeacao = ctk.CTkLabel(
                frame_renomeacao,
                text=f"📊 {aba}.{antiga} → {nova}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2E7D32",
                anchor="w"
            )
            label_renomeacao.pack(side="left", padx=8, pady=6, fill="x", expand=True)

            btn_remover = ctk.CTkButton(
                frame_renomeacao,
                text="✕",
                width=30,
                height=25,
                fg_color="red",
                hover_color="darkred",
                font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda idx=i: self.remover_renomeacao_coluna(idx)
            )
            btn_remover.pack(side="right", padx=5, pady=5)

    def remover_renomeacao_coluna(self, index):
        """Remove uma renomeação de coluna da lista"""
        if 0 <= index < len(self.renomeacoes_colunas):
            aba, antiga, nova = self.renomeacoes_colunas.pop(index)
            self.atualizar_lista_colunas()
            self.label_status.configure(
                text=f"Renomeação de coluna removida: {aba}.{antiga} → {nova}",
                text_color="orange"
            )
            self.verificar_renomeacoes()

    def verificar_renomeacoes(self):
        """Verifica se há renomeações para habilitar o botão executar"""
        if self.renomeacoes_colunas:
            total_colunas = len(self.renomeacoes_colunas)
            self.btn_executar.configure(state="normal")
            self.label_status.configure(
                text=f"Pronto! {total_colunas} renomeação(ões) de coluna(s) pendente(s)",
                text_color="green"
            )
        else:
            self.btn_executar.configure(state="disabled")
            self.label_status.configure(
                text="Adicione renomeações de colunas para continuar",
                text_color="gray"
            )

    def executar_renomeacoes(self):
        """Executa todas as renomeações de colunas"""
        if not self.renomeacoes_colunas:
            messagebox.showwarning("Aviso", "Nenhuma renomeação para executar!")
            return

        # Aplicar renomeações no controller
        try:
            # Aplicar renomeações de colunas
            for aba, coluna_antiga, coluna_nova in self.renomeacoes_colunas:
                resultado = self.controller.renomear_coluna(aba, coluna_antiga, coluna_nova)
                if not resultado['sucesso']:
                    messagebox.showerror("Erro", f"Erro ao renomear coluna '{coluna_antiga}' na aba '{aba}':\n{resultado['erro']}")
                    return

            # Salvar arquivo
            self.salvar_arquivo()

        except Exception as e:
            self.label_status.configure(text="❌ Erro no processamento!", text_color="red")
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")

    def salvar_arquivo(self):
        """Salva o arquivo com as renomeações aplicadas"""
        salvar_como_novo = self.radio_var_salvamento.get() == "novo"

        if salvar_como_novo:
            caminho = filedialog.asksaveasfilename(
                title="Salvar como novo arquivo",
                defaultextension=".xlsx",
                filetypes=[("Arquivos Excel", "*.xlsx")]
            )
        else:
            # Confirmar sobrescrita
            resposta = messagebox.askyesno(
                "Confirmar Sobrescrita",
                "⚠️  ATENÇÃO: Você está prestes a SOBRESCREVER o arquivo original!\n\n"
                "Esta ação NÃO PODE ser desfeita.\n"
                "Tem certeza que deseja continuar?"
            )
            if not resposta:
                return
            caminho = self.arquivo_selecionado

        if not caminho:
            self.label_status.configure(text="Operação cancelada pelo usuário", text_color="gray")
            return

        try:
            self.progress_bar.pack(fill="x", pady=(5, 0))
            self.progress_bar.set(0.5)
            
            self.label_status.configure(text="Salvando arquivo...", text_color="orange")

            # Salvar arquivo
            resultado = self.controller.salvar_arquivo(caminho, salvar_como_novo)

            self.progress_bar.set(1.0)

            if resultado['sucesso']:
                total_colunas = len(self.renomeacoes_colunas)
                
                self.label_status.configure(
                    text=f"✅ Concluído! {total_colunas} coluna(s) renomeada(s)",
                    text_color="green"
                )
                
                tipo_salvamento = "novo arquivo" if salvar_como_novo else "mesmo arquivo"
                messagebox.showinfo(
                    "Sucesso",
                    f"✅ Renomeações aplicadas com sucesso!\n\n"
                    f"📊 Estatísticas:\n"
                    f"• Colunas renomeadas: {total_colunas}\n"
                    f"• Salvo como: {tipo_salvamento}\n"
                    f"• Local: {caminho}\n\n"
                    f"📝 Todas as fórmulas e formatações foram preservadas."
                )
                
                # Limpar listas
                self.renomeacoes_colunas.clear()
                self.atualizar_lista_colunas()
                self.verificar_renomeacoes()
                
            else:
                self.label_status.configure(text="❌ Erro ao salvar arquivo!", text_color="red")
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{resultado['erro']}")
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro no salvamento!", text_color="red")
            messagebox.showerror("Erro", f"Erro inesperado ao salvar:\n{str(e)}")
        finally:
            self.after(3000, self.progress_bar.pack_forget)