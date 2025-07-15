import streamlit as st

def navbar() -> None:
    """Exibe a barra lateral de navegação apenas se o usuário estiver logado."""
    st.sidebar.title("Menu")
    st.sidebar.page_link("./pages/1_Home.py", label="Home")
    st.sidebar.page_link("./pages/3_Historico.py", label="Histórico")
    btn_logout()

def btn_logout() -> None:
    """Botão de logout na barra lateral."""
    btn = st.sidebar.button("Sair do Sistema")
    if btn:
        st.session_state.clear()
        st.switch_page("./app.py")

def verifica_login() -> None:
    """Verifica se o usuário está logado, exibe a navbar ou redireciona para login."""
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        navbar()
    else:
        st.switch_page("./app.py")
