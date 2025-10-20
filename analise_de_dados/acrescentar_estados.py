import pandas as pd

# --- 1️⃣ Carregar a planilha ---
# (troque o caminho pelo seu arquivo)
df = pd.read_excel("planilhas/acrescento_dados.xlsx", sheet_name="respostas qr code")
#print(df.columns.tolist())



# --- 2️⃣ Dicionário com os estados e suas siglas ---
estados_siglas = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO"
}

# --- 3️⃣ Criar nova coluna com as siglas ---
df["Sigla Estado"] = df["qual estado você reside? (input)"].map(estados_siglas)

# --- 4️⃣ (Opcional) Verificar se há estados não reconhecidos ---
nao_encontrados = df[df["Sigla Estado"].isna()]["qual estado você reside? (input)"].unique()

if len(nao_encontrados) > 0:
    print("⚠️ Estados não reconhecidos encontrados:")
    for estado in nao_encontrados:
        print(" -", estado)

# --- 5️⃣ Salvar o resultado ---
df.to_excel("acrescento_dados_com_siglas.xlsx", index=False)
print("✅ Nova planilha criada com a coluna de siglas.")
