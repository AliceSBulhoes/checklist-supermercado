import streamlit as st
import pandas as pd


def checklist() -> None:
    """Função para exibir a página de checklist."""
    st.title("Checklist")
    st.write("Aqui você pode realizar o checklist de tarefas.")

   
def main() -> None:
    """Função principal para executar a página de checklist."""
    # Verifica se o usuário está logado
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        checklist()
    else:
        st.switch_page("./app.py")

if __name__ == "__main__":
    main()