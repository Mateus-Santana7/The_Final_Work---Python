import streamlit as st
import pandas as pd
from Banco_clinica import criar_tabela, inserir_consulta, listar_consultas, excluir_consulta


st.set_page_config(
    page_title="Sistema de Agendamento de Consultas",
    layout="wide"
)


criar_tabela()

st.title(" Sistema de Agendamento de Consultas Médicas")


st.subheader(" Agendar Nova Consulta")

with st.form("form_cadastro", clear_on_submit=True):
    col_a, col_b = st.columns(2)

    with col_a:
        paciente = st.text_input("Nome do Paciente:")
        especialidade = st.selectbox(
            "Especialidade:",
            ["Cardiologia", "Dermatologia", "Pediatria", "Ortopedia", "Ginecologia", "Clínica Geral"]
        )
        medico = st.text_input("Nome do Médico:")

    with col_b:
        valor_consulta = st.number_input(
            "Valor da Consulta (R$):",
            min_value=0.0,
            step=10.0
        )
        data = st.date_input("Data da Consulta:")

    enviado = st.form_submit_button("Salvar Agendamento")

    if enviado:
       
        if paciente.strip() == "" or medico.strip() == "":
            st.error(" Preencha os campos obrigatórios (Paciente e Médico) antes de salvar.")
        elif valor_consulta <= 0:
            st.error(" O valor da consulta deve ser maior que R$ 0,00.")
        else:
            inserir_consulta(
                paciente.strip(),
                especialidade,
                medico.strip(),
                valor_consulta,
                str(data)
            )
            st.success(f" Consulta do paciente '{paciente}' agendada com sucesso!")
            st.rerun()

st.divider()


st.subheader(" Painel de Análises e Consultas Agendadas")

df = listar_consultas()

if df.empty:
    st.info("Nenhuma consulta cadastrada ainda. Use o formulário acima para começar.")
else:
  
    st.write("####  Filtros Interativos")
    col_f1, col_f2 = st.columns(2)

    with col_f1:
      
        opcoes_especialidades = ["Todas"] + list(df["especialidade"].unique())
        especialidade_filtrada = st.selectbox("Filtrar por Especialidade:", opcoes_especialidades)

    with col_f2:
        
        valor_min = float(df["valor_consulta"].min())
        valor_max = float(df["valor_consulta"].max())

        if valor_min == valor_max:
            valor_max += 1.0

        faixa_valor = st.slider(
            "Filtrar por Faixa de Valor (R$):",
            min_value=valor_min,
            max_value=valor_max,
            value=(valor_min, valor_max)
        )

    df_filtrado = df.copy()

    if especialidade_filtrada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["especialidade"] == especialidade_filtrada]

    df_filtrado = df_filtrado[
        (df_filtrado["valor_consulta"] >= faixa_valor[0]) & 
        (df_filtrado["valor_consulta"] <= faixa_valor[1])
    ]

   
    st.write("####  Métricas")
    if not df_filtrado.empty:
        faturamento_total = df_filtrado["valor_consulta"].sum()
        valor_medio = df_filtrado["valor_consulta"].mean()
        total_consultas = len(df_filtrado)
    else:
        faturamento_total = 0.0
        valor_medio = 0.0
        total_consultas = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
    col2.metric("Valor Médio por Consulta", f"R$ {valor_medio:,.2f}")
    col3.metric("Total de Consultas", total_consultas)

  
    st.write("####  Gráficos")
    if not df_filtrado.empty:
        grafico_especialidade, grafico_medico = st.columns(2)

        with grafico_especialidade:
            st.markdown("**Faturamento Total por Especialidade**")
            total_por_especialidade = df_filtrado.groupby("especialidade")["valor_consulta"].sum()
            st.bar_chart(total_por_especialidade)

        with grafico_medico:
            st.markdown("**Quantidade de Consultas por Médico**")
            consultas_por_medico = df_filtrado.groupby("medico")["id"].count()
            st.bar_chart(consultas_por_medico)
    else:
        st.warning("Nenhuma consulta encontrada para os filtros aplicados.")

 
    st.write("####  Lista de Consultas Cadastradas")
    st.dataframe(df_filtrado, use_container_width=True)

    st.divider()

   
    st.subheader(" Cancelar / Excluir Consulta")

    with st.expander("Excluir uma consulta por ID"):
        ids_validos = df["id"].tolist()

        id_para_excluir = st.number_input(
            "ID da consulta para excluir:",
            min_value=int(df["id"].min()),
            max_value=int(df["id"].max()),
            step=1
        )

        if st.button("Excluir Consulta"):
            if id_para_excluir in ids_validos:
                excluir_consulta(id_para_excluir)
                st.success(f" Consulta com ID {id_para_excluir} foi excluída com sucesso!")
                st.rerun()
            else:
                st.error(f" A consulta com ID {id_para_excluir} não foi encontrada no banco de dados.")
