# Importando dependencias
import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
# Importando funções
from utils.sqlUtils import sql_query, salvar_respostas, verificar_checklist_hoje
from components.auth import verifica_login

def configura_pagina() -> None:
    """
    Define as configurações visuais da página Streamlit.
    Inclui o título, ícone, layout e estado inicial da barra lateral.
    """
    st.set_page_config(
        page_title="Checklist Diário",
        page_icon=":material/check_box:",
        layout="centered",
    )

def estilizando_pagina() -> None:
    """
    Estilização da página Checklist com variáveis separadas
    """
    with open('./style/variaveis.css') as vars_file, open('./style/checklist_style.css') as style_file:
        css = f"<style>{vars_file.read()}\n{style_file.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def checklist() -> None:
    """
    Renderiza a interface principal do checklist de tarefas.
    Permite que o usuário marque itens, adicione comentários, envie imagens
    e salve os dados, após validação obrigatória da imagem.
    """
    st.markdown("# Checklist de Tarefas")
    st.markdown("###### Marque os itens concluídos, adicione comentários e carregue a imagem obrigatória.")

    # Verifica se já existe checklist do dia
    if verificar_checklist_hoje():
        st.warning("Você já enviou o checklist hoje. Volte amanhã para um novo.")
        time.sleep(2)
        st.switch_page('./pages/1_Home.py')
        return

    # Carrega os itens de checklist filtrados pelo cargo do usuário
    df_itens = carregar_itens_checklist()

    # Se não houver itens para o cargo, interrompe a execução da página
    if df_itens is None:
        return

    # Renderiza todos os itens e armazena as respostas em uma lista
    respostas = [renderizar_item(row) for _, row in df_itens.iterrows()]

    if st.button("Salvar Checklist", key="btn_salvar"):
        respostas_validas = []
        inconsistentes = []

        for r in respostas:
            feito = r.get("feito", False)
            imagem_path = r.get("imagem_path", "")
            imagem_existe = imagem_path and os.path.exists(imagem_path)

            if feito and imagem_existe:
                respostas_validas.append(r)
            elif feito and not imagem_existe:
                inconsistentes.append(f"Item '{r.get('descricao')}' marcado como feito, mas sem imagem.")
            elif not feito and imagem_existe:
                inconsistentes.append(f"Item '{r.get('descricao')}' tem imagem, mas não foi marcado como feito.")

        if inconsistentes:
            st.warning("Existem inconsistências no checklist:")
            for msg in inconsistentes:
                st.write(f"- {msg}")
        elif not respostas_validas:
            st.warning("Nenhum item válido para salvar.")
        else:
            try:
                salvar_respostas(respostas_validas)

                df_itens = carregar_itens_checklist()
                if df_itens is not None and len(respostas_validas) >= len(df_itens):
                    st.success("Checklist completo salvo com sucesso!")
                    time.sleep(2)
                    st.switch_page('./pages/1_Home.py')
                else:
                    st.success(f"Itens salvos ({len(respostas_validas)}/{len(df_itens)}) - Continue preenchendo o checklist!")
            except Exception as e:
                st.error(f"Erro ao salvar checklist: {e}")




def carregar_itens_checklist() -> pd.DataFrame:
    """
    Carrega os itens de checklist com base no cargo do usuário atual.
    Retorna:
      Um DataFrame filtrado ou None caso não haja itens.
    """
    query = '''SELECT * FROM itens_checklist'''

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

    nome = st.session_state.get("nome", "desconhecido")
    cargo = st.session_state.get("cargo", "").lower()
    hoje = datetime.now().strftime("%Y-%m-%d")


    query = f"""
    SELECT rc.feito, rc.comentario, rc.imagem_path
    FROM respostas_checklist rc
    JOIN funcionarios f ON rc.id_funcionarios = f.id_funcionario
    JOIN itens_checklist ic ON rc.id_itens_checklist = ic.id_itens_checklist
    WHERE f.nome = '{nome}'
    AND LOWER(ic.cargo) = '{cargo}'
    AND DATE(rc.data) = '{hoje}'
    AND rc.id_itens_checklist = '{item_id}'
    """

    resultado = sql_query(query)
    estado_antigo = resultado.iloc[0].to_dict() if not resultado.empty else {}

    with st.expander(row['descricao']):
        # Checkbox para marcar como feito
        feito = st.checkbox(
            "Item concluído",
            value=estado_antigo.get("feito", False),
            key=f"check_{item_id}"
        )

        # Comentário opcional
        comentario = ""
        existe_com = bool(estado_antigo.get("comentario", ""))
        
        if st.checkbox("Adicionar comentário",value=existe_com, key=f"comment_{item_id}"):
            comentario = st.text_area(
                "Comentário",
                value=estado_antigo.get("comentario", ""),
                key=f"input_{item_id}"
            )

        # Se já tem imagem salva, exibe ela
        if estado_antigo.get("imagem_path", ""):
            st.image(estado_antigo["imagem_path"], width=200, caption="Imagem Enviada")
            caminho_arquivo = estado_antigo["imagem_path"]

        # Se não tem, exige upload
        else:
            imagem = st.file_uploader(
                "Carregar imagem (obrigatória)",
                type=["jpg", "png"],
                key=f"image_{item_id}"
            )

            caminho_arquivo = ""
            if imagem is not None:
                data_atual = datetime.now().strftime("%Y-%m-%d")
                pasta_destino = f"./assets/image/{data_atual}/{st.session_state['nome']}-{st.session_state['cargo']}"
                os.makedirs(pasta_destino, exist_ok=True)

                extensao = os.path.splitext(imagem.name)[1]
                nome_arquivo = f"image_{item_id}_{st.session_state['nome']}{extensao}"
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

                with open(caminho_arquivo, "wb") as f:
                    f.write(imagem.read())

        return {
            "id_itens_checklist": item_id,
            "descricao": row['descricao'],
            "feito": feito,
            "comentario": comentario,
            "imagem_path": caminho_arquivo
        }



def main():
    """ Função principal do aplicativo. Garante que o usuário esteja logado antes de exibir a checklist."""
    verifica_login()
    estilizando_pagina()       
    configura_pagina()
    checklist()


if __name__ == "__main__":
    main()