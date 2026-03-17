import pandas as pd

# =====================================================
# 1. Ler arquivo
# =====================================================
df = pd.read_excel("internacoes_mes_fevereiro.xlsx")

# =====================================================
# 2. Dicionário de renomeação (somente o que foi pedido)
# =====================================================
renomear = {
    "DT_REFERENCIA_5000": "DT INTERNACAO",
    "CD_SENHA": "SENHA",
    "CD_CARTEIRINHA_USUARIO": "COD USUARIO",
    "NM_BENEFICIARIO": "USUARIO",
    "DT_NASCIMENTO": "DT NASCIMENTO",
    "NM_OPERADORA_SAUDE": "BASE FULL",
    "CD_PROCEDIMENTO": "COD PROCEDIMENTO",
    "NOME_PROCEDIMENTO": "PROCEDIMENTO",
    "CD_FILIAL": "COD FILIAL",
    "NM_FANTASIA_FILIAL": "FILIAL",
    "CD_PRESTADOR": "COD PRESTADOR",
    "NM_FANTASIA_PRESTADOR_EXECUTANTE": "PRESTADOR",
    "CD_REDE_ATENDIMENTO": "REDE ATENDIMENTO",
    "CATEGORIA": "CATEGORIA DE INTERNACAO",
    "TIPO_ATENDIMENTO": "TP ATENDIMENTO"
}

df = df.rename(columns=renomear)

# =====================================================
# 3. Criar colunas novas (vazias), se não existirem
# =====================================================
colunas_novas = [
    "BASE", "SIGLA", "ESTADO", "TP ATENDIMENTO", "STATUS RESPOSTA",
    "OPERADOR", "CONTATO", "DT ENVIO MANUAL", "DATA DO CONTATO",
    "LIDA", "RESPOSTA DE IDENTIFICACAO", "STATUS", "DATA DE ENVIO",
    "P1", "P2", "P3", "P4", "P5", "P6",
    "COMEN P1", "COMEN P2", "COMEN P3",
    "COMEN P4", "COMEN P5", "COMEN P6"
]

for col in colunas_novas:
    if col not in df.columns:
        df[col] = ""

# =====================================================
# 4. Ordem FINAL das colunas (IDADE no lugar de IDADE T)
# =====================================================
ordem_colunas = [
    "COD FILIAL",
    "FILIAL",
    "BASE FULL",
    "BASE",
    "SIGLA",
    "ESTADO",
    "SENHA",
    "CD_USUARIO",          # se existir, apenas reposiciona
    "COD USUARIO",
    "USUARIO",
    "CPF_BENEFICIARIO",
    "TELEFONE",
    "DT NASCIMENTO",
    "IDADE",
    "COD PRESTADOR",
    "PRESTADOR",
    "COD PROCEDIMENTO",
    "PROCEDIMENTO",
    "REDE ATENDIMENTO",
    "TP ATENDIMENTO",
    "CATEGORIA DE INTERNACAO",
    "STATUS RESPOSTA",
    "DT INTERNACAO",
    "DT ENVIO",
    "CHAVE",
    "OPERADOR",
    "CONTATO",
    "DT ENVIO MANUAL",
    "DATA DO CONTATO",
    "LIDA",
    "RESPOSTA DE IDENTIFICACAO",
    "STATUS",
    "DATA DE ENVIO",
    "P1", "P2", "P3", "P4", "P5", "P6",
    "COMEN P1", "COMEN P2", "COMEN P3",
    "COMEN P4", "COMEN P5", "COMEN P6"
]

# Manter somente colunas existentes (segurança)
ordem_colunas = [c for c in ordem_colunas if c in df.columns]

# Reordenar DataFrame
df = df[ordem_colunas]

# =====================================================
# 5. Salvar arquivo final
# =====================================================
df.to_excel("BASE_FINAL_ORGANIZADA.xlsx", index=False)

print("Arquivo gerado com sucesso (IDADE ajustada).")
