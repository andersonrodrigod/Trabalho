import pandas as pd

class ExcluirLinhasController:
    def processar_arquivo(self, arquivo, config):
        import time
        time.sleep(2)  # Simula processamento
        
        dados_processados = {}
        excel_file = pd.ExcelFile(arquivo)
        
        # Carrega todas as abas
        for aba in excel_file.sheet_names:
            df = pd.read_excel(arquivo, sheet_name=aba)

            # Se a aba estiver entre as selecionadas, aplica os filtros
            if aba in config['abas_selecionadas']:
                if config['excluir_vazias']:
                    df = df.dropna(how='all')
                
                if config['excluir_duplicatas']:
                    df = df.drop_duplicates()
                
                for criterio in config['criterios_personalizados']:
                    df = self.aplicar_criterio(df, criterio, config['tipo_busca'])
            
            # Independentemente de ter sido alterada ou não, adiciona ao resultado
            dados_processados[aba] = df
        
        return dados_processados


    def aplicar_criterio(self, df, criterio, tipo_busca):
        """Aplica um critério de exclusão ao DataFrame"""
        valor = criterio['valor']
        coluna = criterio['coluna']
        
        if coluna:  # Apenas na coluna específica
            if coluna in df.columns:
                if tipo_busca == 'contem':
                    mask = ~df[coluna].astype(str).str.contains(valor, na=False)
                else:  # busca exata
                    mask = df[coluna].astype(str) != valor
                df = df[mask]
        else:  # Em todas as colunas
            mask = pd.Series([True] * len(df))
            for col in df.columns:
                if tipo_busca == 'contem':
                    col_mask = ~df[col].astype(str).str.contains(valor, na=False)
                else:
                    col_mask = df[col].astype(str) != valor
                mask = mask & col_mask
            df = df[mask]
        
        return df
