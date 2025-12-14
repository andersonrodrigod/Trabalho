import pandas as pd

print("📘 Lendo os arquivos...")

df_usuarios = pd.read_excel("Usuarios_encontrados_STATUS.xlsx")
df_status = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="status")

print("🧹 Normalizando campos...")
usuarios_col = df_usuarios["USUARIO"].astype(str).str.strip()
status_contato_col = df_status["Contato"].astype(str).str.strip()

print("🔎 Procurando correspondências (contém)...")

resultados = []

for i, usuario in enumerate(usuarios_col):
    mask = status_contato_col.str.contains(usuario, na=False)
    
    if mask.any():
        linhas_encontradas = df_status[mask].copy()
        chave = df_usuarios.loc[i, "CHAVE"]
        linhas_encontradas["CHAVE"] = chave
        resultados.append(linhas_encontradas)

print("📊 Consolidando resultados...")

if resultados:
    df_final = pd.concat(resultados, ignore_index=True)
else:
    df_final = pd.DataFrame()

print("💾 Salvando arquivo final...")

df_final.to_excel("Status_com_CHAVE.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: Status_com_CHAVE.xlsx")
