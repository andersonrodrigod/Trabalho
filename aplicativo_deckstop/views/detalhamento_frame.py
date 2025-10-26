import customtkinter as ctk
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
from controllers.detalhamento_controller import DetalhamentoController

class Detalhamento(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        master.geometry("700x570")

        self.controller = DetalhamentoController()
        
        # Configuração de cores
        self.cor_primaria = "#238AD9"
        self.cor_sucesso = "#28A745"
        self.cor_perigo = "#DC3545"

        # Label principal
        self.label = ctk.CTkLabel(
            self,
            text="📊 Unir Dados de Detalhamento",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=self.cor_primaria
        )
        self.label.pack(pady=(50, 30))

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

        # Frame principal para organizar o conteúdo
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(pady=(10,10), padx=40, fill="both")

        # Variáveis para armazenar caminhos
        self.path_eletivo = ctk.StringVar()
        self.path_internacao = ctk.StringVar()

        # --- Frame para Planilha Eletivo ---
        frame_eletivo = ctk.CTkFrame(self.frame_principal)
        frame_eletivo.pack(fill="x", pady=(10, 15), padx=20)
        
        # Título do frame eletivo
        label_titulo_eletivo = ctk.CTkLabel(frame_eletivo, text="Planilha Eletivo", font=ctk.CTkFont(size=20, weight="bold"))
        label_titulo_eletivo.pack(anchor="w", pady=(10, 5), padx=(10, 0))

        # Subframe para botão e entry
        subframe_eletivo = ctk.CTkFrame(frame_eletivo)
        subframe_eletivo.pack(fill="x", pady=(0, 10), padx=(10, 10))

        self.btn_eletivo = ctk.CTkButton(
            subframe_eletivo,
            text="📂 Selecionar Arquivo",
            command=self.selecionar_eletivo,
            width=140,
            height=35,
            fg_color=self.cor_primaria,
            hover_color="#1A6BA6"
        )

        self.btn_eletivo.pack(side="left", padx=(0,10))

        self.entry_eletivo = ctk.CTkEntry(
            subframe_eletivo,
            textvariable=self.path_eletivo,
            width=400,
            height=35,
            placeholder_text="Nenhum arquivo selecionado"
        )

        self.entry_eletivo.pack(side="left", fill="x", expand=True)

         # --- Frame para Planilha Internação ---
        frame_internacao = ctk.CTkFrame(self.frame_principal)
        frame_internacao.pack(fill="x", pady=(10,15), padx=20)

        # Título do frame internação
        label_titulo_internacao = ctk.CTkLabel(
            frame_internacao,
            text="Planilha Internação",
            font=ctk.CTkFont(size=20, weight="bold")
        )

        label_titulo_internacao.pack(anchor="w", pady=(10, 5), padx=(10, 0))

        # Subframe para botão e entry
        subframe_internacao = ctk.CTkFrame(frame_internacao)
        subframe_internacao.pack(fill="x", pady=(0, 10), padx=(10, 10))
        
        self.btn_internacao = ctk.CTkButton(
            subframe_internacao,
            text="📂 Selecionar Arquivo",
            command=self.selecionar_internacao,
            width=140,
            height=35,
            fg_color=self.cor_primaria,
            hover_color="#1A6BA6"
        )

        self.btn_internacao.pack(side="left", padx=(0, 10))
        
        self.entry_internacao = ctk.CTkEntry(
            subframe_internacao,
            textvariable=self.path_internacao,
            width=400,
            height=35,
            placeholder_text="Nenhum arquivo selecionado"
        )

        self.entry_internacao.pack(side="left", fill="x", expand=True)


        # Frame para informações
        frame_info = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_info.pack(fill="x", pady=(10, 20), padx=20)

        self.label_info = ctk.CTkLabel(
            frame_info,
            text="💡 Selecione pelo menos 2 arquivos (eletivo e/ou internação) para habilitar a execução",
            font=ctk.CTkFont(size=14),
            text_color="gray",
            wraplength=500
        )

        self.label_info.pack(pady=5)

        # Contador de arquivos
        self.label_contador = ctk.CTkLabel(
            frame_info,
            text="Arquivos selecionados: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.cor_primaria
        )

        self.label_contador.pack(pady=5)

        self.btn_executar = ctk.CTkButton(
            self,
            text="🚀 Executar Unificação", 
            state="disabled", 
            command=lambda: self.execute(),
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.cor_primaria,
            hover_color="#218838"
        )

        self.btn_executar.pack(pady=5, padx=40, fill="x")

        #Frame para status
        self.frame_status = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_status.pack(fill="x", pady=(0,10), padx=20)

        self.label_status = ctk.CTkLabel(
            self.frame_status,
            text="Pronto para selecionar arquivos",
            font=ctk.CTkFont(size=14),
            text_color="green"
        )

        self.label_status.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.frame_status)
        self.progress_bar.set(0)

        self.file_eletivo = [] 
        self.file_internacao = []


    def selecionar_eletivo(self):
        files = filedialog.askopenfilenames(
            title="Selecione as planilhas Eletivo",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if files:
            # Adiciona os novos arquivos à lista existente
            self.file_eletivo.extend(files)  
            # Exibe todos os nomes no Entry
            self.path_eletivo.set(f"{len(self.file_eletivo)} arquivo(s): " + 
                                ", ".join([f.split("/")[-1] for f in self.file_eletivo]))
            self.atualizar_interface()
        self.verificar_pronto()

    def selecionar_internacao(self):
        files = filedialog.askopenfilenames(
            title="Selecione as planilhas Internação",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )

        if files:
            self.file_internacao.extend(files)  # adiciona à lista existente
            self.path_internacao.set(f"{len(self.file_internacao)} arquivo(s): " + 
                                    ", ".join([f.split("/")[-1] for f in self.file_internacao])
            )
            self.atualizar_interface()
        self.verificar_pronto()

    def atualizar_interface(self):
        #Atualiza contador e status na interface
        total_arquivos = len(self.file_eletivo) + len(self.file_internacao)
        self.label_contador.configure(text=f"Arquivos selcionados: {total_arquivos}")

        if total_arquivos > 0:
            self.label_status.configure(
                text=f"{total_arquivos} arquivo(s) selecionado(s) - Pronto para executar",
                text_color="blue"
            )
        else:
            self.label_status.configure(text="Pronto para selecionar arquivos", text_color="green")

    def verificar_pronto(self):
        total = len(self.file_eletivo) + len(self.file_internacao)

        if total >= 2:
            self.btn_executar.configure(state="normal")
            self.label_status.configure(text="✅ Pronto para executar!", text_color="green")
        else:
            self.btn_executar.configure(state="disabled")
            if total > 0:
                self.label_status.configure(text=f"Selecione mais {2 - total} arquivo(s) para habilitar a execução", text_color="orange")

    def execute(self):
        
        # Mostrar barra de progresso
        self.progress_bar.pack(fill="x", pady=(5,0))
        self.progress_bar.set(0.1)

        # Atualizar status
        self.label_status.configure(text="Processando arquivos...", text_color="orange")

        self.btn_executar.configure(state="disabled")

        try:

            lista_dfs = []

            # 2️⃣ Processa arquivos de Eletivo
            self.progress_bar.set(0.3)
            self.update()
            for arquivo in self.file_eletivo:
                dfs_ajustados = self.controller.ajustar_abas(arquivo, tipo="eletivo")
                lista_dfs.append(dfs_ajustados)
                
            # 3️⃣ Processa arquivos de Internação
            self.progress_bar.set(0.6)
            for arquivo in self.file_internacao:
                dfs_ajustados = self.controller.ajustar_abas(arquivo, tipo="internacao")
                lista_dfs.append(dfs_ajustados)

            # 4️⃣ Junta todas as abas iguais usando a função do Controller
            self.progress_bar.set(0.8)
            dfs_juntos = self.controller.juntar_abas(lista_dfs)

            # 5️⃣ Exibe as abas concatenadas no console (opcional)
            print("\n✅ Abas concatenadas:")
            for aba in dfs_juntos.keys():
                print(f" - {aba}")  

            # 6️⃣ Salva o arquivo consolidado
            self.progress_bar.set(1.0)
            self.salvar_arquivo(dfs_juntos)

        except Exception as e:
            self.label_status.configure(text="❌ Erro no processamento!", text_color="red")

            messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")

            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")

    def salvar_arquivo(self, dfs_juntos):
        caminho = filedialog.asksaveasfilename(
            title="Salvar arquivo consolidado", 
            defaultextension=".xlsx", 
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )

        if not caminho:
            self.label_status.configure(text="Operação cancelada pelo usuário", text_color="gray")
            self.progress_bar.pack_forget()
            self.btn_executar.configure(state="normal")
            return
        
        self.progress_bar.pack(fill="x", pady=(5,0))
        
        

        try:
            self.progress_bar.set(0.1)
            self.update()
            with pd.ExcelWriter(caminho, engine="openpyxl") as writer:
                for aba, df in dfs_juntos.items():
                    df.to_excel(writer, sheet_name=aba, index=False)
        
            self.progress_bar.set(0.5)
            
            self.label_status.configure(text="✅ Arquivo salvo com sucesso!", text_color="green")

            self.progress_bar.set(1.0)
            messagebox.showinfo("Concluído", "Arquivo salvo com sucesso!")
            
        except Exception as e:
            self.label_status.configure(text="❌ Erro ao salvar arquivo!", text_color="red")
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o arquivo:\n{str(e)}")
        
        finally:
            # Esconder barra de progresso após 2 segundos
            self.after(2000, self.progress_bar.pack_forget)
            self.btn_executar.configure(state="normal")

        print(f"✅ Arquivo salvo em: {caminho}")



