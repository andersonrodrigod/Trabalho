import customtkinter as ctk
from views.menu_frame import MenuFrame
from views.detalhamento_frame import Detalhamento
from views.concaternar_frame import Concatenar
from views.excluir_linhas_frame import ExcluirLinhas
from views.substituir_valores_frame import SubstituirValores
from views.merge_planilhas_frame import MergePlanilhas
from views.renomear_abas_frame import RenomearAbas
from views.renomear_colunas_frame import RenomearColunas


ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Meu APP")

        #self.geometry("900x800")

        self.current_frame = None
        self.menu_frame = MenuFrame

        self.show_frame(RenomearColunas)
    
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)

