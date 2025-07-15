# Importando bibliotecas necessárias
import streamlit as st
import time
from utils.fetch_json import fetch_json_data


def login() -> bool:
    """Função para realizar o login do usuário."""
    st.title("Login")
    # Input para o nome do usuário
    nome = st.text_input("Nome do usuário")
    # Input do usuário para o cargo
    cargo = st.text_input("Cargo")
    # Botão para realizar o login
    btn = st.button("Entrar")

    df_funcionarios = fetch_json_data('data/funcionarios.json')

    if btn:
        # Verifica se há um funcionário com nome e cargo correspondentes
        match = df_funcionarios[
            (df_funcionarios['nome'].str.lower() == nome.strip().lower()) &
            (df_funcionarios['cargo'].str.lower() == cargo.strip().lower())
        ]
        # Se houver correspondência, define o estado de sessão e redireciona
        if not match.empty:
            # Define o estado de sessão com os dados do funcionário
            st.session_state['logged_in'] = True
            st.session_state['cargo'] = match.iloc[0]['cargo']
            st.session_state['nome'] = match.iloc[0]['nome']
            # Exibe uma mensagem de sucesso e redireciona para a página inicial
            st.success("Login bem-sucedido!")
            # Aguarda 2 segundos antes de redirecionar
            time.sleep(2)
            # Redireciona para a página inicial
            st.switch_page("./pages/1_home.py")
            return True
        else:
            # Se não houver correspondência, exibe uma mensagem de erro
            st.error("Nome ou cargo inválido. Tente novamente.")

    return False


def configura_pagina() -> None:
    """Configurações da página Streamlit."""
    st.set_page_config(
        page_title="Login - Checklist Streamlit",
        page_icon=":clipboard:",
        layout="centered",
        initial_sidebar_state="expanded"
    )


def main() -> None:
    """Função principal para executar o aplicativo Streamlit."""
    # Configurações da página
    configura_pagina()
    # Verifica se o usuário já está logado
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        # Se já estiver logado, redireciona para a página principal
        st.switch_page("./pages/1_home.py")
    else:
        # Se não estiver logado, chama a função de login
        login()

if __name__ == "__main__":
    main()