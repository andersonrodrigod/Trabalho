import pandas as pd


class ExcluirColunaController:
    def __init__(self, arquivo):
        
        self.caminho_arquivo = pd.ExcelFile(arquivo)
        self.df = None

    def carregar_dataframe(self):
        print("Carregando DataFrame do arquivo Excel...")
        self.df = pd.read_excel(self.caminho_arquivo)
        print("DataFrame carregado com sucesso.")
        return self.df
    
    def filtrar_colunas(self, colunas_escolhidas):
        print(f"Filtrando colunas:{colunas_escolhidas}...")

        if self.df is None:
            print("DataFrame não carregado. Carregando agora...")
            self.carregar_dataframe()

        print("Filtrando apenas as colunas selecionadas...")
        df_filtrado = self.df[colunas_escolhidas]

        print("devolvendo dataframe filtrado para a próxima etapa.")

        return df_filtrado
        
