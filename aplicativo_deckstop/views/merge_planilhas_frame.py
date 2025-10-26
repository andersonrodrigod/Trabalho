# views/merge_arquivos.py
import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from controllers.merge_planilhas_controller import MergePlanilhasController

class MergePlanilhas(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.controller = MergePlanilhasController()
        master.geometry("850x800+100+50")
        
        # Configuração de cores
        self.cor_primaria = "#238AD9"
        self.cor_sucesso = "#238AD9"
        self.cor_perigo = "#DC3545"
        self.cor_alerta = "#FFC107"
        self.cor_info = "#238AD9"

        # Variáveis
        self.arquivo_principal = None
        self.arquivo_merge = None
        self.info_compatibilidade = None

        # === LAYOUT PRINCIPAL ===
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

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
        self.btn_back.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # Label principal
        self.label = ctk.CTkLabel(
            self.grid_frame,
            text="🔄 Merge de Planilhas Excel",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.cor_primaria
        )
        self.label.grid(row=0, column=1, columnspan=2, pady=(0, 20))

        # === SELEÇÃO DE ARQUIVO PRINCIPAL ===
        self.frame_arquivo_principal = ctk.CTkFrame(self.grid_frame)
        self.frame_arquivo_principal.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        label_titulo_principal = ctk.CTkLabel(
            self.frame_arquivo_principal,
            text="📁 Arquivo Principal (Base - COM FÓRMULAS)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_principal.pack(anchor="w", pady=(10, 5), padx=10)

        subframe_principal = ctk.CTkFrame(self.frame_arquivo_principal, fg_color="transparent")
        subframe_principal.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_selecionar_principal = ctk.CTkButton(
            subframe_principal,
            text="Selecionar Principal",
            command=self.selecionar_arquivo_principal,
            width=140,
            height=32,
            fg_color=self.cor_primaria,
            hover_color="#1A6BA6"
        )
        self.btn_selecionar_principal.pack(side="left", padx=(0, 10))

        self.entry_arquivo_principal = ctk.CTkEntry(
            subframe_principal,
            width=400,
            height=32,
            placeholder_text="Arquivo base que contém fórmulas e será atualizado",
            state="readonly"
        )
        self.entry_arquivo_principal.pack(side="left", fill="x", expand=True)

        # === SELEÇÃO DE ARQUIVO MERGE ===
        self.frame_arquivo_merge = ctk.CTkFrame(self.grid_frame)
        self.frame_arquivo_merge.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        label_titulo_merge = ctk.CTkLabel(
            self.frame_arquivo_merge,
            text="📂 Arquivo de Merge (DADOS para atualização)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_merge.pack(anchor="w", pady=(10, 5), padx=10)

        subframe_merge = ctk.CTkFrame(self.frame_arquivo_merge, fg_color="transparent")
        subframe_merge.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_selecionar_merge = ctk.CTkButton(
            subframe_merge,
            text="Selecionar Merge",
            command=self.selecionar_arquivo_merge,
            width=140,
            height=32,
            fg_color=self.cor_info,
            hover_color="#1A6BA6"
        )
        self.btn_selecionar_merge.pack(side="left", padx=(0, 10))

        self.entry_arquivo_merge = ctk.CTkEntry(
            subframe_merge,
            width=400,
            height=32,
            placeholder_text="Arquivo com os novos dados para substituir",
            state="readonly"
        )
        self.entry_arquivo_merge.pack(side="left", fill="x", expand=True)

        # === RESUMO DA COMPATIBILIDADE ===
        self.frame_compatibilidade = ctk.CTkFrame(self.grid_frame)
        self.frame_compatibilidade.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        frame_titulo_compat = ctk.CTkFrame(self.frame_compatibilidade, fg_color="transparent")
        frame_titulo_compat.pack(fill="x", padx=10, pady=(5, 0))

        label_titulo_compat = ctk.CTkLabel(
            frame_titulo_compat,
            text="📊 Resumo da Compatibilidade",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_compat.pack(side="left")

        self.btn_verificar_compat = ctk.CTkButton(
            frame_titulo_compat,
            text="🔄 Verificar",
            command=self.verificar_compatibilidade,
            width=80,
            height=28,
            fg_color=self.cor_info,
            hover_color="#1A6BA6",
            state="disabled"
        )
        self.btn_verificar_compat.pack(side="right")

        # Frame para informações de compatibilidade
        self.frame_info_compat = ctk.CTkFrame(self.frame_compatibilidade, fg_color="transparent")
        self.frame_info_compat.pack(fill="x", padx=10, pady=5)

        self.label_info_compat = ctk.CTkLabel(
            self.frame_info_compat,
            text="Selecione ambos os arquivos para verificar compatibilidade",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=700
        )
        self.label_info_compat.pack()

        # === DETALHES DAS ABAS ===
        self.frame_detalhes_abas = ctk.CTkFrame(self.grid_frame)
        self.frame_detalhes_abas.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 10), padx=5)

        frame_titulo_detalhes = ctk.CTkFrame(self.frame_detalhes_abas, fg_color="transparent")
        frame_titulo_detalhes.pack(fill="x", padx=10, pady=(5, 0))

        label_titulo_detalhes = ctk.CTkLabel(
            frame_titulo_detalhes,
            text="📋 Detalhes das Abas (Fórmulas serão preservadas)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_titulo_detalhes.pack(side="left")

        # Frame para as duas colunas de abas
        frame_colunas_abas = ctk.CTkFrame(self.frame_detalhes_abas, fg_color="transparent")
        frame_colunas_abas.pack(fill="both", expand=True, padx=10, pady=5)

        # Coluna 1: Abas que serão substituídas
        frame_col1 = ctk.CTkFrame(frame_colunas_abas)
        frame_col1.pack(side="left", fill="both", expand=True, padx=(0, 5))

        label_col1 = ctk.CTkLabel(
            frame_col1,
            text="🔄 Abas que SERÃO Atualizadas",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.cor_primaria
        )
        label_col1.pack(pady=(5, 5))

        self.frame_abas_substituidas = ctk.CTkScrollableFrame(
            frame_col1,
            height=150,
            fg_color="#f0f0f0"
        )
        self.frame_abas_substituidas.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # Coluna 2: Abas que serão mantidas
        frame_col2 = ctk.CTkFrame(frame_colunas_abas)
        frame_col2.pack(side="right", fill="both", expand=True, padx=(5, 0))

        label_col2 = ctk.CTkLabel(
            frame_col2,
            text="💾 Abas que SERÃO Mantidas",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.cor_sucesso
        )
        label_col2.pack(pady=(5, 5))

        self.frame_abas_mantidas = ctk.CTkScrollableFrame(
            frame_col2,
            height=150,
            fg_color="#f0f8f0"
        )
        self.frame_abas_mantidas.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        # === BOTÃO EXECUTAR E STATUS ===
        self.btn_executar = ctk.CTkButton(
            self.grid_frame,
            text="🚀 Executar Merge (Preservar Fórmulas)",
            text_color="white",
            command=self.executar_merge,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.cor_sucesso,
            hover_color="#1A6BA6",
            state="disabled",
        )
        self.btn_executar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(20, 10), padx=5)

        # Frame para status
        self.frame_status = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
        self.frame_status.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        self.label_status = ctk.CTkLabel(
            self.frame_status,
            text="Selecione os arquivos principal e de merge para começar",
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
        self.frame_compatibilidade.grid_remove()
        self.frame_detalhes_abas.grid_remove()

    # MÉTODOS PRINCIPAIS (os mesmos do código anterior, mas com atualizações no processamento)

    def selecionar_arquivo_principal(self):
        """Seleciona o arquivo principal"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo Excel PRINCIPAL (com fórmulas)",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        
        if arquivo:
            self.arquivo_principal = arquivo
            self.entry_arquivo_principal.configure(state="normal")
            self.entry_arquivo_principal.delete(0, "end")
            self.entry_arquivo_principal.insert(0, arquivo.split("/")[-1])
            self.entry_arquivo_principal.configure(state="readonly")
            
            self.verificar_arquivos_selecionados()

    def selecionar_arquivo_merge(self):
        """Seleciona o arquivo de merge"""
        arquivo = filedialog.askopenfilename(
            title="Selecione o arquivo Excel de MERGE (com dados)",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        
        if arquivo:
            self.arquivo_merge = arquivo
            self.entry_arquivo_merge.configure(state="normal")
            self.entry_arquivo_merge.delete(0, "end")
            self.entry_arquivo_merge.insert(0, arquivo.split("/")[-1])
            self.entry_arquivo_merge.configure(state="readonly")
            
            self.verificar_arquivos_selecionados()

    def verificar_arquivos_selecionados(self):
        """Verifica se ambos os arquivos foram selecionados"""
        if self.arquivo_principal and self.arquivo_merge:
            self.frame_compatibilidade.grid()
            self.btn_verificar_compat.configure(state="normal")
            self.label_status.configure(
                text="Arquivos selecionados! Clique em 'Verificar' para analisar compatibilidade.",
                text_color="blue"
            )

    def verificar_compatibilidade(self):
        """Verifica a compatibilidade entre os arquivos"""
        if not self.arquivo_principal or not self.arquivo_merge:
            return

        try:
            self.progress_bar.pack(fill="x", pady=(5, 0))
            self.progress_bar.set(0.3)
            
            self.label_status.configure(text="Verificando compatibilidade entre arquivos...", text_color="orange")
            
            # Verificar compatibilidade
            self.info_compatibilidade = self.controller.verificar_compatibilidade_arquivos(
                self.arquivo_principal, self.arquivo_merge
            )
            
            self.progress_bar.set(1.0)
            self.mostrar_compatibilidade()
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro na verificação!", text_color="red")
            messagebox.showerror("Erro", f"Erro ao verificar compatibilidade:\n{str(e)}")
        finally:
            self.after(1000, self.progress_bar.pack_forget)

    def mostrar_compatibilidade(self):
        """Mostra os resultados da verificação de compatibilidade"""
        info = self.info_compatibilidade
        
        # Atualizar informações gerais
        texto_info = (
            f"✅ Arquivos compatíveis! "
            f"Principal: {info['total_abas_principal']} abas | "
            f"Merge: {info['total_abas_merge']} abas | "
            f"Abas em comum: {info['total_abas_comuns']}"
        )
        
        self.label_info_compat.configure(text=texto_info, text_color="green")
        
        # Mostrar frame de detalhes
        self.frame_detalhes_abas.grid()
        
        # Atualizar lista de abas
        self.atualizar_lista_abas()
        
        # Habilitar botão executar se houver abas em comum
        if info['total_abas_comuns'] > 0:
            self.btn_executar.configure(state="normal")
            self.label_status.configure(
                text=f"Pronto para merge! {info['total_abas_comuns']} aba(s) serão atualizadas preservando fórmulas.",
                text_color="green"
            )
        else:
            self.btn_executar.configure(state="disabled")
            self.label_status.configure(
                text="⚠️ Nenhuma aba em comum encontrada. O merge não atualizará nenhuma aba.",
                text_color="orange"
            )

    def atualizar_lista_abas(self):
        """Atualiza as listas de abas substituídas e mantidas com detalhes das colunas"""
        info = self.info_compatibilidade
        
        # Limpar listas atuais
        for widget in self.frame_abas_substituidas.winfo_children():
            widget.destroy()
        
        for widget in self.frame_abas_mantidas.winfo_children():
            widget.destroy()
        
        # Adicionar abas que serão substituídas com detalhes das colunas
        for aba in info['abas_comuns']:
            detalhes = info['detalhes_abas'][aba]
            frame_aba = ctk.CTkFrame(self.frame_abas_substituidas, fg_color="#E8F4FD")
            frame_aba.pack(fill="x", pady=2, padx=2)
            
            # Nome da aba
            label_aba = ctk.CTkLabel(
                frame_aba,
                text=f"🔄 {aba}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#1565C0",
                anchor="w"
            )
            label_aba.pack(side="top", padx=5, pady=(2, 0), fill="x")
            
            # Detalhes das colunas
            label_detalhes = ctk.CTkLabel(
                frame_aba,
                text=f"Colunas: {detalhes['total_colunas_comuns']}/{detalhes['total_colunas_principal']} em comum",
                font=ctk.CTkFont(size=9),
                text_color="#666666",
                anchor="w"
            )
            label_detalhes.pack(side="top", padx=5, pady=(0, 2), fill="x")
        
        # Adicionar abas que serão mantidas
        abas_mantidas = set(info['abas_principal']) - set(info['abas_comuns'])
        for aba in abas_mantidas:
            frame_aba = ctk.CTkFrame(self.frame_abas_mantidas, fg_color="#E8F5E8")
            frame_aba.pack(fill="x", pady=2, padx=2)
            
            label_aba = ctk.CTkLabel(
                frame_aba,
                text=f"💾 {aba}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#2E7D32",
                anchor="w"
            )
            label_aba.pack(side="left", padx=5, pady=2, fill="x", expand=True)

    def executar_merge(self):
        """Executa o processo de merge preservando fórmulas"""
        if not self.arquivo_principal or not self.arquivo_merge:
            messagebox.showwarning("Aviso", "Selecione ambos os arquivos!")
            return

        if not self.info_compatibilidade or self.info_compatibilidade['total_abas_comuns'] == 0:
            messagebox.showwarning("Aviso", "Nenhuma aba em comum para atualizar!")
            return

        self.progress_bar.pack(fill="x", pady=(5, 0))
        self.progress_bar.set(0.1)
        
        self.label_status.configure(text="Iniciando processo de merge (preservando fórmulas)...", text_color="orange")
        self.btn_executar.configure(state="disabled")

        try:
            self.progress_bar.set(0.3)
            
            # Executar merge
            workbook_resultado, abas_substituidas, abas_mantidas = self.controller.processar_merge(
                self.arquivo_principal, self.arquivo_merge, {}
            )

            self.progress_bar.set(0.8)

            if workbook_resultado:
                self.salvar_arquivo_processado(workbook_resultado, abas_substituidas, abas_mantidas)
            else:
                raise Exception("Nenhum dado processado")

        except Exception as e:
            self.label_status.configure(text="❌ Erro no processamento!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o merge:\n{str(e)}")
            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")

    def salvar_arquivo_processado(self, workbook, abas_substituidas, abas_mantidas):
        """Salva o arquivo resultante do merge"""
        caminho = filedialog.asksaveasfilename(
            title="Salvar arquivo com merge aplicado", 
            defaultextension=".xlsx", 
            filetypes=[("Arquivos Excel", "*.xlsx")]
        )

        if not caminho:
            self.label_status.configure(text="Operação cancelada pelo usuário", text_color="gray")
            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")
            return

        try:
            # Salvar o workbook processado
            self.controller.salvar_workbook(workbook, caminho)
            
            self.progress_bar.set(1.0)
            
            # Mensagem de resumo
            total_substituidas = len(abas_substituidas)
            total_mantidas = len(abas_mantidas)
            
            self.label_status.configure(
                text=f"✅ Merge concluído! {total_substituidas} aba(s) atualizada(s), {total_mantidas} aba(s) mantida(s)", 
                text_color="green"
            )
            
            messagebox.showinfo(
                "Merge Concluído", 
                f"✅ Arquivo gerado com sucesso!\n\n"
                f"📊 Estatísticas:\n"
                f"• Abas atualizadas: {total_substituidas}\n"
                f"• Abas mantidas: {total_mantidas}\n"
                f"• Total de abas: {total_substituidas + total_mantidas}\n\n"
                f"🔧 Funcionalidades preservadas:\n"
                f"• ✅ Fórmulas intactas em TODAS as abas\n"
                f"• ✅ Formatações originais\n"
                f"• ✅ Gráficos e objetos\n"
                f"• ✅ Configurações da planilha\n\n"
                f"💾 Local: {caminho}"
            )
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro ao salvar arquivo!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")
        
        finally:
            self.after(3000, self.progress_bar.pack_forget)
            self.btn_executar.configure(state="normal")