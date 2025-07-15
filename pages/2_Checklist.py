import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import time

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
        erros = validar_respostas(respostas)

        if erros:
            # Mostra os erros encontrados na validação
            # for erro in erros:
            #     st.error(erro)
            st.warning("Preencha todos os campos obrigatórios antes de salvar.")
        else:
            salvar_respostas(respostas)
            st.success("Checklist salvo com sucesso!")
            time.sleep(2)
            st.switch_page('./pages/1_Home.py')


def carregar_itens_checklist() -> pd.DataFrame:
    """
    Carrega os itens de checklist com base no cargo do usuário atual.
    Retorna:
      Um DataFrame filtrado ou None caso não haja itens.
    """
    df = pd.read_json('data/itens_checklist.json')
    cargo = st.session_state.get('cargo', '').lower()

    # Filtra os itens que correspondem ao cargo do usuário
    df_filtrado = df[df['cargo'].str.lower() == cargo]
    return df_filtrado if not df_filtrado.empty else None


def renderizar_item(row: pd.Series) -> dict:
    """
    Renderiza um único item do checklist com opções interativas.
    Parâmetros:
        row (pd.Series): Linha do DataFrame com os dados do item.

    Retorna:
        dict: Respostas preenchidas pelo usuário (marcado, comentário, imagem, etc.).
    """
    with st.expander(row['descricao']):
        # Checkbox para marcar o item como concluído
        marcado = st.checkbox("Item concluído", key=f"check_{row['id_itens_checklist']}")

        # Campo opcional de comentário
        comentario = ""
        if st.checkbox("Adicionar comentário", key=f"comment_{row['id_itens_checklist']}"):
            comentario = st.text_area("Comentário", key=f"input_{row['id_itens_checklist']}")

        # Upload obrigatório de imagem
        imagem = st.file_uploader(
            "Carregar imagem (obrigatória)",
            type=["jpg", "jpeg", "png"],
            key=f"image_{row['id_itens_checklist']}"
        )
        
        # Definindo variáveis
        pasta_destino = ""
        nome_arquivo = ""

        # Verefica se há uma imagem
        if imagem is not None:
            # Define o diretório onde será salvo
            pasta_destino = f"assets/image/{st.session_state['nome']}-{st.session_state['cargo']}"
            os.makedirs(pasta_destino, exist_ok=True)

            # Extrai a extensão do arquivo original
            extensao = os.path.splitext(imagem.name)[1]  # .jpg, .png, etc.

            # Define o nome do arquivo com extensão
            nome_arquivo = f"image_{row['id_itens_checklist']}_{st.session_state['nome']}{extensao}"

            # Caminho completo do arquivo no disco
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

            # Salva a imagem no diretório desejado
            with open(caminho_arquivo, "wb") as f:
                f.write(imagem.read())

        return {
            "id_itens_checklist": row['id_itens_checklist'],
            "descricao": row['descricao'],
            "marcado": marcado,
            "comentario": comentario,
            "imagem_path": f"./{pasta_destino}/{nome_arquivo}"
        }


def validar_respostas(respostas: list) -> list:
    """
    Valida se TODOS os itens foram:
    - Marcados como concluídos
    - E possuem imagem de fato salva no disco

    Retorna:
        list: Uma única mensagem de erro, caso alguma condição falhe.
    """
    for r in respostas:
        # Verifica se o item foi marcado
        if not r['marcado']:
            return ["Todos os itens devem estar marcados como concluídos e conter uma imagem obrigatória."]
        
        # Verifica se a imagem foi realmente salva
        imagem_path = r.get("imagem_path", "")
        if not imagem_path or imagem_path.endswith("/") or not os.path.exists(imagem_path):
            return ["Todos os itens devem estar marcados como concluídos e conter uma imagem obrigatória."]
    
    return []



def salvar_respostas(respostas: list) -> None:
    """
    Salva as respostas do checklist em um arquivo JSON.
    Adiciona metadados como nome do funcionário, cargo e data de preenchimento.

    Parâmetros:
        respostas (list): Lista de dicionários com os dados preenchidos.
    """
    # Tenta carregar os dados existentes, ou cria uma nova lista
    try:
        with open("data/respostas_checklist.json", "r", encoding="utf-8") as f:
            dados_existentes = json.load(f)
            if not isinstance(dados_existentes, list):
                dados_existentes = []
    except (FileNotFoundError, json.JSONDecodeError):
        dados_existentes = []

    # Coleta dados extras do usuário para salvar junto com cada item
    nome_funcionario = st.session_state.get("nome", "desconhecido")
    cargo_funcionario = st.session_state.get("cargo", "desconhecido")
    data_preenchimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for r in respostas:
        dados_existentes.append({
            "id": len(dados_existentes) + 1,
            "nome_funcionario": nome_funcionario,
            "cargo_funcionario": cargo_funcionario,
            "data_preenchimento": data_preenchimento,
            "id_itens_checklist": r["id_itens_checklist"],
            "marcado": r["marcado"],
            "comentario": r["comentario"],
            "imagem_path": r["imagem_path"]
        })

    # Salva todos os dados novamente no arquivo
    with open("data/respostas_checklist.json", "w", encoding="utf-8") as f:
        json.dump(dados_existentes, f, indent=4, ensure_ascii=False)


def main():
    """ Função principal do aplicativo. Garante que o usuário esteja logado antes de exibir a checklist."""
    configura_pagina()
    if st.session_state.get('logged_in'):
        checklist()
    else:
        st.switch_page("./app.py")


if __name__ == "__main__":
    main()
