# Importando dependencias
import streamlit as st
import pandas as pd
import os
import time
# Importando funções
from utils.sqlUtils import sql_query, salvar_respostas

def configura_pagina() -> None:
    """
    Define as configurações visuais da página Streamlit.
    Inclui o título, ícone, layout e estado inicial da barra lateral.
    """
    st.set_page_config(
        page_title="Checklist - Checklist Streamlit",
        page_icon=":clipboard:",
        layout="centered",
        initial_sidebar_state="expanded"
    )


def checklist() -> None:
    """
    Renderiza a interface principal do checklist de tarefas.
    Permite que o usuário marque itens, adicione comentários, envie imagens
    e salve os dados, após validação obrigatória da imagem.
    """
    st.title("Checklist de Tarefas")
    st.write("Marque os itens concluídos, adicione comentários e carregue a imagem obrigatória.")

    # Carrega os itens de checklist filtrados pelo cargo do usuário
    df_itens = carregar_itens_checklist()

    # Se não houver itens para o cargo, interrompe a execução da página
    if df_itens is None:
        return

    # Renderiza todos os itens e armazena as respostas em uma lista
    respostas = [renderizar_item(row) for _, row in df_itens.iterrows()]

    # Ao clicar no botão de salvar, realiza a validação e salva as respostas
    if st.button("Salvar Checklist"):
        respostas = list(st.session_state.get("respostas_checklist", {}).values())

        # Filtra apenas os válidos (feito e imagem existe)
        respostas_validas = [
            r for r in respostas
            if r.get("feito") and r.get("imagem_path") and os.path.exists(r.get("imagem_path"))
        ]

        if not respostas_validas:
            st.warning("Nenhum item marcado como feito com imagem encontrada.")
        else:
            salvar_respostas(respostas_validas)
            st.success("Itens válidos salvos com sucesso!")
            time.sleep(2)
            st.switch_page('./pages/1_Home.py')



def carregar_itens_checklist() -> pd.DataFrame:
    """
    Carrega os itens de checklist com base no cargo do usuário atual.
    Retorna:
      Um DataFrame filtrado ou None caso não haja itens.
    """
    query = '''SELECT * FROM  itens_checklist'''

    # Consulta a tabela itens checklist
    df = sql_query(query)

    cargo = st.session_state.get('cargo', '').lower()

    # Filtra os itens que correspondem ao cargo do usuário
    df_filtrado = df[df['cargo'].str.lower() == cargo]

    return df_filtrado if not df_filtrado.empty else None


def renderizar_item(row: pd.Series) -> dict:
    """
    Renderiza um único item do checklist com opções interativas.
    """

    item_id = row['id_itens_checklist']
    estado_antigo = st.session_state.get("respostas_checklist", {}).get(item_id, {})

    with st.expander(row['descricao']):
        # Checkbox para marcar como feito
        feito = st.checkbox(
            "Item concluído",
            value=estado_antigo.get("feito", False),
            key=f"check_{item_id}"
        )

        # Comentário opcional
        comentario = ""
        if st.checkbox("Adicionar comentário", key=f"comment_{item_id}"):
            comentario = st.text_area(
                "Comentário",
                value=estado_antigo.get("comentario", ""),
                key=f"input_{item_id}"
            )

        # Upload obrigatório
        imagem = st.file_uploader(
            "Carregar imagem (obrigatória)",
            type=["jpg", "png"],
            key=f"image_{item_id}"
        )

        pasta_destino = ""
        nome_arquivo = ""
        caminho_arquivo = ""

        if imagem is not None:
            pasta_destino = f"./assets/image/{st.session_state['nome']}-{st.session_state['cargo']}"
            os.makedirs(pasta_destino, exist_ok=True)
            extensao = os.path.splitext(imagem.name)[1]
            nome_arquivo = f"image_{item_id}_{st.session_state['nome']}{extensao}"
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho_arquivo, "wb") as f:
                f.write(imagem.read())
        else:
            caminho_arquivo = estado_antigo.get("imagem_path", "")

        # Atualiza no session_state
        if "respostas_checklist" not in st.session_state:
            st.session_state["respostas_checklist"] = {}

        st.session_state["respostas_checklist"][item_id] = {
            "id_itens_checklist": item_id,
            "descricao": row['descricao'],
            "feito": feito,
            "comentario": comentario,
            "imagem_path": caminho_arquivo
        }

        return st.session_state["respostas_checklist"][item_id]


def main():
    """ Função principal do aplicativo. Garante que o usuário esteja logado antes de exibir a checklist."""
    configura_pagina()
    if st.session_state.get('logged_in'):
        checklist()
    else:
        st.switch_page("./app.py")


if __name__ == "__main__":
    main()
