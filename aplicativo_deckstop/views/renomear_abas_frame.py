# views/renomear_abas.py
import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from controllers.renomear_abas_controller import RenomearAbasController

class RenomearAbas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.controller = RenomearAbasController()
        master.geometry("850x680+100+50")  # Reduzindo a altura
        
        # Configuração de cores
        self.cor_primaria = "#FF6B35"
        self.cor_sucesso = "#28A745"
        self.cor_perigo = "#DC3545"
        self.cor_alerta = "#FFC107"
        self.cor_info = "#17A2B8"

        # Variáveis
        self.arquivo_selecionado = None
        self.renomeacoes_abas = []  # Lista de tuplas (antigo, novo)

        # === LAYOUT PRINCIPAL ===
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Botão Voltar
        self.btn_back = ctk.CTkButton(
            self.grid_frame, 
            text="←", 
            command=lambda: master.show_frame(master.menu_frame), 
            width=20,
            height=35,
            fg_color="gray",
            hover_color="#5A6268"
        )
        self.btn_back.grid(row=0, column=0, sticky="w", pady=(0, 15))

        # Label principal
        self.label = ctk.CTkLabel(
            self.grid_frame,
            text="📄 Renomear Abas",
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
            hover_color="#E55A2B"
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

        # === RENOMEAR ABAS - LAYOUT EM COLUNAS ===
        self.frame_abas = ctk.CTkFrame(self.grid_frame)
        self.frame_abas.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 15), padx=5)
        
        # Configurar pesos para expandir
        self.grid_frame.rowconfigure(2, weight=1)

        # Frame principal com duas colunas
        frame_colunas_abas = ctk.CTkFrame(self.frame_abas, fg_color="transparent")
        frame_colunas_abas.pack(fill="both", expand=True, padx=10, pady=10)

        # === COLUNA 1: CONTROLES DE ENTRADA ===
        frame_coluna_controles = ctk.CTkFrame(frame_colunas_abas)
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
            text="Aba para renomear:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_aba.pack(anchor="w", pady=(0, 5))

        self.combobox_abas = ctk.CTkComboBox(
            frame_coluna_controles,
            values=[],
            state="readonly",
            width=250,
            height=35
        )
        self.combobox_abas.pack(anchor="w", pady=(0, 15), fill="x")

        # Input para novo nome da aba
        self.label_nova_aba = ctk.CTkLabel(
            frame_coluna_controles,
            text="Novo nome da aba:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_nova_aba.pack(anchor="w", pady=(0, 5))

        self.entry_nova_aba = ctk.CTkEntry(
            frame_coluna_controles,
            placeholder_text="Digite o novo nome...",
            width=250,
            height=35
        )
        self.entry_nova_aba.pack(anchor="w", pady=(0, 20), fill="x")

        # Botão para adicionar renomeação de aba
        self.btn_adicionar_aba = ctk.CTkButton(
            frame_coluna_controles,
            text="➕ Adicionar Renomeação",
            command=self.adicionar_renomeacao_aba,
            width=200,
            height=38,
            fg_color=self.cor_sucesso,
            hover_color="#218838",
            state="disabled",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_adicionar_aba.pack(anchor="w", pady=(0, 15))

        # === COLUNA 2: LISTA DE ALTERAÇÕES ===
        frame_coluna_lista = ctk.CTkFrame(frame_colunas_abas)
        frame_coluna_lista.pack(side="right", fill="both", expand=True, padx=(10, 0))

        label_titulo_lista = ctk.CTkLabel(
            frame_coluna_lista,
            text="📋 Alterações Pendentes",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_lista.pack(anchor="w", pady=(0, 10))

        self.frame_lista_abas = ctk.CTkScrollableFrame(
            frame_coluna_lista,
            height=180,  # Altura fixa para controlar o tamanho
            fg_color="#f8f9fa"
        )
        self.frame_lista_abas.pack(fill="both", expand=True, pady=(0, 10))

        # Label quando não há renomeações
        self.label_lista_vazia = ctk.CTkLabel(
            self.frame_lista_abas,
            text="Nenhuma renomeação adicionada\n\nUse o painel ao lado para adicionar renomeações de abas.",
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
            text="🚀 Executar Renomeações de Abas",
            command=self.executar_renomeacoes,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.cor_primaria,
            hover_color="#E55A2B",
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
        self.frame_abas.grid_remove()
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
                # Atualizar combobox
                self.combobox_abas.configure(values=resultado['abas'])
                
                if resultado['abas']:
                    self.combobox_abas.set(resultado['abas'][0])
                
                # Mostrar frames
                self.frame_abas.grid()
                self.frame_opcoes_salvamento.grid()
                
                # Habilitar controles
                self.btn_adicionar_aba.configure(state="normal")
                
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

    def adicionar_renomeacao_aba(self):
        """Adiciona uma renomeação de aba à lista"""
        aba_antiga = self.combobox_abas.get()
        aba_nova = self.entry_nova_aba.get().strip()

        if not aba_nova:
            messagebox.showwarning("Aviso", "Digite o novo nome da aba!")
            return

        if aba_antiga == aba_nova:
            messagebox.showwarning("Aviso", "O novo nome deve ser diferente do nome atual!")
            return

        # Verificar se já existe esta renomeação
        for antiga, nova in self.renomeacoes_abas:
            if antiga == aba_antiga:
                messagebox.showwarning("Aviso", f"A aba '{aba_antiga}' já tem uma renomeação pendente!")
                return

        # Adicionar à lista
        self.renomeacoes_abas.append((aba_antiga, aba_nova))
        self.atualizar_lista_abas()

        # Limpar campo
        self.entry_nova_aba.delete(0, 'end')

        self.label_status.configure(
            text=f"Renomeação de aba adicionada: {aba_antiga} → {aba_nova}",
            text_color="blue"
        )

        # Habilitar botão executar se houver renomeações
        self.verificar_renomeacoes()

    def atualizar_lista_abas(self):
        """Atualiza a lista visual de renomeações de abas"""
        # Esconder label de lista vazia se houver itens
        if self.renomeacoes_abas:
            self.label_lista_vazia.pack_forget()
        else:
            self.label_lista_vazia.pack(expand=True, pady=20)
            return

        # Limpar widgets antigos (exceto o label de lista vazia)
        for widget in self.frame_lista_abas.winfo_children():
            if widget != self.label_lista_vazia:
                widget.destroy()

        for i, (antiga, nova) in enumerate(self.renomeacoes_abas):
            frame_renomeacao = ctk.CTkFrame(self.frame_lista_abas, fg_color="#E8F4FD", height=35)
            frame_renomeacao.pack(fill="x", pady=2, padx=2)

            label_renomeacao = ctk.CTkLabel(
                frame_renomeacao,
                text=f"📄 {antiga} → {nova}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#1565C0",
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
                command=lambda idx=i: self.remover_renomeacao_aba(idx)
            )
            btn_remover.pack(side="right", padx=5, pady=5)

    def remover_renomeacao_aba(self, index):
        """Remove uma renomeação de aba da lista"""
        if 0 <= index < len(self.renomeacoes_abas):
            antiga, nova = self.renomeacoes_abas.pop(index)
            self.atualizar_lista_abas()
            self.label_status.configure(
                text=f"Renomeação de aba removida: {antiga} → {nova}",
                text_color="orange"
            )
            self.verificar_renomeacoes()

    def verificar_renomeacoes(self):
        """Verifica se há renomeações para habilitar o botão executar"""
        if self.renomeacoes_abas:
            total_abas = len(self.renomeacoes_abas)
            self.btn_executar.configure(state="normal")
            self.label_status.configure(
                text=f"Pronto! {total_abas} renomeação(ões) de aba(s) pendente(s)",
                text_color="green"
            )
        else:
            self.btn_executar.configure(state="disabled")
            self.label_status.configure(
                text="Adicione renomeações de abas para continuar",
                text_color="gray"
            )

    def executar_renomeacoes(self):
        """Executa todas as renomeações de abas"""
        if not self.renomeacoes_abas:
            messagebox.showwarning("Aviso", "Nenhuma renomeação para executar!")
            return

        # Aplicar renomeações no controller
        try:
            # Aplicar renomeações de abas
            for aba_antiga, aba_nova in self.renomeacoes_abas:
                resultado = self.controller.renomear_aba(aba_antiga, aba_nova)
                if not resultado['sucesso']:
                    messagebox.showerror("Erro", f"Erro ao renomear aba '{aba_antiga}':\n{resultado['erro']}")
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
                total_abas = len(self.renomeacoes_abas)
                
                self.label_status.configure(
                    text=f"✅ Concluído! {total_abas} aba(s) renomeada(s)",
                    text_color="green"
                )
                
                tipo_salvamento = "novo arquivo" if salvar_como_novo else "mesmo arquivo"
                messagebox.showinfo(
                    "Sucesso",
                    f"✅ Renomeações aplicadas com sucesso!\n\n"
                    f"📊 Estatísticas:\n"
                    f"• Abas renomeadas: {total_abas}\n"
                    f"• Salvo como: {tipo_salvamento}\n"
                    f"• Local: {caminho}\n\n"
                    f"📝 Todas as fórmulas e formatações foram preservadas."
                )
                
                # Limpar listas
                self.renomeacoes_abas.clear()
                self.atualizar_lista_abas()
                self.verificar_renomeacoes()
                
            else:
                self.label_status.configure(text="❌ Erro ao salvar arquivo!", text_color="red")
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{resultado['erro']}")
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro no salvamento!", text_color="red")
            messagebox.showerror("Erro", f"Erro inesperado ao salvar:\n{str(e)}")
        finally:
            self.after(3000, self.progress_bar.pack_forget)