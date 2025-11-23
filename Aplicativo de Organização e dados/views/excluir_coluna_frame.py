import customtkinter as ctk
import pandas as pd
from controllers.excluir_colunas_controller import ExcluirColunaController
from tkinter import filedialog, messagebox

class ExcluirColunaFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        master.geometry("1000x650")

        self.arquivo_selecionado = None
        self.colunas_disponiveis = []
        self.colunas_selecionadas = []

        # === LAYOUT PRINCIPAL COMPACTO ===
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Configurar pesos das colunas para centralização
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)
        self.grid_frame.columnconfigure(2, weight=1)

        # === LINHA 0: CABEÇALHO COM BOTÃO VOLTAR E TÍTULO ===
        # Botão Voltar - coluna 0
        self.btn_voltar = ctk.CTkButton(
            self.grid_frame, 
            text="← Voltar", 
            command=lambda: master.show_frame(master.menu_frame), 
            width=80,
            height=30,
            hover_color="#1C148F"
        )
        self.btn_voltar.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Título centralizado - coluna 1
        self.label = ctk.CTkLabel(
            self.grid_frame, 
            text="Excluir Coluna", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label.grid(row=0, column=1, pady=(0, 20))

        # Coluna 2 vazia para balancear o layout
        # Pode adicionar outro elemento aqui se quiser

        # === SELEÇÃO DE ARQUIVO ===
        self.frame_arquivo = ctk.CTkFrame(self.grid_frame)
        self.frame_arquivo.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        label_titulo_arquivo = ctk.CTkLabel(
            self.frame_arquivo,
            text="📁 Selecionar Arquivo Excel",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_arquivo.pack(pady=(10, 5))

        subframe_arquivo = ctk.CTkFrame(self.frame_arquivo, fg_color="transparent")
        subframe_arquivo.pack(fill="x", padx=10, pady=(0, 10))

        # Container para centralizar os elementos de seleção de arquivo
        container_selecao = ctk.CTkFrame(subframe_arquivo, fg_color="transparent")
        container_selecao.pack(expand=True)

        self.btn_selecionar_arquivo = ctk.CTkButton(
            container_selecao,
            text="Procurar",
            command=self.selecionar_arquivo,
            width=100,
            height=32,
            hover_color="#218838"
        )
        self.btn_selecionar_arquivo.pack(side="left", padx=(0, 10))

        self.entry_arquivo = ctk.CTkEntry(
            container_selecao,
            width=400,
            height=32,
            placeholder_text="Nenhum arquivo selecionado",
            state="readonly",
            justify="center"
        )
        self.entry_arquivo.pack(side="left", fill="x", expand=True)

        # Adicione também um fg_color ao botão para melhor visualização
        self.btn_voltar.configure(fg_color="#2B2B2B")  # Ou outra cor que combine com seu tema
        
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