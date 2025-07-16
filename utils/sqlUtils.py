# Importando dependencias
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

# O arquivo checklist.db deve estar em 'data/checklist.db'
DB_PATH = "data/checklist.db"
# Criando uma engine
engine = create_engine(f"sqlite:///{DB_PATH}")


def sql_query(query: str) -> pd.DataFrame:
    """
    Executa queries comuns e retorna DataFrame

    Retorna:
        pd.DataFrama: Um DF com os dados da query
    """

    with engine.connect() as conn:
        data = conn.execute(text(query))
        return pd.DataFrame(data.fetchall(), columns=data.keys())


def salvar_respostas(respostas: list) -> None:
    """
    Salva as respostas do checklist em um arquivo JSON.
    Adiciona metadados como nome do funcionário, cargo e data de preenchimento.

    Parâmetros:
        respostas (list): Lista de dicionários com os dados preenchidos.
    """
    # Tenta carregar os dados existentes, ou cria uma nova lista
    nome = st.session_state.get("nome", "desconhecido")
    data_preenchimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Pega o ID do funcionário (assumindo que nomes são únicos por enquanto)
    with engine.begin() as conn:
        result = conn.execute(text("SELECT id_funcionario FROM funcionarios WHERE nome = :nome"), {"nome": nome})
        row = result.fetchone()
        if not row:
            st.error("Funcionário não encontrado no banco de dados.")
            return
        id_funcionario = row[0]

        # Para cada resposta, insere no banco
        for r in respostas:
            conn.execute(text('''
                INSERT INTO respostas_checklist (
                    id_itens_checklist, id_funcionarios, feito, comentario, imagem_path, data
                ) VALUES (
                    :id_itens_checklist, :id_funcionarios, :feito, :comentario, :imagem_path, :data
                )
            '''), {
                "id_itens_checklist": r["id_itens_checklist"],
                "id_funcionarios": id_funcionario,
                "feito": r["feito"],
                "comentario": r["comentario"],
                "imagem_path": r["imagem_path"],
                "data": data_preenchimento
            })


def tabela_funcionarios() -> None:
    """
    Cria a tabela 'funcionarios' com dados default (uma vez)
    """

    query_criacao = '''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(200), 
        cargo VARCHAR(200)
    );
    '''
    # Executa a query
    with engine.begin() as conn:
        conn.execute(text(query_criacao))

        # Verifica se já tem dados
        total = conn.execute(text("SELECT COUNT(*) FROM funcionarios")).scalar()

        if total == 0:
            default_funcionarios = [
                {'nome': 'Alice', 'cargo': 'Gerente de Loja'},
                {'nome': 'Bob', 'cargo': 'Repositor'}
            ]
            # Percorre a lista default
            for pessoa in default_funcionarios:
                conn.execute(text("""
                    INSERT INTO funcionarios (nome, cargo) 
                    VALUES (:nome, :cargo)
                """), pessoa)

def tabela_itens_checklist():
    """
    Cria a tabela 'itens_checklist' com dados default (uma vez)
    """

    query_criacao = '''
    CREATE TABLE IF NOT EXISTS itens_checklist (
        id_itens_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
        cargo VARCHAR(200),
        descricao VARCHAR(2000)
    );
    '''

    # Executa a query
    with engine.begin() as conn:
        conn.execute(text(query_criacao))
        
         # Verifica se já tem dados
        total = conn.execute(text("SELECT COUNT(*) FROM itens_checklist")).scalar()

        if total == 0:
            default_itens_checklist = {
                'Repositor': [
                    "Verificar validade dos produtos nas prateleiras",
                    "Garantir reabastecimento de produtos essenciais",
                    "Limpeza da área de exposição de produtos",
                    "Conferência de etiquetas de preços",
                    "Organização do estoque de fundo"
                ],
                'Gerente de Loja': [
                    "Conferência do fluxo de caixa da abertura",
                    "Checagem das escalas de funcionários do dia",
                    "Verificação de temperaturas de geladeiras/freezers",
                    "Reunião rápida de alinhamento com equipe",
                    "Avaliação geral da limpeza da loja"
                ]
            }

            # Percorre o dicionario com valoroes default
            for cargo, descricoes in default_itens_checklist.items():
                for descricao in descricoes:
                    conn.execute(text("""
                        INSERT INTO itens_checklist (cargo, descricao)
                        VALUES (:cargo, :descricao)
                    """), {"cargo": cargo, "descricao": descricao})

def tabela_respostas_checklist():
    """
    Cria a tabela 'respostas_checklist' (uma vez
    """

    query_criacao = '''
    CREATE TABLE IF NOT EXISTS respostas_checklist (
        id_respostas_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
        id_itens_checklist INTEGER,
        id_funcionarios INTEGER,
        feito BOOLEAN,
        comentario VARCHAR(2000),
        imagem_path VARCHAR(200),
        data DATETIME,
        FOREIGN KEY (id_itens_checklist) REFERENCES itens_checklist(id_itens_checklist),
        FOREIGN KEY (id_funcionarios) REFERENCES funcionarios(id_funcionario)
    );
    '''
    # Executa a query
    with engine.begin() as conn:
        conn.execute(text(query_criacao))

def criar_tabelas():
    """
    Chama todas as funções de criação
    """

    tabela_funcionarios()
    tabela_itens_checklist()
    tabela_respostas_checklist()
