import streamlit as st
import pandas as pd
from components.auth import verifica_login  # Garante que só usuários logados vejam o histórico
from utils.sqlUtils import sql_query, excluir_diario

def configura_pagina() -> None:
    """
    Define as configurações visuais da página de histórico.
    Inclui título, ícone, layout e estado da barra lateral.
    """
    st.set_page_config(
        page_title="Histórico - Checklist Streamlit",
        page_icon=":clipboard:",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def historico() -> None:
    """
    Renderiza a interface da página de histórico.
    Exibe uma mensagem introdutória e, futuramente, os registros preenchidos pelos usuários.
    """
    st.title("Histórico de Checklists")
    st.write("Aqui você pode visualizar o histórico de atividades realizadas no sistema.")

    try:
        # Tenta carregar as respostas salvas anteriormente
        query = '''SELECT funcionarios.nome, funcionarios.cargo, itens_checklist.descricao, respostas_checklist.comentario, respostas_checklist.feito, respostas_checklist.data, respostas_checklist.imagem_path
        FROM funcionarios, itens_checklist, respostas_checklist
        WHERE funcionarios.id_funcionario = respostas_checklist.id_funcionarios AND itens_checklist.id_itens_checklist = respostas_checklist.id_itens_checklist
        '''

        df = sql_query(query)

        if df.empty:
            st.info("Ainda não há checklists salvos.")
        else:
            # Filtro para apenas o funcionário logado
            df = df[df['nome'] == st.session_state['nome']]
            # Exibe a tabela de registros
            st.dataframe(df)

    except Exception as e:
        st.error("Erro ao carregar o histórico.")
        st.exception(e)
    
    # Botão para o desenvolvimento
    if st.button("Excluir Registro diário"):
        query = '''DELETE FROM respostas_checklist 
        WHERE DATE(data) = :hoje
        '''
         
        excluir_diario(query)




def main() -> None:
    """
    Função principal da página de histórico.
    Verifica login, configura o layout e carrega o conteúdo da tela.
    """
    verifica_login()       # Garante que apenas usuários logados tenham acesso
    configura_pagina()     # Aplica as configurações visuais da página
    historico()            # Carrega a interface do histórico


# Executa a aplicação apenas se o script for o ponto de entrada
if __name__ == "__main__":
    main()
