import customtkinter as ctk
from views.detalhamento_frame import Detalhamento
from views.concaternar_frame import Concatenar
from views.excluir_linhas_frame import ExcluirLinhas
from views.substituir_valores_frame import SubstituirValores
from views.merge_planilhas_frame import MergePlanilhas
from views.renomear_abas_frame import RenomearAbas
from views.renomear_colunas_frame import RenomearColunas


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        master.geometry("350x300")

        self.label = ctk.CTkLabel(self, text="Menu Principal")
        self.label.pack(pady=(10,20))

        self.btn_concatenar_planilhas = ctk.CTkButton(self, text="Concatenar Planilhas", command=lambda: master.show_frame(Concatenar), width=200)

        self.btn_concatenar_planilhas.pack(pady=(0,5))

        self.btn_unir_dados = ctk.CTkButton(self, text="Planilhas de Detalhamento", command=lambda: master.show_frame(Detalhamento), width=200)

        self.btn_unir_dados.pack(pady=(0, 5))


        self.btn_substituir_valores = ctk.CTkButton(self, text="Substituir Valores", width=200, command=lambda: master.show_frame(SubstituirValores))

        self.btn_substituir_valores.pack(pady=(0,5))

        self.btn_excluir_linhas = ctk.CTkButton(self, text="Excluir Linhas", width=200, command=lambda: master.show_frame(ExcluirLinhas))

        self.btn_fundir_planilhas = ctk.CTkButton(self, text="Fundir Planilhas", width=200, command=lambda: master.show_frame(MergePlanilhas))

        self.btn_excluir_linhas.pack(pady=(0,5))

        self.btn_renomear_abas = ctk.CTkButton(self, text="Renomear Abas", width=200, command=lambda: master.show_frame(RenomearAbas))

        self.btn_renomear_abas.pack(pady=(0,5))

        self.btn_renomear_colunas = ctk.CTkButton(self, text="Renomear Colunas", width=200, command=lambda: master.show_frame(RenomearColunas))

        self.btn_renomear_colunas.pack(pady=(0,5))
        