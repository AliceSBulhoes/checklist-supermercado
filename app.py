# Importando bibliotecas necessárias
import streamlit as st
import time
import pandas as pd
# Importando funções
from utils.tabelas import criar_tabelas, sql_query

def login() -> bool:
    """
    Renderiza a interface de login do sistema.
    Coleta nome e cargo do usuário, valida as informações e armazena o estado de login na sessão.

    Retorna:
        bool: True se o login for bem-sucedido, False caso contrário.
    """
    st.title("Login")

    # Inputs do usuário
    nome = st.text_input("Nome do usuário")
    cargo = st.text_input("Cargo")

    # Verifica se cliclou no botãoi
    if st.button("Entrar"):
        # Verifica os campos
        if verificar_usuario(nome, cargo): 
            return True

    return False


def verificar_usuario(nome: str, cargo: str) -> bool:
    """
    Função para verificar a autenticação
    """

    # Para uma lógica mais complexa, poderia adicionar um filtro
    # no proprio query para fazer essa comparação com WHERE
    query = '''SELECT * FROM funcionarios'''

    # Chamando função
    df_funcionarios = sql_query(query)

    # Verifica se há um funcionário com nome e cargo correspondentes
    match = df_funcionarios[
        (df_funcionarios['nome'].str.lower() == nome.strip().lower()) &
        (df_funcionarios['cargo'].str.lower() == cargo.strip().lower())
    ]

    if not match.empty:
        # Se encontrar correspondência, salva os dados na sessão
        st.session_state['logged_in'] = True
        st.session_state['cargo'] = match.iloc[0]['cargo']
        st.session_state['nome'] = match.iloc[0]['nome']

        # Mensagem de sucesso e redirecionamento
        st.success("Login bem-sucedido!")
        time.sleep(2)  # Espera 2 segundos antes de redirecionar
        st.switch_page("./pages/1_Home.py")
        return True
    else:
        # Exibe erro se não encontrou correspondência
        st.error("Nome ou cargo inválido. Tente novamente.")
    
    return False


def configura_pagina() -> None:
    """
    Configura a interface visual da página de login.
    Define título, ícone, layout e estado da barra lateral.
    """
    st.set_page_config(
        page_title="Login - Checklist Streamlit",
        page_icon=":clipboard:",
        layout="centered",
        initial_sidebar_state="expanded"
    )


def main() -> None:
    """
    Função principal da aplicação.
    Verifica se o usuário já está logado e redireciona para a home, ou exibe o formulário de login.
    """
    configura_pagina()
    criar_tabelas()

    # Se o usuário já estiver logado, redireciona para a home
    if st.session_state.get('logged_in'):
        st.switch_page("./pages/1_Home.py")
    else:
        login()


# Executa a função principal apenas se o script for chamado diretamente
if __name__ == "__main__":
    main()
