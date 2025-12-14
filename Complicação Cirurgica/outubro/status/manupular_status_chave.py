import pandas as pd

# 1) Ler todas as abas
df_abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)

df_novos = df_abas["novos_contatos"]
df_nao_lidos = df_abas["contatos_nao_lidos"] 
df_lidos = df_abas["contatos_lidos"]
df_lidos_nao_respondidos = df_abas["lidos_nao_respondidos"]
df_segundo_envio = df_abas["segundo_envio_lidas"]

# 2) Normalizar coluna CHAVE
chave_nao_lidos = df_nao_lidos["Chave"].dropna().astype(str)
chave_lidos_nao_respondidos = df_lidos_nao_respondidos["Chave"].dropna().astype(str)

novos_chave = df_novos["Chave"].astype(str)

# 3) Condições usando SOMENTE a CHAVE
cond_chave_nao_lidos = novos_chave.isin(chave_nao_lidos)
cond_chave_lidos_nao_respondidos = novos_chave.isin(chave_lidos_nao_respondidos)

# 4) Máscaras finais
# Enviar para contatos_lidos → só os que NÃO estão em nao_lidos
mascara_para_enviar_contatos_lidos = ~cond_chave_nao_lidos

# Enviar para segundo envio → só os que estão em lidos_nao_respondidos
mascara_para_enviar_segundo_envio = cond_chave_lidos_nao_respondidos

# 5) Seleção final
linhas_para_enviar_contatos_lidos = df_novos[mascara_para_enviar_contatos_lidos]
linhas_para_enviar_segundo_envio = df_novos[mascara_para_enviar_segundo_envio]

print("Linhas para contatos lidos:", len(linhas_para_enviar_contatos_lidos))
print("Linhas para segundo envio:", len(linhas_para_enviar_segundo_envio))

# 6) Atualizar abas
df_lidos_atualizado = pd.concat(
    [df_lidos, linhas_para_enviar_contatos_lidos],
    ignore_index=True
)

df_segundo_envio_atualizado = pd.concat(
    [df_segundo_envio, linhas_para_enviar_segundo_envio],
    ignore_index=True
)

# 7) Máscara total de enviados
mascara_enviados_total = (
    mascara_para_enviar_contatos_lidos |
    mascara_para_enviar_segundo_envio
)

# 8) Remover enviados de novos_contatos
abas_novos_restante = df_novos[~mascara_enviados_total]

# 9) Salvar novo arquivo
with pd.ExcelWriter("novos_contatos_atualizado.xlsx", engine="openpyxl") as writer:
    abas_novos_restante.to_excel(writer, sheet_name="novos_contatos", index=False)
    df_nao_lidos.to_excel(writer, sheet_name="contatos_nao_lidos", index=False)
    df_lidos_atualizado.to_excel(writer, sheet_name="contatos_lidos", index=False)
    df_lidos_nao_respondidos.to_excel(writer, sheet_name="lidos_nao_respondidos", index=False)
    df_segundo_envio_atualizado.to_excel(writer, sheet_name="segundo_envio_lidas", index=False)
