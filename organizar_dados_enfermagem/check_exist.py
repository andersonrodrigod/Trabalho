import pandas as pd

def verificar_nomes(arquivo_excel, nome_coluna_1='Nome 1', nome_coluna_2='Nome 2'):
    # Lê o arquivo Excel
    df = pd.read_excel(arquivo_excel)

    # Remove espaços extras e converte para string
    nomes_1 = df[nome_coluna_1].dropna().astype(str).str.strip()
    nomes_2 = df[nome_coluna_2].dropna().astype(str).str.strip()

    # Verifica quais nomes de Nome 2 estão em Nome 1
    presentes = df[df[nome_coluna_2].astype(str).str.strip().isin(nomes_1)]
    ausentes = df[~df[nome_coluna_2].astype(str).str.strip().isin(nomes_1)]

    # Salva os resultados em arquivos separados
    presentes.to_excel('nomes_presentes.xlsx', index=False)
    ausentes.to_excel('nomes_ausentes.xlsx', index=False)

    print("✅ Arquivos gerados:")
    print("- nomes_presentes.xlsx → nomes de 'Nome 2' que estão em 'Nome 1'")
    print("- nomes_ausentes.xlsx → nomes de 'Nome 2' que NÃO estão em 'Nome 1'")

# Exemplo de uso
verificar_nomes('novo.xlsx')
