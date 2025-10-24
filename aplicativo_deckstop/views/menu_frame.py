import customtkinter as ctk
from views.detalhamento_frame import Detalhamento


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text="Menu Principal")
        self.label.pack(pady=(10,20))

        self.btn_unir_dados = ctk.CTkButton(self, text="Planilhas de Detalhamento", command=lambda: master.show_frame(Detalhamento), width=200)

        self.btn_unir_dados.pack(pady=(0, 5))


        self.btn_editar_dados = ctk.CTkButton(self, text="Editar Dados", width=200)

        self.btn_editar_dados.pack(pady=(0,5))