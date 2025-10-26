import customtkinter as ctk
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
from controllers.concatenar_controller import ConcatenarController

class Concatenar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        master.geometry("500x600")
        
        self.controller = ConcatenarController()
        self.arquivos_selecionados = []
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Label principal
        self.label = ctk.CTkLabel(
            self, 
            text="📊 Concatenar Planilhas", 
            font=ctk.CTkFont(size=26, weight="bold"), 
            text_color="#238AD9"
        )
        self.label.pack(pady=(50, 5))

        # Botão Voltar no canto superior esquerdo
        self.btnback = ctk.CTkButton(
            self,
            text="←",
            command=lambda: master.show_frame(master.menu_frame),
            width=20,
            height=35,
            fg_color="gray",
            hover_color="#5A6268"
        )

        self.btnback.place(x=20, y=20)
        
        # Frame para os botões de seleção
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=(20, 5), padx=40, fill="x")
        
        # Botão para selecionar arquivos
        self.btn_selecionar = ctk.CTkButton(
            self.frame_botoes,
            text="📁 Selecionar Arquivos",
            command=self.selecionar_arquivos,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=35,
            fg_color="#238AD9",
            hover_color="#1A6BA6"
        )
        self.btn_selecionar.pack(fill="x")
        
        # Label para mostrar quantidade de arquivos selecionados
        self.label_contador = ctk.CTkLabel(
            self.frame_botoes,
            text="Nenhum arquivo selecionado",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.label_contador.pack(pady=5)
        
        # Frame para a lista de arquivos
        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(pady=10, padx=40, fill="both")
        
        # Label da lista
        self.label_lista = ctk.CTkLabel(
            self.frame_lista,
            text="Arquivos selecionados:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_lista.pack(anchor="w", pady=(10, 5))
        
        # Scrollable frame para mostrar os arquivos
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.frame_lista,
            height=150
        )
        self.scroll_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Botão executar
        self.btn_executar = ctk.CTkButton(
            self,
            text="▶️ Executar Concatenção",
            command=self.executar_concatenacao,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#238AD9",
            hover_color="#1A6BA6",
            state="disabled"  # Inicialmente desabilitado
        )
        self.btn_executar.pack(pady=5, padx=40, fill="x")
        
        # Frame para status/progresso
        self.frame_status = ctk.CTkFrame(self)
        self.frame_status.pack(pady=(5, 10), padx=40, fill="x")
        
        self.label_status = ctk.CTkLabel(
            self.frame_status,
            text="Pronto para executar",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.label_status.pack(pady=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.frame_status)
        self.progress_bar.pack(pady=5, fill="x")
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()  # Escondida inicialmente

    def selecionar_arquivos(self):
        """Seleciona múltiplos arquivos"""
        arquivos = filedialog.askopenfilenames(
            title="Selecione as planilhas",
            filetypes=[
                ("Planilhas", "*.xlsx *.xls *.csv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            self.atualizar_lista_arquivos()
            self.atualizar_contador()
            self.btn_executar.configure(state="normal")
            self.label_status.configure(text=f"{len(arquivos)} arquivos selecionados", text_color="blue")

    def atualizar_lista_arquivos(self):
        """Atualiza a lista visual de arquivos"""
        # Limpa a lista atual
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Adiciona cada arquivo na lista
        for i, arquivo in enumerate(self.arquivos_selecionados):
            nome_arquivo = arquivo.split("/")[-1]  # Pega apenas o nome do arquivo
            
            frame_arquivo = ctk.CTkFrame(self.scroll_frame)
            frame_arquivo.pack(fill="x", pady=2)
            
            label_arquivo = ctk.CTkLabel(
                frame_arquivo,
                text=f"{i+1}. {nome_arquivo}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            label_arquivo.pack(side="left", padx=10, pady=5, fill="x", expand=True)
            
            # Botão para remover arquivo individual
            btn_remover = ctk.CTkButton(
                frame_arquivo,
                text="✕",
                width=30,
                height=30,
                fg_color="red",
                hover_color="darkred",
                command=lambda a=arquivo: self.remover_arquivo(a)
            )
            btn_remover.pack(side="right", padx=5)

    def atualizar_contador(self):
        """Atualiza o contador de arquivos"""
        quantidade = len(self.arquivos_selecionados)
        if quantidade == 0:
            texto = "Nenhum arquivo selecionado"
            self.btn_executar.configure(state="disabled")
        elif quantidade == 1:
            texto = "1 arquivo selecionado"
        else:
            texto = f"{quantidade} arquivos selecionados"
        
        self.label_contador.configure(text=texto)

    def remover_arquivo(self, arquivo):
        """Remove um arquivo específico da lista"""
        if arquivo in self.arquivos_selecionados:
            self.arquivos_selecionados.remove(arquivo)
            self.atualizar_lista_arquivos()
            self.atualizar_contador()
            
            if not self.arquivos_selecionados:
                self.btn_executar.configure(state="disabled")
                self.label_status.configure(text="Pronto para executar", text_color="green")

    def executar_concatenacao(self):
        """Executa a concatenação dos arquivos"""
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
        
        # Mostra a progress bar
        self.progress_bar.pack(pady=5, fill="x")
        self.progress_bar.set(0)
        
        # Atualiza status
        self.label_status.configure(text="Processando...", text_color="orange")
        self.btn_executar.configure(state="disabled")
        self.btn_selecionar.configure(state="disabled")
        
        try:
            # Simula processamento (substitua pela lógica real do controller)
            self.atualizar_progresso()
            
            # Chama o controller para processar os arquivos
            resultado = self.controller.processar_arquivos(self.arquivos_selecionados)
            
            if resultado:
                self.salvar_arquivo_concatenado(resultado)
            else:
                raise Exception("Erro no processamento")
                
        except Exception as e:
            self.label_status.configure(text="Erro na concatenação! ❌", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        
        finally:
            # Reabilita os botões
            self.btn_selecionar.configure(state="normal")
            # Esconde a progress bar após 2 segundos
            self.after(2000, self.progress_bar.pack_forget)
            # Esconde a progress bar após 2 segundos
            self.after(2000, self.progress_bar.pack_forget)

    def atualizar_progresso(self):
        """Atualiza a barra de progresso (simulação)"""
        # Esta é uma simulação - substitua pela lógica real de progresso
        def simular_progresso():
            for i in range(101):
                self.progress_bar.set(i/100)
                self.update_idletasks()
                self.after(20)  # Pequeno delay para animação
        
        # Inicia em uma thread separada para não travar a interface
        import threading
        thread = threading.Thread(target=simular_progresso)
        thread.daemon = True
        thread.start()

    def salvar_arquivo_concatenado(self, resultado):
        caminho_salvar = filedialog.asksaveasfilename(
            title="Salvar planilha concatenada",
            defaultextension=".xlsx",
            filetypes=[("Planilhas Excel", "*.xlsx")]
        )

        if not caminho_salvar:
            messagebox.showinfo("Cancelado", "Operação de salvamento cancelada.")
            self.label_status.configure(text="Concatenação concluída (não salva)", text_color="orange")
            return

        try:
            with pd.ExcelWriter(caminho_salvar, engine="openpyxl") as writer:
                for aba, df in resultado.items():
                    df.to_excel(writer, sheet_name=aba, index=False)

            self.label_status.configure(text="Concatenação concluída e salva! ✅", text_color="green")
            self.progress_bar.set(1)
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso:\n{caminho_salvar}")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar o arquivo:\n{str(e)}")
            self.label_status.configure(text="Erro ao salvar arquivo ❌", text_color="red")
