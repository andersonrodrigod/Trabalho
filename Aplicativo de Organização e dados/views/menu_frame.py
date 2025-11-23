import customtkinter as ctk
from views.excluir_coluna_frame import ExcluirColunaFrame


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        master.geometry("350x300")

        self.label = ctk.CTkLabel(self, text="Bem Vindo ao Data Joiner!", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=(10, 20))

        self.excluir_colunas = ctk.CTkButton(self, text="Excluir Colunas", command=lambda: master.show_frame(ExcluirColunaFrame))
        self.excluir_colunas.pack(pady=(0, 5))
