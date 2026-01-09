import pandas as pd


df_base = pd.read_excel('SETEMBRO.xlsx')

colunas_desejadas = [
    'STATUS BOT', 'BASE', 'COD USUARIO', 'USUARIO', 'TELEFONE RELATORIO',
    'TELEFONE 1', 'TELEFONE 2', 'TELEFONE 3', 'TELEFONE 4', 'TELEFONE 5',
    'PRESTADOR', 'PROCEDIMENTO', 'TP ATENDIMENTO', 'DT INTERNACAO', 'ENVIO',
    'ULTIMO STATUS DE ENVIO','IDENTIFICACAO', 'RESPOSTA', 'LIDA', 'ENTREGUE', 'ENVIADA',
    'NAO_ENTREGUE_META', 'MENSAGEM_NAO_ENTREGUE', 'EXPERIMENTO',
    'OPT_OUT', 'TELEFONE ENVIADO', 'CHAVE RELATORIO', 'CHAVE STATUS',
    'STATUS TELEFONE', 'STATUS CHAVE', "PROCESSO", "QT TELEFONE"
]

abas = [
    "HAP", "NDI SP", "NDI MINAS", "CCG", "CLINIPAN"
]




mask_sem_telefone = df_base["TELEFONE"].isna() | (df_base["TELEFONE"] == "")
filtro_sem_telefone = df_base[mask_sem_telefone]

mask_aba_hap = df_base["BASE"] == ""

def montar_df_final(df_base):
    df_final = pd.DataFrame(columns=colunas_desejadas)

    if "BASE" in df_base: df_final["BASE"] = df_base["BASE"]
    if "COD USUARIO" in df_base: df_final["COD USUARIO"] = df_base["COD USUARIO"]
    if "USUARIO" in df_base: df_final["USUARIO"] = df_base["USUARIO"]
    if "TELEFONE" in df_base: df_final["TELEFONE RELATORIO"] = df_base["TELEFONE"]
    if 'TP ATENDIMENTO' in df_base: df_final['TP ATENDIMENTO'] = df_base['TP ATENDIMENTO']
    if 'DT ENVIO' in df_base: df_final['ENVIO'] = df_base['DT ENVIO']
    if 'CHAVE' in df_base: df_final['CHAVE RELATORIO'] = df_base['CHAVE']

    for col in colunas_desejadas:
        if col not in df_final.columns:
            df_final[col] = ""

    return df_final

df_usuarios = montar_df_final(filtro_sem_telefone)

# Preservar a ordem original através do índice
df_usuarios = df_usuarios.reset_index(drop=False).rename(columns={'index': 'ordem_original'})

# Criar arquivo Excel com múltiplas abas
with pd.ExcelWriter('SETEMBRO_COM_TELEFONES.xlsx', engine='openpyxl') as writer:
    # Criar uma aba para cada BASE
    for aba in abas:
        # Filtrar dados da aba específica
        df_aba = df_usuarios[df_usuarios['BASE'] == aba].copy()
        
        # Remover a coluna de ordem antes de salvar
        if 'ordem_original' in df_aba.columns:
            df_aba = df_aba.drop(columns=['ordem_original'])
        
        # Escrever na aba correspondente
        if not df_aba.empty:
            df_aba.to_excel(writer, sheet_name=aba, index=False)
    
    # Criar uma aba com todos os dados na ordem original
    df_todos = df_usuarios.sort_values('ordem_original').copy()
    df_todos = df_todos.drop(columns=['ordem_original'])
    df_todos.to_excel(writer, sheet_name='TODOS', index=False)




