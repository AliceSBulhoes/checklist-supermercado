import streamlit as st
import pandas as pd
from components.auth import verifica_login


def historico() -> None:
    """Função para exibir a página de histórico."""
    st.title("Histórico")
    st.write("Aqui você pode visualizar o histórico de atividades.")

def configura_pagina() -> None:
    """Configurações da página Streamlit."""
    st.set_page_config(
        page_title="Histórico - Checklist Streamlit",
        page_icon=":clipboard:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def main() -> None:
    """Função principal para executar a página de histórico."""
    # Verifica se o usuário está logado
    verifica_login()
    # Configura a página
    configura_pagina()
    # Chama a função de histórico
    historico()


if __name__ == "__main__":
    main()
