from datetime import date, datetime


data_str = "25/11/2025"
data_str_1 = "28/11/2025"


data_internacao = datetime.strptime(data_str, "%d/%m/%Y").date()
data_internacao_1 = datetime.strptime(data_str_1, "%d/%m/%Y").date()

print("Data original:", data_internacao)

if data_internacao < data_internacao_1:
    print("Data de internação é anterior a 28/11/2025")
else:
    print("Data de internação é igual ou posterior a 28/11/2025")


