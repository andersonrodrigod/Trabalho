import streamlit as st
import pandas as pd
from controllers.main_controller import contar_status, contar_status_resposta,contar_elogio_queixas_geral, contar_elogio, contar_queixas, contar_respostas, contar_elogios_queixas
from models.data_model import load_data

arquivo = "Planilha Julho 04.11.xlsx"

df = load_data(arquivo)

def layout_geral_status():
    

    st.subheader("Status: Resumo Geral")

    # Tabela
    resumo = contar_status(df)
    st.dataframe(pd.DataFrame(resumo, index=["Quantidade"]))

def layout_geral_status_resposta():
    st.subheader("Respostas: Resumo Geral")

    resumo = contar_status_resposta(df)

    st.dataframe(pd.DataFrame(resumo, index=["Quantidade"]))


def layout_geral_elogio():
    st.subheader("Elogios e Queixas: Resumo Geral")

    geral = contar_elogio_queixas_geral(df)
    elogio = contar_elogio(df)
    queixa = contar_queixas(df)
    elogio_queixa = contar_elogios_queixas(df)
    resposta = contar_respostas(df)

    st.dataframe(geral)
    st.subheader("Elogios")
    st.dataframe(elogio)
    st.subheader("Queixas")
    st.dataframe(queixa)
    st.subheader("Elogio ou Queixa")
    st.header(elogio_queixa)
    st.subheader("Tabela Total de Notas")
    st.dataframe(resposta)
    