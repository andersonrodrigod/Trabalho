import pandas as pd
from datetime import date
import unicodedata

# --- Caminho do arquivo ---
arquivo = "Planilha Julho 15.10.xlsx"

# --- Ler a planilha ---
df = pd.read_excel(arquivo, sheet_name="BASE")
df.columns = df.columns.str.lower().str.strip()

# --- Checar colunas obrigatórias ---
colunas_necessarias = {"operador", "tipo de contato"}
if not colunas_necessarias.issubset(df.columns):
    raise ValueError(f"A planilha precisa ter as colunas: {colunas_necessarias}")

# --- Adicionar data atual ---
data_atual = date.today()
df["data"] = data_atual

# --- Remover linhas vazias ---
df = df.dropna(subset=["operador", "tipo de contato"])

# --- Normalizar nome dos operadores ---
def normalizar_operador(nome):
    nome = str(nome).strip().lower()  # remove espaços e coloca em minúsculas
    nome = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("utf-8")  # remove acentos
    return nome.title()  # retorna com a primeira letra maiúscula

df["operador"] = df["operador"].apply(normalizar_operador)

# --- Normalizar tipo de contato ---
def normalizar_texto(txt):
    txt = str(txt).strip().lower()
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("utf-8")
    if "whats" in txt:
        return "whats app"
    elif "liga" in txt:
        return "ligacao"
    else:
        return txt

df["tipo de contato"] = df["tipo de contato"].apply(normalizar_texto)

# --- Operadores e tipos fixos ---
todos_operadores = sorted(df["operador"].unique())
tipos = ["whats app", "ligacao"]

# --- Criar todas as combinações ---
combinacoes = pd.MultiIndex.from_product(
    [[data_atual], todos_operadores, tipos],
    names=["data", "operador", "tipo de contato"]
)

# --- Agrupar dados e preencher zeros ---
resumo = (
    df.groupby(["data", "operador", "tipo de contato"])
    .size()
    .reindex(combinacoes, fill_value=0)
    .reset_index(name="quantidade")
)

# --- Criar tabelas separadas ---
tabela_whats = resumo[resumo["tipo de contato"] == "whats app"].pivot(
    index="data", columns="operador", values="quantidade"
).fillna(0)

tabela_ligacao = resumo[resumo["tipo de contato"] == "ligacao"].pivot(
    index="data", columns="operador", values="quantidade"
).fillna(0)

# --- Concatenar lado a lado com MultiIndex correto ---
tabela_final = pd.concat([tabela_whats, tabela_ligacao], axis=1, keys=["WHATSAPP", "LIGAÇÃO"])

# --- Ajustar nome do índice para 'data' e remover o rótulo 'operador' ---
tabela_final.index.name = "data"

# --- Salvar Excel mantendo MultiIndex e alinhamento correto ---
nome_saida = f"RESUMO_DIARIO_OPERADORES_{data_atual}.xlsx"
with pd.ExcelWriter(nome_saida) as writer:
    tabela_final.to_excel(writer, index=True, merge_cells=True)

print(f"✅ Planilha '{nome_saida}' gerada com sucesso!")
