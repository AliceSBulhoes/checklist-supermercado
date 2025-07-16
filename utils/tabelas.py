from sqlalchemy import create_engine, inspect, text
import streamlit as st
import pandas as pd

CONN = st.connection('checklist_db', type='sql')

def sql_query(query: str):
    """Executa a querry comum"""

    with CONN.session as s:
        data = s.execute(text(query))

        return pd.DataFrame(data)

def tabela_funcionarios():
    """
    Função para criar tabela 'funcionarios' com dados default (apenas uma vez)
    """
    # Query para criar a tabela
    query_criacao = '''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(200), 
        cargo VARCHAR(200)
    );
    '''

    with CONN.session as s:
        # Cria a tabela se não existir
        s.execute(text(query_criacao))

        # Verifica se já tem dados
        resultado = s.execute(text("SELECT COUNT(*) FROM funcionarios;"))
        total = resultado.scalar()

        if total == 0:
            default_funcionarios = {
                1: {'nome': 'Alice', 'cargo': 'Gerente de Loja'},
                2: {'nome': 'Bob', 'cargo': 'Repositor'}
            }

            # Percorre todas as tabelas
            for pessoa in default_funcionarios.values():
                insert_query = text("INSERT INTO funcionarios (nome, cargo) VALUES (:nome, :cargo)")
                s.execute(insert_query, params=pessoa)

        s.commit()


def tabela_itens_checklist():
    """
    Função para criar tabela 'itens_checklist' com dados default (apenas uma vez)
    """
    query_criacao = '''
    CREATE TABLE IF NOT EXISTS itens_checklist (
        id_itens_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
        cargo VARCHAR(200),
        descricao VARCHAR(2000)
    );
    '''

    with CONN.session as s:
        # Cria a tabela se não existir
        s.execute(text(query_criacao))

        # Verifica se a tabela já tem dados
        resultado = s.execute(text("SELECT COUNT(*) FROM itens_checklist;"))
        total = resultado.scalar()

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

            # Insere cada item com seu respectivo cargo
            for cargo, descricoes in default_itens_checklist.items():
                for descricao in descricoes:
                    insert_query = text("""
                        INSERT INTO itens_checklist (cargo, descricao)
                        VALUES (:cargo, :descricao)
                    """)
                    s.execute(insert_query, params={"cargo": cargo, "descricao": descricao})

        s.commit()

def tabela_respostas_checklist():
    """
    Função para criar tabela 'respostas_checklist' (apenas uma vez)
    """
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

    with CONN.session as s:
        s.execute(text(query_criacao))
        s.commit()



def criar_tabelas():
    """Criação das tabelas"""
    tabela_funcionarios()
    tabela_itens_checklist()
    tabela_respostas_checklist()



