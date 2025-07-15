import streamlit as st
import pandas as pd
from components.auth import verifica_login


def historico() -> None:
    """Função para exibir a página de histórico."""
    st.title("Histórico")
    st.write("Aqui você pode visualizar o histórico de atividades.")


def main() -> None:
    """Função principal para executar a página de histórico."""
    # Verifica se o usuário está logado
    verifica_login()
    historico()


if __name__ == "__main__":
    main()
