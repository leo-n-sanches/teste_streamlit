import streamlit as st
import pandas as pd

def calc_general_stats(df:pd.DataFrame):
    df_data = df.groupby(by="Data")[["Valor"]].sum()
    df_data["lag_1"] = df_data["Valor"].shift(1)
    df_data["diferença_mensal"] = df_data["Valor"] - df_data["lag_1"]
    df_data["media_6m_diferenca_mensal_absoluta"] = df_data["diferença_mensal"].rolling(6).mean()
    df_data["media_12m_diferenca_mensal_absoluta"] = df_data["diferença_mensal"].rolling(12).mean()
    df_data["media_24m_diferenca_mensal_absoluta"] = df_data["diferença_mensal"].rolling(24).mean()
    
    df_data["diferenca mensal relativa"] = df_data["Valor"] / df_data["lag_1"] - 1

    df_data["evolucao_6m_total"] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data["evolucao_12m_total"] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] - x[0])
    df_data["evolucao_24m_total"] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] - x[0])

    df_data["evolucao_6m_relativa"] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] / x[0] - 1)
    df_data["evolucao_12m_relativa"] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] / x[0] - 1)
    df_data["evolucao_24m_relativa"] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] / x[0] - 1)

    df_data = df_data.drop("lag_1", axis=1)

    return df_data

st.set_page_config(page_title="Finanças", page_icon="💰")


st.markdown("""
# Boas vindas!
 
## Ao app financeiro

            
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

    tab_data.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)

    # graficos
    with tab_share:
        
        date = st.selectbox("Filtro Data", options=df_instituicao.index)

        # date = st.date_input("Data para visualização",
        #                      min_value=df_instituicao.index.min(),
        #                      max_value=df_instituicao.index.max(),)
        
        # if date not in df_instituicao.index:
        #     st.warning("Entre com uma data valida")
        # else:
        #     st.bar_chart(df_instituicao.loc[date])


        st.bar_chart(df_instituicao.loc[date])

    df_stats = calc_general_stats(df)
    st.dataframe(df_stats)



