1️⃣ Conceito geral do pipeline

Este pipeline trabalha com duas visões de contagem:

Contagem TOTAL (QT_*)

Contagem por telefone + nome (colunas originais: LIDA, ENTREGUE, etc.)

Essas duas contagens não usam a mesma chave e não têm o mesmo nível de confiabilidade.
Isso é uma decisão consciente.

2️⃣ Contagem TOTAL (QT_*)
🔹 Como funciona
contagem_total = (
    df_status
    .groupby(["Contato", "STATUS_MAP"])
    .size()
    .unstack(fill_value=0)
)

df_novos["QT_*"] = df_novos["CHAVE STATUS"].map(contagem_total)


A contagem TOTAL é feita exclusivamente pela chave Contato

Contato vem da CHAVE RELATORIO

Os valores QT_* representam o histórico total associado àquela chave

⚠️ Limitação importante (erro conhecido)

Se a CHAVE RELATORIO mudou ou veio errada em algum momento,
o histórico TOTAL ficará fragmentado.

Ou seja:

Se uma mesma pessoa teve mais de uma CHAVE RELATORIO

O QT_* não irá somar tudo

Esse erro não é corrigido automaticamente

✔ Esse comportamento é assumido e documentado
✔ O erro é visível e auditável

3️⃣ Contagem por telefone + nome (colunas originais)
🔹 Como funciona
contagem_tel_nome = (
    df_status
    .groupby(["NOME_NORM", "TELEFONE_NORM", "STATUS_MAP"])
    .size()
    .unstack(fill_value=0)
)

df_novos[col] = (
    (NOME_NORM, TELEFONE ENVIADO_NORM)
    → contagem_tel_nome
)


Essa contagem usa:

NOME_NORM

TELEFONE ENVIADO

Ela representa o histórico daquele telefone específico

Independe da CHAVE RELATORIO

✅ Quando funciona bem

Nome correto

Telefone correto

TELEFONE ENVIADO preenchido

❌ Quando falha

Se a CHAVE RELATORIO estiver errada
e o telefone não for corretamente identificado,
essa contagem também ficará errada.

4️⃣ Fallback (NOME + TELEFONE)
🔹 O que o fallback faz

O fallback não resolve tudo. Ele:

Só roda quando não entrou via chave

Tenta casar:

NOME_NORM

TELEFONE 1 (normalizado)

Se encontrar:

preenche TELEFONE ENVIADO

preenche CHAVE STATUS

permite que a contagem funcione

🔹 Código-chave do fallback
df_novos["TELEFONE ENVIADO_NORM"] = df_novos["TELEFONE 1"].apply(normalizar_tel)


⚠️ IMPORTANTE
O fallback só verifica o TELEFONE 1
Ele não olha TELEFONE 2–5

Isso é intencional, para evitar custo computacional alto.

5️⃣ Erro conhecido: CHAVE errada + telefone fora do TELEFONE 1
🚨 Situação problemática

Quando:

A CHAVE RELATORIO está errada

O telefone correto não está no TELEFONE 1

O fallback não consegue identificar o telefone

O pipeline não sabe qual telefone usar

Resultado:

TELEFONE ENVIADO fica vazio

Contagem por telefone + nome fica errada

QT_* pode ficar fragmentado

6️⃣ O que FAZER quando esse erro ocorrer (procedimento operacional)
✅ Regra prática (IMPORTANTE)

Sempre que for disparar para um NOVO telefone
em um registro com ERRO DE CHAVE,
mover esse telefone para a coluna TELEFONE 1.

Por quê?

O fallback só olha o TELEFONE 1

Isso garante que:

o telefone seja identificado

TELEFONE ENVIADO seja preenchido

a contagem volte a funcionar corretamente

🔁 Resumo operacional

Identificar registros com:

STATUS CHAVE = ERRO

Ao usar novo telefone:

mover para TELEFONE 1

Rodar o pipeline normalmente

✔ Simples
✔ Explícito
✔ Auditável
✔ Sem custo computacional extra

7️⃣ Decisão consciente do projeto

Este projeto não tenta corrigir automaticamente todos os erros, porque:

O custo computacional ficou muito alto

A correção automática pode errar silenciosamente

O erro é raro, identificável e corrigível manualmente

Preferimos erro explícito + correção humana
a automação pesada e opaca.

8️⃣ Frase final (resumo mental)

QT_ depende da chave.
As colunas normais dependem do telefone.
Se a chave errar, o telefone precisa estar no TELEFONE 1.*