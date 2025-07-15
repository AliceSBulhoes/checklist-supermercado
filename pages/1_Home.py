import streamlit as st
import pandas as pd
from components.auth import verifica_login

def home() -> None:
    """Função para exibir a página inicial após o login."""
    st.title("Página Inicial")
    st.write("Bem-vindo(a) ao sistema!")
    
    # Exibe o cargo do usuário logado
    if 'cargo' in st.session_state:
        st.write(f"Cargo: {st.session_state['cargo']}")
    
    # Botão para iniciar o checklist
    btn_checklist()

def btn_checklist() -> None:
    """Função para exibir o botão de checklist."""
    # Botão para iniciar o checklist
    btn = st.button("Iniciar Checklist", on_click=lambda: st.switch_page("./pages/2_Checklist.py"))

    # Se o botão for clicado, redireciona para a página de checklist
    if btn:
        st.switch_page("./pages/2_Checklist.py")
    
def main() -> None:
    """Função principal para executar a página inicial."""
    # Verifica se o usuário está logado
    verifica_login()
    home()

if __name__ == "__main__":
    main()