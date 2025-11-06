import streamlit as st
from models.data_model import load_data
from views.main_view import layout_geral_status, layout_geral_status_resposta, layout_geral_elogio


st.set_page_config(layout="wide")

st.title("Atualização da Planilha")



def main():
    st.sidebar.header("Painel de Filtros")
    st.set_page_config(page_title="Dashboard", layout="wide")

    pagina = st.sidebar.selectbox("Escolha o Tipo de Análise de Dados", [
        "Tabela Global"
    ])

    if pagina == "Tabela Global":
        st.title("Tabelas Pesquisa de Satisfação")
        layout_geral_status()   
        layout_geral_status_resposta()
        layout_geral_elogio()
   




    


if __name__ == "__main__":
    main()

