import streamlit as st
import pandas as pd


st.set_page_config(page_title="Finanças", page_icon="💰")

st.text("hello world!")

st.markdown("""
# Boas vindas!
 
## Nosso app financeiro

            
Espero que você goste.
            
""")

file_upload = st.file_uploader(label="Faça upload dos dados aqui", type=["csv"])

if file_upload:
    # leitura
    df = pd.read_csv(file_upload)
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    # exibir
    exp1 = st.expander("Dados Brutos")
    columns_fmt = {"Valor": st.column_config.NumberColumn("Valor", format="R$%d")}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    # institucional
    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")

    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])

    with tab_data:
        st.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)

    # graficos
    with tab_share:

        date = st.date_input("Data para visualização",
                             min_value=df_instituicao.index.min(),
                             max_value=df_instituicao.index.max(),)

        last_dt = df_instituicao.sort_index().iloc[-1]
        st.bar_chart(last_dt)


