# Relatorio de Diferencas - Pipelines Complicacao Cirurgica vs Internacoes

Data: 2026-02-27

## Escopo comparado
- `1.0 criar_orquestra.py`
- `2.0 enviar_status_orquestra.py`
- `3.0 orquestracao_usuarios.py`

Projetos:
- A: `C:\Users\anderson.dossantos\Desktop\dev\Trabalho\Complicação Cirurgica\pipeline`
- B: `C:\Users\anderson.dossantos\Desktop\dev\Trabalho\Internações\pipeline`

## Resumo executivo
- `1.0`: diferenca apenas de arquivo-base de entrada (dataset).
- `2.0`: diferenca pequena, mas com impacto importante em parsing de dados:
  - A preserva telefones como texto (`dtype` explicito).
  - B nao preserva esse `dtype`.
  - Nome da coluna de data de envio difere (`Data de envio` vs `Data do envio`).
- `3.0`: diferenca de regra de negocio:
  - B tem regra extra para `ENCERRAR_CONTATO_NAO_TEM_INTERESSE`.
  - Limiar de `LIDA_REPOSTA_NAO` difere (A: `>=1`, B: `>=2`).
  - A tem regra `mask_lida_resposta_sim_sem_resposta`; B nao.

## Quantidade de diferencas (git numstat)
- `1.0 criar_orquestra.py`: `+2 / -2`
- `2.0 enviar_status_orquestra.py`: `+1 / -6`
- `3.0 orquestracao_usuarios.py`: `+9 / -21`

## Diferencas por arquivo

### 1.0 criar_orquestra.py
Impacto: baixo (parametrizacao de fonte).

Principais linhas:
- A: `C:\Users\anderson.dossantos\Desktop\dev\Trabalho\Complicação Cirurgica\pipeline\1.0 criar_orquestra.py:9`
  - `Lendo arquivo COMPLICAÇÃO JANEIRO 27.02.xlsx`
- A: `...\1.0 criar_orquestra.py:10`
  - `pd.read_excel("COMPLICAÇÃO JANEIRO 27.02.xlsx", sheet_name="BASE")`
- B: `C:\Users\anderson.dossantos\Desktop\dev\Trabalho\Internações\pipeline\1.0 criar_orquestra.py:9`
  - `Lendo arquivo BASE JANEIRO INTERNAÇÕES MAIN.xlsx`
- B: `...\1.0 criar_orquestra.py:10`
  - `pd.read_excel("BASE JANEIRO INTERNAÇÕES MAIN.xlsx", sheet_name="BASE")`

Conclusao: a logica do arquivo e igual; muda apenas o nome da base.

### 2.0 enviar_status_orquestra.py
Impacto: medio/alto (consistencia de chave/telefone e compatibilidade de coluna).

Diferenca 1: leitura tipada de telefones
- A tem:
  - `...\Complicação Cirurgica\pipeline\2.0 enviar_status_orquestra.py:18`
  - `dtype_usuarios = {c: str for c in colunas_telefone if c in colunas_usuarios}`
  - `...:19` leitura da aba `usuarios` com `dtype=dtype_usuarios`
- B nao tem esse bloco.

Risco: sem `dtype`, o Excel pode converter telefone para float/notacao cientifica e quebrar match/normalizacao.

Diferenca 2: nome da coluna de data no status
- A usa `Data de envio` em `...\2.0 enviar_status_orquestra.py:71`
- B usa `Data do envio` em `...\Internações\...\2.0 enviar_status_orquestra.py:66`

Risco: usar a coluna errada gera `NaT` em massa e afeta filtro temporal/ordenacao.

### 3.0 orquestracao_usuarios.py
Impacto: alto (decisao de processo/acao para contato).

Pontos de divergencia de regra:

1) Regra extra de encerramento por desinteresse (so B)
- B: `...\Internações\pipeline\3.0 orquestracao_usuarios.py:144`
  - `ENCERRAR_CONTATO_NAO_TEM_INTERESSE`
- B: `...:192`
  - `mask_nao_tem_interesse` com `RESPOSTA == "Não tenho interesse"`
- B: `...:210`
  - aplica `PROCESSO = "ENCERRAR_CONTATO_NAO_TEM_INTERESSE"`

2) Limiar para resposta nao
- A: `...\Complicação Cirurgica\pipeline\3.0 orquestracao_usuarios.py:193`
  - `LIDA_REPOSTA_NAO >= 1`
- B: `...\Internações\pipeline\3.0 orquestracao_usuarios.py:187`
  - `LIDA_REPOSTA_NAO >= 2`

3) Regra combinada existente so em A
- A: `...\3.0 orquestracao_usuarios.py:177`
  - `mask_lida_resposta_sim_sem_resposta`
- A: `...:211` aplica para `ENCERRAR_CONTATO_LIDOS_RESPOSTA_SIM`
- B nao possui esse bloco.

4) Troca de contato (`MUDAR_CONTATO_*`)
- A e B agora estao alinhados com a correção: `processos_troca_contato` e exclusao de mesmo slot/telefone enviado.
  - A: `...\Complicação Cirurgica\pipeline\3.0 orquestracao_usuarios.py:103,118`
  - B: `...\Internações\pipeline\3.0 orquestracao_usuarios.py:103,118`

## Onde esta o custo de manutencao hoje
- Mesmo fluxo com pequenas variacoes de schema (nome de arquivo/coluna) e limiares de regra.
- Alteracao manual em dois repositorios aumenta risco de drift (um corrige, outro nao).

## Plano recomendado para unificar manutencao
1. Extrair variacoes para configuracao (`yaml/json` por projeto), mantendo um codigo unico.
2. Parametrizar no minimo:
   - `base_input_file`
   - `status_data_envio_col` (`Data de envio` ou `Data do envio`)
   - `preserve_phone_dtype` (true/false)
   - thresholds de negocio (`lida_resposta_nao_min`, etc.)
   - habilitar/desabilitar regra `nao_tem_interesse`
3. Criar modulo comum para regras (`orquestracao_rules.py`) e somente carregador de config por projeto.
4. Adicionar testes de regressao com 2 fixtures (Complicacao e Internacoes) validando colunas `PROCESSO` e `ACAO`.
5. Rodar os dois cenarios no mesmo CI local (ou script unico) para evitar divergencia futura.

## Prioridade de alinhamento imediato
1. Levar leitura tipada de telefones para Internacoes no `2.0`.
2. Parametrizar a coluna de data (`Data de envio`/`Data do envio`) em ambos.
3. Decidir oficialmente se `LIDA_REPOSTA_NAO` deve ser `>=1` ou `>=2` por projeto (documentar).
4. Documentar regra `Nao tenho interesse` como diferenca intencional ou portar para ambos.
