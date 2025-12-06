import pandas as pd

# Load the base Excel file and read the 'BASE' sheet
df_base = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE", dtype=str, engine="openpyxl")

# Load the new telephone data
df_tel = pd.read_excel("complica_novembro_minas_55.xlsx", dtype=str, engine="openpyxl")

# Select relevant columns and drop rows with missing Codigo or Telefone 2
df_tel = df_tel[["Codigo", "Telefone 2"]].dropna(subset=["Codigo", "Telefone 2"])

# Clean the Codigo.2 values to remove leading/trailing spaces and invisible characters
df_tel["Codigo"] = df_tel["Codigo"].astype(str).str.strip().str.replace('\u00A0', '', regex=True)

# Clean the Telefone 2 values and preserve 'sem numero' as valid
df_tel["Telefone 2"] = df_tel["Telefone 2"].astype(str).str.strip()

# Create a dictionary for quick lookup
tel_dict = df_tel.drop_duplicates(subset="Codigo").set_index("Codigo")["Telefone 2"].to_dict()

# Clean the COD USUARIO column in the base file
df_base["COD USUARIO"] = df_base["COD USUARIO"].astype(str).str.strip().str.replace('\u00A0', '', regex=True)

# Preserve the original TELEFONE column
df_base["TELEFONE_ANTIGO"] = df_base["TELEFONE"]

# Update the TELEFONE column using the dictionary, including 'sem numero' values
df_base["TELEFONE"] = df_base.apply(
    lambda row: tel_dict.get(row["COD USUARIO"], row["TELEFONE"]),
    axis=1
)

# Save the updated BASE sheet to a new Excel file
df_base.to_excel("NOVEMBRO GERAL_atualizado.xlsx", sheet_name="BASE", index=False, engine="openpyxl")