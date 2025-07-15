# Importando bibliotecas necessárias
import streamlit as st
import pandas as pd
import time

# Lista de cargos disponíveis
CARGOS = [
    "Repositor",
    "Gerente de loja",
    # Adicione outros cargos conforme necessário
]

def page_config() -> None:
    """Configurações da página Streamlit."""
    st.set_page_config(
        page_title="Login - Checklist Streamlit",
        page_icon=":clipboard:",
        initial_sidebar_state="expanded"
    )

def login() -> bool:
    """Função para realizar o login do usuário."""
    st.title("Login")
    # Input do usuário para o cargo
    cargo = st.text_input("Cargo")
    # Botão para realizar o login
    btn = st.button("Entrar")

    if btn:
        # Verifica se o cargo está na lista de cargos válidos
        if cargo.capitalize() in CARGOS:
            # Se o cargo for válido, armazena no estado da sessão
            st.session_state['logged_in'] = True
            st.success("Login bem-sucedido!")
            # Armazena o cargo no estado da sessão
            st.session_state['cargo'] = cargo
             # Simula um atraso para o feedback do usuário
            time.sleep(2) 
            # Redireciona para a página principal ou outra página conforme necessário
            st.switch_page("./pages/1_home.py")
            return True
        # Se o cargo não for válido, exibe uma mensagem de erro
        else:
            st.error("Cargo inválido. Tente novamente.")
            print("Cargo inválido:", cargo.capitalize())
            print("Cargos válidos:", CARGOS)
    return False

def main() -> None:
    """Função principal para executar o aplicativo Streamlit."""
    # Configurações da página
    page_config()
    # Verifica se o usuário já está logado
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        # Se já estiver logado, redireciona para a página principal
        st.switch_page("./pages/1_home.py")
    else:
        # Se não estiver logado, chama a função de login
        login()

if __name__ == "__main__":
    main()