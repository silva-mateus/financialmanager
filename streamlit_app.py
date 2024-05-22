
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime

# Conexão com o banco de dados
def connect_db():
    return mysql.connector.connect(
        host,
        user,
        password,
        database
    )

# Inserir nova receita
def insert_income(name, description, date, category, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO income (Name, Description, Date, Category, Amount) VALUES (%s, %s, %s, %s, %s)",
        (name, description, date, category, amount)
    )
    conn.commit()
    conn.close()

# Inserir nova despesa
def insert_expense(name, description, date, category, amount, recurring, recurring_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expense (Name, Description, Date, Category, Amount, Recurring, RecurringType) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, description, date, category, amount, recurring, recurring_type)
    )
    conn.commit()
    conn.close()

# Obter dados de uma tabela
def get_table_data(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    conn.close()
    return rows, columns

# Função principal da aplicação
def main():
    st.title("Gerenciador Financeiro")

    menu = ["Adicionar Receita", "Adicionar Despesa", "Visualizar Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Adicionar Receita":
        st.subheader("Adicionar Receita")

        name = st.text_input("Nome")
        description = st.text_input("Descrição")
        date = st.date_input("Data", datetime.today())
        category = st.text_input("Categoria")
        amount = st.number_input("Quantia", min_value=0.0, format="%.2f")

        if st.button("Adicionar"):
            if name and description and category:
                insert_income(name, description, date, category, amount)
                st.success("Receita adicionada com sucesso!")
            else:
                st.error("Preencha todos os campos")

    elif choice == "Adicionar Despesa":
        st.subheader("Adicionar Despesa")

        name = st.text_input("Nome")
        description = st.text_input("Descrição")
        date = st.date_input("Data", datetime.today())
        category = st.text_input("Categoria")
        amount = st.number_input("Quantia", min_value=0.0, format="%.2f")
        recurring = st.checkbox("Recorrente")
        recurring_type = st.text_input("Tipo de Recorrência", value="mensal" if recurring else "")

        if st.button("Adicionar"):
            if name and description and category:
                insert_expense(name, description, date, category, amount, recurring, recurring_type)
                st.success("Despesa adicionada com sucesso!")
            else:
                st.error("Preencha todos os campos")

    elif choice == "Visualizar Dashboard":
        st.subheader("Dashboard")

        # Obtendo dados das tabelas
        income_data, income_columns = get_table_data("income")
        expense_data, expense_columns = get_table_data("expense")

        # Depuração: Exibir dados brutos
        #st.write("Dados de Receita:", income_data)
        #st.write("Dados de Despesa:", expense_data)

        # Convertendo para DataFrame
        income_df = pd.DataFrame(income_data, columns=income_columns)
        expense_df = pd.DataFrame(expense_data, columns=expense_columns)

        # Depuração: Exibir DataFrames
        st.write("DataFrame de Receita:", income_df)
        st.write("DataFrame de Despesa:", expense_df)

        # Gráfico de pizza para receitas e despesas
        if not income_df.empty and not expense_df.empty:
            income_df['Quantia'] = income_df['Amount'].astype(float)
            expense_df['Quantia'] = expense_df['Amount'].astype(float)

            combined_df = pd.concat([
                income_df[['Date', 'Category', 'Quantia']].assign(Tipo='Receita'),
                expense_df[['Date', 'Category', 'Quantia']].assign(Tipo='Despesa')
            ])

            fig = px.pie(combined_df, names='Tipo', values='Quantia', title='Distribuição de Receitas e Despesas')
            st.plotly_chart(fig)

            # Tabela de receitas e despesas
            st.dataframe(combined_df)
        else:
            st.info("Nenhuma transação encontrada")

if __name__ == '__main__':
    main()
