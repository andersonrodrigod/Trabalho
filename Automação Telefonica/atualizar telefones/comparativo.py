import pandas as pd

# Lê os arquivos
antigo = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE", dtype=str)
novo = pd.read_excel("NOVEMBRO GERAL_atualizado.xlsx", sheet_name="BASE", dtype=str)
dados = pd.read_excel("complica_novembro_sp_55.xlsx", dtype=str)[["Codigo", "Telefone 2"]].dropna()

# Remove duplicados de COD USUARIO nos dois arquivos
antigo_unico = antigo.drop_duplicates(subset="COD USUARIO", keep=False)
novo_unico = novo.drop_duplicates(subset="COD USUARIO", keep=False)

# Faz o merge para comparar os telefones
comparativo = pd.merge(
    antigo_unico[["COD USUARIO", "USUARIO", "TELEFONE"]],
    novo_unico[["COD USUARIO", "TELEFONE"]],
    on="COD USUARIO",
    suffixes=("_ANTIGO", "_NOVO")
)

# Lista de usuários que deveriam ser atualizados
codigos_validos = set(dados["Codigo"].unique())

# Telefones que foram alterados
alterados = comparativo[comparativo["TELEFONE_ANTIGO"] != comparativo["TELEFONE_NOVO"]]

# Verifica se houve alteração indevida
alteracoes_indesejadas = alterados[~alterados["COD USUARIO"].isin(codigos_validos)]

# Resultado
if not alteracoes_indesejadas.empty:
    print(f"\n⚠️ ATENÇÃO: {len(alteracoes_indesejadas)} telefones foram alterados indevidamente!")
    print(alteracoes_indesejadas)
else:
    print("\n✅ Tudo certo! Nenhum telefone foi alterado fora dos usuários previstos.")
