import customtkinter as ctk
from tkinter import filedialog



class Detalhamento(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
 
        # Label principal
        self.label = ctk.CTkLabel(
            self,
            text="📊 Unir Dados de Detalhamento",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#238AD9"
        )
        self.label.pack(pady=(40,20))

        # Botão Voltar no canto superior esquerdo
        self.btn_back = ctk.CTkButton(self, text="<", command=lambda: master.show_frame(master.menu_frame), width=20)

        self.btn_back.place(x=10, y=10)

        # Variáveis para armazenar caminhos
        self.path_eletivo = ctk.StringVar()
        self.path_internacao = ctk.StringVar()

         # --- Frame para Planilha Eletivo ---
        frame_eletivo = ctk.CTkFrame(self)
        frame_eletivo.pack(pady=(5, 5))

        self.btn_eletivo = ctk.CTkButton(frame_eletivo, text="Eletivo", command=lambda: self.selecionar_eletivo())
        self.btn_eletivo.grid(row=0, column=0, padx=(0,10), pady=10)

        self.entry_eletivo = ctk.CTkEntry(frame_eletivo, textvariable=self.path_eletivo, width=300)
        self.entry_eletivo.grid(row=0, column=1, pady=10)
        
        # --- Frame para Planilha Internação ---
        frame_internacao = ctk.CTkFrame(self)
        frame_internacao.pack(pady=(5, 5))

        self.btn_internacao = ctk.CTkButton(frame_internacao, text="Internação", command=lambda: self.selecionar_internacao())
        self.btn_internacao.grid(row=0, column=0, padx=(0,10), pady=10)

        self.entry_internacao = ctk.CTkEntry(frame_internacao, textvariable=self.path_internacao, width=300)
        self.entry_internacao.grid(row=0, column=1, pady=10)

        # --- Botão Executar --- 
        self.btn_executar = ctk.CTkButton(self, text="Executar", state="disabled", command=lambda: self.execute())
        self.btn_executar.pack(pady=(20,10))

        self.file_eletivo = None
        self.file_internacao = None

        self.file_eletivo = [] 
        self.file_internacao = []

    def selecionar_eletivo(self):
        files = filedialog.askopenfilenames(
            title="Selecione a planilha Eletivo",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if files:
            # Adiciona os novos arquivos à lista existente
            self.file_eletivo.extend(files)  
            # Exibe todos os nomes no Entry
            self.path_eletivo.set(f"{len(self.file_eletivo)} arquivo(s): " + 
                                ", ".join([f.split("/")[-1] for f in self.file_eletivo]))
        self.verificar_pronto()

    def selecionar_internacao(self):
        files = filedialog.askopenfilenames(
            title="Selecione a planilha Internação",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )
        if files:
            self.file_internacao.extend(files)  # adiciona à lista existente
            self.path_internacao.set(f"{len(self.file_internacao)} arquivo(s): " + 
                                    ", ".join([f.split("/")[-1] for f in self.file_internacao]))
        self.verificar_pronto()


    def verificar_pronto(self):
        total = 0
        if self.file_eletivo: total += len(self.file_eletivo)
        if self.file_internacao: total += len(self.file_internacao)

        if total >=2:
            self.btn_executar.configure(state="normal")
        else:
            self.btn_executar.configure(state="disabled")

    def execute(self):
        print("Executar clicado!")
        print("Eletivo:", self.path_eletivo.get())
        print("Internação:", self.path_internacao.get())       














