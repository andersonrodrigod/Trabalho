import pandas as pd

# 1) Ler todas as abas
df_abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)

df_novos = df_abas["novos_contatos"]
df_nao_lidos = df_abas["contatos_nao_lidos"]
df_lidos = df_abas["contatos_lidos"]
df_lidos_nao_respondidos = df_abas["lidos_nao_respondidos"]
df_segundo_envio = df_abas["segundo_envio_lidas"]

# Normalizar para comparação
df_cod_nao_lidos = df_nao_lidos["Codigo"].dropna().astype(str)
df_nome_nao_lidos = df_nao_lidos["Nome"].dropna().astype(str)
df_prest_nao_lidos = df_nao_lidos["PRESTADOR"].dropna().astype(str)

df_cod_lidos_nao_respondidos = df_lidos_nao_respondidos["Codigo"].dropna().astype(str)
df_nome_lidos_nao_respondidos = df_lidos_nao_respondidos["Nome"].dropna().astype(str)
df_prest_lidos_nao_respondidos = df_lidos_nao_respondidos["PRESTADOR"].dropna().astype(str)


novos_cod = df_novos["Codigo"].astype(str)
novos_nome = df_novos["Nome"].astype(str)
novos_prest = df_novos["PRESTADOR"].astype(str)
novos_envio = df_novos["ENVIO"]

# 1️⃣ Condição 1: Código bate → envia
cond_codigo_nao_lidas = novos_cod.isin(df_cod_nao_lidos)
cond_codigo_lidas_nao_respondidas = novos_cod.isin(df_cod_lidos_nao_respondidos)

# 2️⃣ Condição 2: Código NÃO bate → checa nome E prestador
cond_nome_nao_lidas  = novos_nome.isin(df_nome_nao_lidos)
cond_prest_nao_lidas = novos_prest.isin(df_prest_nao_lidos)

cond_nome_lidas_nao_respondidas = novos_nome.isin(df_nome_lidos_nao_respondidos)
cond_prest_lidas_nao_respondidas = novos_prest.isin(df_prest_lidos_nao_respondidos)

cond_nome_prest_nao_lidas = ~cond_codigo_nao_lidas & (cond_nome_nao_lidas  & cond_prest_nao_lidas)

cond_nome_prest_lidas_nao_respondidas = ~cond_codigo_lidas_nao_respondidas & (cond_nome_lidas_nao_respondidas & cond_prest_lidas_nao_respondidas)

# 3️⃣ Máscara final → envia só os que NÃO existem
mascara_para_enviar_contatos_lidos = ~(cond_codigo_nao_lidas | cond_nome_prest_nao_lidas)

mascara_para_enviar_contatos_lidos_nao_respondidos = cond_codigo_lidas_nao_respondidas | cond_nome_prest_lidas_nao_respondidas

# 4️⃣ Seleção final → linhas que vão ser enviadas
linhas_para_enviar_contatos_lidos = df_novos[mascara_para_enviar_contatos_lidos]

linhas_para_enviar_contatos_lidos_nao_respondidos = df_novos[mascara_para_enviar_contatos_lidos_nao_respondidos]


print("Linhas para enviar contatos lidos:", len(linhas_para_enviar_contatos_lidos))
print("Total de linhas enviadas par lidas mas não respondidas:", len(mascara_para_enviar_contatos_lidos_nao_respondidos))

# 5️⃣ Atualizar contatos_lidos
df_lidos_atualizado = pd.concat([df_lidos, linhas_para_enviar_contatos_lidos], ignore_index=True)

df_segundo_envio_atualizado = pd.concat([df_segundo_envio, linhas_para_enviar_contatos_lidos_nao_respondidos], ignore_index=True)

# 6️⃣ Criar máscara total de enviados (lidos + nao respondidos)
mascara_enviados_total = (
    mascara_para_enviar_contatos_lidos |
    mascara_para_enviar_contatos_lidos_nao_respondidos
)

# 6️⃣ Remover enviados da aba novos_contatos
abas_novos_restante = df_novos[~mascara_enviados_total]

# 7️⃣ Criar NOVO ARQUIVO atualizado
with pd.ExcelWriter("novos_contatos_atualizado.xlsx", engine="openpyxl") as writer:
    abas_novos_restante.to_excel(writer, sheet_name="novos_contatos", index=False)
    df_nao_lidos.to_excel(writer, sheet_name="contatos_nao_lidos", index=False)
    df_lidos_atualizado.to_excel(writer, sheet_name="contatos_lidos", index=False)
    df_lidos_nao_respondidos.to_excel(writer, sheet_name="lidos_nao_respondidos", index=False)
    df_segundo_envio_atualizado.to_excel(writer, sheet_name="segundo_envio_lidas", index=False)


#criar novo arquivo

"""with pd.ExcelWriter("novos_contatos_atualizado.xlsx", engine="openpyxl") as writer:
    abas_novos.to_excel(writer, sheet_name="novos_contatos", index=False)
    abas_nao_lidos.to_excel(writer, sheet_name="contatos_nao_lidos", index=False)
    df_lidos_atualizado.to_excel(writer, sheet_name="contatos_lidos", index=False)"""