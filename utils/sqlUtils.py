# Importando dependencias
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import os
import shutil

import os
import shutil

# Caminho original do banco no projeto
ORIGINAL_DB_PATH = os.path.join(os.getcwd(), "checklist.db")

# Verifica se está no Streamlit Cloud
is_streamlit_cloud = os.environ.get("STREAMLIT_ENV") == "cloud" or "HOME" in os.environ and "/home/appuser" in os.environ.get("HOME", "")

# Define caminho correto com base no ambiente
if is_streamlit_cloud:
    TEMP_DB_PATH = "/tmp/checklist.db"
    # Copia para /tmp se necessário
    if not os.path.exists(TEMP_DB_PATH):
        shutil.copy(ORIGINAL_DB_PATH, TEMP_DB_PATH)
    DB_PATH = TEMP_DB_PATH
else:
    # No local, usa o original mesmo
    DB_PATH = ORIGINAL_DB_PATH

# Agora sim cria a engine com o caminho certo
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

# Garante que o arquivo existe
if not os.path.exists(DB_PATH):
    open(DB_PATH, 'w').close()

def excluir_diario(query: str) -> None:
    """
    Função para excluir registro diário para desenvolvimento
    """
    hoje = datetime.now().strftime("%Y-%m-%d")

    with engine.begin() as conn:
        conn.execute(text(query), {'hoje' : hoje})


def sql_query(query: str) -> pd.DataFrame:
    """
    Executa queries comuns e retorna DataFrame

    Retorna:
        pd.DataFrama: Um DF com os dados da query
    """
    with engine.connect() as conn:
        data = conn.execute(text(query))
        return pd.DataFrame(data.fetchall(), columns=data.keys())

def verificar_checklist_hoje() -> bool:
    """
    Verifica se o usuário já enviou um checklist completo hoje
    
    Retorna:
        bool: True se já enviou todos os itens hoje, False caso contrário
    """
    nome = st.session_state.get("nome", "desconhecido")
    cargo = st.session_state.get("cargo", "").lower()
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    # Query para contar itens do cargo
    query_itens_cargo = """
    SELECT COUNT(*) 
    FROM itens_checklist 
    WHERE LOWER(cargo) = :cargo
    """
    
    # Query para contar respostas do usuário hoje
    query_respostas_hoje = """
    SELECT COUNT(*) 
    FROM respostas_checklist rc
    JOIN funcionarios f ON rc.id_funcionarios = f.id_funcionario
    JOIN itens_checklist ic ON rc.id_itens_checklist = ic.id_itens_checklist
    WHERE f.nome = :nome 
    AND LOWER(ic.cargo) = :cargo
    AND DATE(rc.data) = :hoje
    """
    
    with engine.connect() as conn:
        # Total de itens do cargo
        total_itens = conn.execute(
            text(query_itens_cargo), 
            {"cargo": cargo}
        ).scalar()
        
        # Respostas do usuário hoje
        respostas_hoje = conn.execute(
            text(query_respostas_hoje),
            {"nome": nome, "cargo": cargo, "hoje": hoje}
        ).scalar()
        
    return respostas_hoje >= total_itens if total_itens > 0 else False


def salvar_respostas(respostas: list) -> None:
    """
    Salva as respostas do checklist no banco de dados.
    Atualiza respostas existentes ou insere novas.
    """
    nome = st.session_state.get("nome", "desconhecido")
    data_preenchimento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with engine.begin() as conn:
        # Pega o ID do funcionário
        result = conn.execute(
            text("SELECT id_funcionario FROM funcionarios WHERE nome = :nome"), 
            {"nome": nome}
        )
        row = result.fetchone()
        if not row:
            raise Exception("Funcionário não encontrado no banco de dados")
        id_funcionario = row[0]

        # Para cada resposta, verifica se já existe e atualiza/insere
        for r in respostas:
            # Verifica se já existe resposta para este item hoje
            check_query = """
            SELECT id_respostas_checklist 
            FROM respostas_checklist 
            WHERE id_itens_checklist = :item_id 
            AND id_funcionarios = :func_id 
            AND DATE(data) = DATE(:data)
            """
            result = conn.execute(text(check_query), {
                "item_id": r["id_itens_checklist"],
                "func_id": id_funcionario,
                "data": data_preenchimento
            })
            existing = result.fetchone()
            
            if existing:
                # Atualiza resposta existente
                conn.execute(text('''
                    UPDATE respostas_checklist
                    SET feito = :feito,
                        comentario = :comentario,
                        imagem_path = :imagem_path,
                        data = :data
                    WHERE id_respostas_checklist = :id
                '''), {
                    "id": existing[0],
                    "feito": r["feito"],
                    "comentario": r["comentario"],
                    "imagem_path": r["imagem_path"],
                    "data": data_preenchimento
                })
            else:
                # Insere nova resposta
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
