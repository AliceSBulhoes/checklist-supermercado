from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
import os

# 🚨 Conexão direta com o SQLite, sem usar secrets.toml
# O arquivo checklist.db deve estar em 'data/checklist.db'
DB_PATH = "data/checklist.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

def sql_query(query: str):
    """Executa queries comuns e retorna DataFrame"""
    with engine.connect() as conn:
        data = conn.execute(text(query))
        return pd.DataFrame(data.fetchall(), columns=data.keys())

def tabela_funcionarios():
    """Cria a tabela 'funcionarios' com dados default (uma vez)"""
    query_criacao = '''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(200), 
        cargo VARCHAR(200)
    );
    '''
    with engine.begin() as conn:
        conn.execute(text(query_criacao))

        # Verifica se já tem dados
        total = conn.execute(text("SELECT COUNT(*) FROM funcionarios")).scalar()
        if total == 0:
            default_funcionarios = [
                {'nome': 'Alice', 'cargo': 'Gerente de Loja'},
                {'nome': 'Bob', 'cargo': 'Repositor'}
            ]
            for pessoa in default_funcionarios:
                conn.execute(text("""
                    INSERT INTO funcionarios (nome, cargo) 
                    VALUES (:nome, :cargo)
                """), pessoa)

def tabela_itens_checklist():
    """Cria a tabela 'itens_checklist' com dados default (uma vez)"""
    query_criacao = '''
    CREATE TABLE IF NOT EXISTS itens_checklist (
        id_itens_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
        cargo VARCHAR(200),
        descricao VARCHAR(2000)
    );
    '''
    with engine.begin() as conn:
        conn.execute(text(query_criacao))

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

            for cargo, descricoes in default_itens_checklist.items():
                for descricao in descricoes:
                    conn.execute(text("""
                        INSERT INTO itens_checklist (cargo, descricao)
                        VALUES (:cargo, :descricao)
                    """), {"cargo": cargo, "descricao": descricao})

def tabela_respostas_checklist():
    """Cria a tabela 'respostas_checklist' (uma vez)"""
    query_criacao = '''
    CREATE TABLE IF NOT EXISTS respostas_checklist (
        id_respostas_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
        id_itens_checklist INTEGER,
        id_funcionarios INTEGER,
        feito BOOLEAN,
        comentario VARCHAR(2000),
        imagem_path VARCHAR(200),
        FOREIGN KEY (id_itens_checklist) REFERENCES itens_checklist(id_itens_checklist),
        FOREIGN KEY (id_funcionarios) REFERENCES funcionarios(id_funcionario)
    );
    '''
    with engine.begin() as conn:
        conn.execute(text(query_criacao))

def criar_tabelas():
    """Chama todas as funções de criação"""
    tabela_funcionarios()
    tabela_itens_checklist()
    tabela_respostas_checklist()
