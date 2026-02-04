import pandas as pd

# =========================
# 1. Ler os arquivos
# =========================

df_base = pd.read_excel("BASE_FINAL_ORGANIZADA.xlsx")
df_tipo = pd.read_excel("TIPO_ATENDIMENTO.xlsx")

# =========================
# 2. Garantir mesmo tipo e limpar espaços
# =========================

df_base["SENHA"] = df_base["SENHA"].astype(str).str.strip()
df_tipo["CD_SENHA"] = df_tipo["CD_SENHA"].astype(str).str.strip()

# =========================
# 3. Criar o dicionário de mapeamento
# =========================

mapa_tp_atendimento = (
    df_tipo
    .set_index("CD_SENHA")["TIPO_ATENDIMENTO"]
    .to_dict()
)

# =========================
# 4. Aplicar o map
# =========================

df_base["TP ATENDIMENTO"] = df_base["SENHA"].map(mapa_tp_atendimento)

# =========================
# 5. Salvar o resultado
# =========================

df_base.to_excel(
    "BASE_FINAL_ORGANIZADA_COM_TP_ATENDIMENTO.xlsx",
    index=False
)

print("Arquivo gerado com sucesso!")
