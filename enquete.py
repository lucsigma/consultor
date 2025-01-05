

import sqlite3
import streamlit as st

# Função para criar o banco de dados e a tabela
def criar_banco():
    conn = sqlite3.connect('enquete.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            motivo TEXT NOT NULL,
            solucao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar as respostas no banco de dados
def salvar_resposta(nome, motivo, solucao):
    conn = sqlite3.connect('enquete.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO participantes (nome, motivo, solucao)
        VALUES (?, ?, ?)
    ''', (nome, motivo, solucao))
    conn.commit()
    conn.close()

# Função para listar participantes e respostas do banco de dados
def listar_participantes():
    conn = sqlite3.connect('enquete.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, motivo, solucao FROM participantes')
    participantes = cursor.fetchall()
    conn.close()
    return participantes

# Função para excluir um participante com base no ID
def excluir_registro(id_participante):
    conn = sqlite3.connect('enquete.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM participantes WHERE id = ?', (id_participante,))
    conn.commit()
    conn.close()

# Função para verificar se a senha está correta antes de listar participantes ou excluir registros
def verificar_senha(senha_digitada):
    return senha_digitada == "1235"

# Interface Streamlit
st.title("bem vindos a nossa enquete")

# Criar banco de dados na inicialização
criar_banco()

# Solicitar nome
nome = st.text_input("Digite o seu nome:")

if nome:
    st.write(f"Bem-vindo(a), {nome}!")

    # Pergunta sobre discussões
    a = st.radio("Você tem algum motivo recorrente de discussões em seu relacionamento?", ("sim", "não"))

    if a == "sim":
        motivo = st.text_input("Qual seria esse motivo?")
        solucao = st.text_input("Como você tentou resolver?")
        if st.button("Enviar resposta"):
            if motivo and solucao:  # Verificar se motivo e solução foram preenchidos
                salvar_resposta(nome, motivo, solucao)
                st.success("Obrigado por participar da nossa enquete! Vamos analisar sua participação.")
            else:
                st.warning("Por favor, preencha todos os campos antes de enviar.")
    else:
        motivo = "Nenhum"
        solucao = "Nenhuma"
        if st.button("Enviar resposta"):
            salvar_resposta(nome, motivo, solucao)
            st.success("Obrigado por participar da nossa enquete. Desejamos o melhor para você!")

    # Verificar senha para listar participantes
    senha = st.text_input("Digite a senha para listar ou excluir participantes e respostas:", type="password")
    
    if verificar_senha(senha):
        # Listar participantes
        participantes = listar_participantes()
        st.subheader("Lista de Participantes e Respostas")
        for id_participante, nome, motivo, solucao in participantes:
            st.write(f"Nome: {nome}")
            st.write(f"Motivo: {motivo}")
            st.write(f"Solução: {solucao}")
            st.write("-" * 30)
        
        # Opção de excluir registro
        excluir_id = st.number_input("Digite o ID do participante para excluir o registro:", min_value=1, step=1)
        if st.button("Excluir Registro"):
            excluir_registro(excluir_id)
            st.success(f"Registro com ID {excluir_id} excluído com sucesso.")
    else:
        st.warning("Senha incorreta. Acesso negado.")