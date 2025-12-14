import pandas as pd
import re
import numpy as np
from controle_usuarios import detectar_usuarios_defeituosos

print("\n================ INICIANDO PROCESSAMENTO ================\n")

# ==========================================================
# 1) LER TODAS AS ABAS
# ==========================================================
df_abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)

df_usuarios = df_abas["usuarios"].copy()
df_nao_lidos = df_abas["usuarios_nao_lidos"].copy()
df_lidos = df_abas["usuarios_lidos"].copy()
df_respondidos = df_abas["usuarios_respondidos"].copy()
df_segundo_envio = df_abas["segundo_envio_lidos"].copy()
df_duplicados = df_abas["usuarios_duplicados"].copy()
df_resolvidos = df_abas["usuarios_resolvidos"].copy()
df_lidos_nao_respondidos = df_abas["usuarios_lidos_nao_respondidos"].copy()
df_defeituosos = df_abas["usuarios_defeituosos"].copy()
df_trocar_contato_lida2 = df_abas["trocar_contato_lida"].copy()

# ================================================================================
# 2) CONDIÇÃO PARA ENVIAR PARA USUARIOS RESPECTIVAS ABAS COM SUAS CONDICÕES
# ================================================================================
colunas_status = [
    "LIDA", "ENTREGUE", "ENVIADA",
    "NAO_ENTREGUE_META", "MENSAGEM_NAO_ENTREGUE",
    "EXPERIMENTO", "OPT_OUT"
]

abas_base = {
    "HAP": "HAP",
    "CCG": "CCG",
    "NDI SP": "NDI SP",
    "NDI MINAS": "NDI MINAS",
    "CLINIPAN": "CLINIPAN"
}

ch_usuarios = df_usuarios["CHAVE RELATORIO"].astype(str).str.strip()
ch_respondidos = df_respondidos["CHAVE RELATORIO"].astype(str).str.strip()
ch_lidos = df_lidos["CHAVE RELATORIO"].astype(str).str.strip()
df_usuarios["SOMA_STATUS"] = df_usuarios[colunas_status].sum(axis=1)


mask_em_respondidos = ch_usuarios.isin(ch_respondidos)
mask_em_lidos = ch_usuarios.isin(ch_lidos)
mask_lida1 = df_usuarios["LIDA"] == 1
mask_lida2 = df_usuarios["LIDA"] == 2

mask_acumalador = df_usuarios["SOMA_STATUS"] >= 4
df_usuarios.loc[mask_acumalador, "QT TELEFONE"] += 1
df_usuarios.loc[mask_acumalador, colunas_status] = np.nan

df_para_base = df_usuarios[mask_acumalador].copy()

for base, nome_aba in abas_base.items():
    
    df_base = df_para_base[df_para_base["BASE"] == base]

    if not df_base.empty:
        print(f"📌 Movendo {len(df_base)} registros para a aba {nome_aba}...")

        if nome_aba not in df_abas:
            df_abas[nome_aba] = pd.DataFrame(columns=df_usuarios.columns)
        
        # Registrar contagem antes de mover
        print(f"📌 {len(df_base)} registros enviados para a aba: {nome_aba}")

        # Mostrar as primeiras 5 chaves
        print("   → CHAVES:")
        print(df_base["CHAVE RELATORIO"].head().to_list())

        df_abas[nome_aba] = pd.concat([df_abas[nome_aba], df_base], ignore_index=True)


mask_para_resolvidos = mask_em_respondidos
mask_para_lidos_nao_respondidos = ~mask_em_respondidos & mask_em_lidos & ~mask_acumalador
mask_para_segundo_envio = mask_lida1 & ~mask_em_respondidos & ~mask_acumalador
mask_para_trocar_contato_lida2 = mask_lida2 & ~mask_em_respondidos & ~mask_acumalador
 
df_novos_resolvidos = df_usuarios[mask_para_resolvidos].copy()
df_lidos_nao_respondidos = df_usuarios[mask_para_lidos_nao_respondidos]
df_segundo_envio = df_usuarios[mask_para_segundo_envio]
df_trocar_contato_lida2 = df_usuarios[mask_para_trocar_contato_lida2]

mask_remover = (
    mask_para_resolvidos |
    mask_para_lidos_nao_respondidos |
    mask_para_segundo_envio |
    mask_para_trocar_contato_lida2 |
    mask_acumalador
)

