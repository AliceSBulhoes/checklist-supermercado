import streamlit as st
import pandas as pd
from components.auth import verifica_login  # Função de verificação de login
import time

def home() -> None:
    """
    Exibe a página inicial após o login.
    Mostra uma mensagem de boas-vindas, o cargo do usuário e o botão para iniciar o checklist.
    """
    st.title("Página Inicial")
    st.write("Bem-vindo(a) ao sistema!")

    # Exibe o cargo do usuário se estiver salvo na sessão
    if 'cargo' in st.session_state:
        st.write(f"Cargo: {st.session_state['cargo']}")

    # Exibe o botão para iniciar o checklist
    btn_checklist()


def configura_pagina() -> None:
    """
    Configura os parâmetros visuais da página inicial no Streamlit.
    Define título, ícone, layout e estado da barra lateral.
    """
    st.set_page_config(
        page_title="Página Inicial - Checklist Streamlit",
        page_icon=":clipboard:",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def btn_checklist() -> None:
    """
    Exibe o botão para iniciar o checklist.
    Ao clicar, redireciona o usuário para a página de checklist.
    """

    # Botão para Abrir Checklist
    if st.button("Abrir Checklist Diária"):
        st.switch_page("./pages/2_Checklist.py")


def main() -> None:
    """
    Função principal para executar a lógica da página inicial.
    Configura a interface, valida login e exibe conteúdo principal.
    """
    configura_pagina()
    verifica_login()  # Verifica se o usuário está logado antes de acessar
    home()  # Exibe a interface da home


# Executa o app caso este arquivo seja o ponto de entrada principal
if __name__ == "__main__":
    main()
