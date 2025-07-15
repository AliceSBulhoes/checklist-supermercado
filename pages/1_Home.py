import streamlit as st
import pandas as pd

btn = st.button("Sair")
if btn:
    # Limpa o estado da sessão
    st.session_state.clear()
    # Redireciona para a página de login
    st.switch_page("./app.py")