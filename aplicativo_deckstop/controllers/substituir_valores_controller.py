# controllers/substituir_valores_controller.py
import pandas as pd

class SubstituirValoresController:
    def processar_arquivo(self, arquivo, config):
        """
        Processa o arquivo Excel aplicando as substituições configuradas
        """
        dados_processados = {}
        excel_file = pd.ExcelFile(arquivo)
        
        for aba in excel_file.sheet_names:
            df = pd.read_excel(arquivo, sheet_name=aba)

            # Aplica substituições apenas nas abas selecionadas
            if aba in config['abas_selecionadas']:
                df = self.aplicar_substituicoes(df, config)
            
            dados_processados[aba] = df
        
        return dados_processados

    def aplicar_substituicoes(self, df, config):
        """
        Aplica todas as substituições no DataFrame
        """
        for substituicao in config['substituicoes']:
            valor_antigo = substituicao['valor_antigo']
            valor_novo = substituicao['valor_novo']
            coluna = substituicao['coluna']
            tipo_busca = substituicao['tipo_busca']
            case_sensitive = substituicao['case_sensitive']
            
            if coluna:  # Apenas na coluna específica
                if coluna in df.columns:
                    df[coluna] = self.substituir_coluna(
                        df[coluna], valor_antigo, valor_novo, tipo_busca, case_sensitive
                    )
            else:  # Em todas as colunas
                for col in df.columns:
                    df[col] = self.substituir_coluna(
                        df[col], valor_antigo, valor_novo, tipo_busca, case_sensitive
                    )
        
        return df

    def substituir_coluna(self, serie, valor_antigo, valor_novo, tipo_busca, case_sensitive):
        """
        Substitui valores em uma série/coluna específica
        """
        if tipo_busca == 'exato':
            # Substituição exata
            if case_sensitive:
                mask = serie.astype(str) == valor_antigo
            else:
                mask = serie.astype(str).str.lower() == valor_antigo.lower()
            
            serie = serie.astype(str)
            serie[mask] = valor_novo
            
        else:  # substituição por conteúdo
            if case_sensitive:
                serie = serie.astype(str).str.replace(
                    valor_antigo, valor_novo, regex=False
                )
            else:
                # Para case insensitive, usamos regex com flag
                import re
                serie = serie.astype(str).apply(
                    lambda x: re.sub(
                        re.escape(valor_antigo), 
                        valor_novo, 
                        x, 
                        flags=re.IGNORECASE
                    ) if pd.notna(x) else x
                )
        
        return serie