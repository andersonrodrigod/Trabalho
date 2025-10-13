import pandas as pd
import warnings

warnings.simplefilter("ignore", UserWarning)

# --- 1. Arquivos ---
nao_respondidos = "base_nao_respondidos.xlsx"
base_principal = "Base Colaboradores Enfermagem.xlsx"
saida = "colaboradores_férias_encontrados.xlsx"

# --- 2. Ler o arquivo base_nao_respondidos ---
df_nao = pd.read_excel(nao_respondidos)

# --- 3. Filtrar apenas os que têm STATUS = DESLIGADO ---
df_desligados = df_nao[df_nao["STATUS"].str.strip().str.upper() == "FÉRIAS"]

# --- 4. Pegar os nomes da coluna Colaborador ---
nomes_desligados = df_desligados["Colaborador"].dropna().str.strip().str.upper().tolist()

print(f"🔍 Total de desligados encontrados: {len(nomes_desligados)}")

# --- 5. Ler a aba 'Base' do arquivo principal (linha 2 = cabeçalho real) ---
df_base = pd.read_excel(base_principal, sheet_name="Base", header=1)

# --- 6. Criar uma cópia padronizada (sem espaços e em maiúsculas) para comparação ---
df_base["Colab_upper"] = df_base["Colaborador"].astype(str).str.strip().str.upper()

# --- 7. Filtrar linhas da base cujo colaborador esteja entre os desligados ---
df_encontrados = df_base[df_base["Colab_upper"].isin(nomes_desligados)].drop(columns=["Colab_upper"])

print(f"✅ Colaboradores encontrados na Base: {len(df_encontrados)}")

# --- 8. Salvar em uma nova planilha ---
df_encontrados.to_excel(saida, index=False)

print(f"📁 Arquivo gerado com sucesso: {saida}")
