import pandas as pd

df1 = pd.read_excel("total1.xlsx", sheet_name="Em_uma_escala_de_0_a_10_quan", usecols=["Nome", "Cod.", "responsavel",  "Resposta"])

df2 = pd.read_excel("total1.xlsx", sheet_name="Existe_um_ponto_focal_de_rel", usecols=[ "Cod.", "Resposta"])
df3 = pd.read_excel("total1.xlsx", sheet_name="Como_voce_avalia_o_seu_relac", usecols=[ "Cod.", "Opção"])
df4  = pd.read_excel("total1.xlsx", sheet_name="Como_voce_avalia_o_cumprimen", usecols=["Cod.", "Opção"])
df5  = pd.read_excel("total1.xlsx", sheet_name="Se_voce_atua_na_rede_propria", usecols=["Cod.", "Opção"])
df6  = pd.read_excel("total1.xlsx", sheet_name="Qual_e_sua_maior_dificuldade", usecols=["Cod.", "Opção"])

# Merge progressivo
df_merged = df1.rename(columns={"Resposta": "Escala_0a10"})
df2 = df2.rename(columns={"Resposta": "Ponto_Focal"})
df3 = df3.rename(columns={"Opção": "Avaliação_Relac"})
df4 = df4.rename(columns={"Opção": "Cumprimento"})
df5 = df5.rename(columns={"Opção": "Atuação_Rede_Propria"})
df6 = df6.rename(columns={"Opção": "Dificuldade"})


df_merged = df_merged.merge(df2, on="Cod.", how="left")
df_merged = df_merged.merge(df3, on="Cod.", how="left")
df_merged = df_merged.merge(df4, on="Cod.", how="left")
df_merged = df_merged.merge(df5, on="Cod.", how="left")
df_merged = df_merged.merge(df6, on="Cod.", how="left")

ordem = [
    "Cod.", 
    "Nome", 
    "responsavel", 
    "Ponto_Focal",
    "Escala_0a10", 
    "Avaliação_Relac", 
    "Cumprimento", 
    "Atuação_Rede_Propria", 
    "Dificuldade"
]

df_merged = df_merged[ordem]

print(df_merged.columns)

df_merged.to_excel("merged_output.xlsx", index=False)