df_resolvidos = pd.concat(
    [df_resolvidos, df_novos_resolvidos],
    ignore_index=True
)

df_resolvidos = df_resolvidos.drop_duplicates(
    subset=["CHAVE RELATORIO"],
    keep="first"
)

df_usuarios = df_usuarios[~mask_remover].copy()

df_usuarios_defeituosos = detectar_usuarios_defeituosos(df_usuarios, df_resolvidos)




# ==========================================================
# 4) ATUALIZAR DICIONÁRIO DE ABAS ANTES DE SALVAR
# ==========================================================


df_usuarios = df_usuarios.drop(columns=["SOMA_STATUS"], errors="ignore")

df_abas["usuarios"] = df_usuarios
df_abas["usuarios_resolvidos"] = df_resolvidos
df_abas["usuarios_lidos_nao_respondidos"] = df_lidos_nao_respondidos
df_abas["segundo_envio_lidos"] = df_segundo_envio
df_abas["usuarios_defeituosos"] = df_usuarios_defeituosos
df_abas["trocar_contato_lida"] = df_trocar_contato_lida2



# (abas_base já foram atualizadas no loop anterior)


print("\n📁 Salvando arquivo final...")

# ==========================================================
# 5) SALVAR TODAS AS ABAS NO EXCEL
# ==========================================================
with pd.ExcelWriter("novos_contatos_atualizado.xlsx", engine="openpyxl") as writer:
    for nome_aba, df in df_abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)


print("\n🎉 Arquivo 'novos_contatos_atualizado.xlsx' salvo com sucesso!")












print("\n================ RESULTADOS DAS DISTRIBUIÇÕES ================\n")


print("\n📌 Após limpeza da aba 'usuarios':")
print("Total restante:", len(df_usuarios))
print("Primeiras chaves restantes:")
print(df_usuarios["CHAVE RELATORIO"].head().to_list())

# 1) RESOLVIDOS
print(f"📌 RESOLVIDOS: {len(df_resolvidos)} registros")
if len(df_resolvidos) > 0:
    print("   → Primeiras CHAVES:")
    print(df_resolvidos["CHAVE RELATORIO"].head().to_list())
print("--------------------------------------------------------------")

# 2) LIDOS NÃO RESPONDIDOS
print(f"📌 LIDOS NÃO RESPONDIDOS: {len(df_lidos_nao_respondidos)} registros")
if len(df_lidos_nao_respondidos) > 0:
    print("   → Primeiras CHAVES:")
    print(df_lidos_nao_respondidos["CHAVE RELATORIO"].head().to_list())
print("--------------------------------------------------------------")

# 3) SEGUNDO ENVIO
print(f"📌 SEGUNDO ENVIO: {len(df_segundo_envio)} registros")
if len(df_segundo_envio) > 0:
    print("   → Primeiras CHAVES:")
    print(df_segundo_envio["CHAVE RELATORIO"].head().to_list())
print("--------------------------------------------------------------")

# 4) BASES (HAP, CCG, etc.)
print("\n================ MOVIMENTAÇÃO PARA BASES ================\n")
for base, nome_aba in abas_base.items():
    if nome_aba in df_abas:
        qtd = len(df_abas[nome_aba])
        print(f"📌 {nome_aba}: {qtd} registros")
        if qtd > 0:
            print("   → Primeiras CHAVES:")
            print(df_abas[nome_aba]["CHAVE RELATORIO"].head().to_list())
    print("--------------------------------------------------------------")



#df_usuarios = df_usuarios[~mask_acumalador].copy()






# prints de verificações
"""print(mask_para_segundo_envio.head(10))
print(df_usuarios.loc[mask_acumalador, colunas_status].head(10))
qt_cols = ["QT " + c for c in colunas_status] + ["QT TELEFONE"]

print("\n📌 Colunas QT correspondentes (devem TER valores):")
print(df_usuarios.loc[mask_acumalador, qt_cols].head(10))
print("Total Encontrados:", mask_para_segundo_envio.sum())
print(mask_para_resolvidos.head(10))
print("Total Encontrados:", mask_para_resolvidos.sum())
"""

# ==========================================================
# 3) CONDIÇÃO PARA ENVIAR PARA USUARIOS RESOLVIDOS
# ==========================================================



