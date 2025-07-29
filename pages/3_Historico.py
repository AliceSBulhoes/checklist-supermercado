# Importando dependencias
import streamlit as st
import pandas as pd
from datetime import date 
# Importando funções
from components.auth import verifica_login  # Garante que só usuários logados vejam o histórico
from utils.sqlUtils import sql_query, excluir_diario

def configura_pagina() -> None:
    """
    Define as configurações visuais da página de histórico.
    Inclui título, ícone, layout e estado da barra lateral.
    """
    st.set_page_config(
        page_title="Histórico",
        page_icon=":material/view_cozy:",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def estilizando_pagina() -> None:
    """
    Estilização da página Historico com variáveis separadas
    """
    with open('./style/variaveis.css') as vars_file, open('./style/historico_style.css') as style_file:
        css = f"<style>{vars_file.read()}\n{style_file.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


def historico() -> None:
    """
    Renderiza a interface da página de histórico.
    Exibe uma mensagem introdutória e, futuramente, os registros preenchidos pelos usuários.
    """
    st.markdown("# Histórico de Checklists")
    st.markdown("###### Aqui você pode visualizar o histórico de atividades realizadas no sistema.")

    try:
        # Tenta carregar as respostas salvas anteriormente
        query = '''SELECT funcionarios.nome, funcionarios.cargo, itens_checklist.descricao, respostas_checklist.comentario, respostas_checklist.feito, respostas_checklist.data, respostas_checklist.imagem_path
        FROM funcionarios, itens_checklist, respostas_checklist
        WHERE funcionarios.id_funcionario = respostas_checklist.id_funcionarios AND itens_checklist.id_itens_checklist = respostas_checklist.id_itens_checklist
        '''

        df = sql_query(query)

        df['data'] = pd.to_datetime(df['data'])

        if df.empty:
            st.info("Ainda não há checklists salvos.")
        else:
            if 'nome' in st.session_state:
                df = df[df['nome'] == st.session_state['nome']]
            
            if df.empty:
                st.info("Você ainda não tem checklists salvos.")
                return

            # Extrai todas as datas únicas para o seletor
            all_dates = df['data'].dt.date.unique()
            # Ordena as datas em ordem decrescente (mais recente primeiro)
            all_dates_sorted = sorted(all_dates, reverse=True)

            if all_dates_sorted:
                # Usa a data mais recente como valor padrão
                default_date = all_dates_sorted[0]
            else:
                default_date = date.today()

            # Widget de seleção de data
            selected_date = st.date_input("Selecione a data para filtrar:",key="filtro" ,value=default_date, min_value=min(all_dates_sorted) if all_dates_sorted else None, max_value=max(all_dates_sorted) if all_dates_sorted else None)

            # Filtra o DataFrame pela data selecionada
            filtered_df = df[df['data'].dt.date == selected_date]

            if filtered_df.empty:
                st.info(f"Não há checklists para a data selecionada: **{selected_date.strftime('%d/%m/%Y')}**.")
                return

            # Ordena o DataFrame filtrado pela data para garantir uma ordem consistente
            filtered_df = filtered_df.sort_values(by='data', ascending=False) # Ordem decrescente (mais recente primeiro)

            # Cabeçalho para o dia selecionado (opcional, pode ser removido se o título principal for suficiente)
            st.markdown(f'### Checklists para {selected_date.strftime("%d/%m/%Y")}')
            
            for index, row in filtered_df.iterrows():
                data_formatada_hora = row['data'].strftime("%H:%M:%S")
                
                with st.expander(f"**{row['descricao']}** - {data_formatada_hora}"):
                    # Crie duas colunas dentro do expander
                    col_info, col_imagem = st.columns([2, 1]) # 2 partes para info, 1 para imagem (ajuste conforme necessário)

                    with col_info:
                        st.markdown(f"**Funcionário:** {row['nome']}")
                        st.markdown(f"**Cargo:** {row['cargo']}")
                        st.markdown(f"**Descrição:** {row['descricao']}")
                        st.markdown(f"**Feito:** {'Sim' if row['feito'] else 'Não'}")
                        if row['comentario']:
                            st.markdown(f"**Comentário:** {row['comentario']}")
                    
                    with col_imagem:
                        if row['imagem_path'] and row['imagem_path'] != "":
                            st.image(row['imagem_path'], caption="Imagem do Checklist", use_container_width =True)
                        else:
                            st.info("Nenhuma imagem para este checklist.")
    except Exception as e:
        st.error("Erro ao carregar o histórico.")
        st.exception(e)
    
    # Botão para o desenvolvimento
    if st.button(":material/delete: Excluir Registro Diário", key="btn_excluir"):
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
    estilizando_pagina()   # Fazendo a estilização do home
    configura_pagina()     # Aplica as configurações visuais da página
    historico()            # Carrega a interface do histórico


# Executa a aplicação apenas se o script for o ponto de entrada
if __name__ == "__main__":
    main()
