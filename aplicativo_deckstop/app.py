import customtkinter as ctk
from views.menu_frame import MenuFrame


ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Meu APP")
        self.geometry("500x300")

        self.current_frame = None
        self.menu_frame = MenuFrame

        self.show_frame(MenuFrame)
    
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)

