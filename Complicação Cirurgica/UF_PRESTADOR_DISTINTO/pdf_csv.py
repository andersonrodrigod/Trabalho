import re
import pdfplumber
import pandas as pd

PDF_PATH = "PA PARANGABA.pdf"
CSV_PATH = "pa_parangaba_final.csv"

# Exemplo de linha esperada:
# 172226623 JOBSON DE BRITO RODRIGUES ONC-GJ POSTO ONCOLOGIA 16 ONCOLOGIA 02-MAR-26
LINHA_REGEX = re.compile(
    r"^(?P<cd_atendimento>\d{9,})\s+"
    r"(?P<nome_paciente>.+?)\s+"
    r"(?P<acomodacao>ONC-GJ\s+POSTO\s+ONCOLOGIA)\s+"
    r"(?P<leito>\S+)\s+"
    r"(?P<clinica>ONCOLOGIA)\s+"
    r"(?P<data_ocupacao>\d{2}-[A-Z]{3}-\d{2})$"
)


def limpar_linha(linha):
    """Corrige casos em que o nome do paciente cola com 'ONC-GJ'."""
    return re.sub(r"([A-Z])(?=ONC-GJ\s+POSTO\s+ONCOLOGIA)", r"\1 ", linha)


def extrair_setor(texto_pagina):
    match = re.search(r"Nm Setor:\s*\d+\s*(.+)", texto_pagina)
    return match.group(1).strip() if match else ""


def extrair_registros(pdf_path):
    registros = []

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text() or ""
            if not texto:
                continue

            setor = extrair_setor(texto)
            linhas = [l.strip() for l in texto.splitlines() if l.strip()]

            for linha in linhas:
                if not re.match(r"^\d{9,}", linha):
                    continue

                linha = limpar_linha(linha)
                match = LINHA_REGEX.match(linha)
                if not match:
                    continue

                dados = match.groupdict()
                dados["setor"] = setor
                registros.append(dados)

    return registros


def main():
    registros = extrair_registros(PDF_PATH)
    df = pd.DataFrame(registros)

    colunas = [
        "cd_atendimento",
        "nome_paciente",
        "setor",
        "acomodacao",
        "leito",
        "clinica",
        "data_ocupacao",
    ]

    if df.empty:
        df = pd.DataFrame(columns=colunas)
    else:
        df = df[colunas]

    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    print(f"OK - CSV gerado com {len(df)} linhas: {CSV_PATH}")


if __name__ == "__main__":
    main()
