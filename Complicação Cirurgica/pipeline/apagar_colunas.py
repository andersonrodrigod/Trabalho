from openpyxl import load_workbook

arquivo_original = "COMPLICAÇÃO DEZEMBRO 2025 v2.xlsx"
arquivo_saida = "COMPLICAÇÃO DEZEMBRO 2025 v2_TRATADO.xlsx"

wb = load_workbook(arquivo_original)

ws = wb["STATUS"]

ws.delete_cols(1, 4)  # A:D

wb.save(arquivo_saida)

print("Arquivo criado (com possíveis limitações).")
