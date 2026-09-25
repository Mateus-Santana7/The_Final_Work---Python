import sqlite3
import pandas as pd

NOME_BANCO = "clinica.db"

def conectar():
    return sqlite3.connect(NOME_BANCO, check_same_thread=False)

def criar_tabela():
    conexao = conectar()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS consultas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            medico TEXT NOT NULL,
            valor_consulta REAL NOT NULL,
            data TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def inserir_consulta(paciente, especialidade, medico, valor_consulta, data):
    conexao = conectar()
    conexao.execute(
        """
        INSERT INTO consultas (paciente, especialidade, medico, valor_consulta, data)
        VALUES (?, ?, ?, ?, ?)
        """,
        (paciente, especialidade, medico, valor_consulta, data)
    )
    conexao.commit()
    conexao.close()

def listar_consultas():
    conexao = conectar()
    df = pd.read_sql_query("SELECT * FROM consultas ORDER BY id DESC", conexao)
    conexao.close()
    return df

def excluir_consulta(id_consulta):
    conexao = conectar()
    conexao.execute("DELETE FROM consultas WHERE id = ?", (id_consulta,))
    conexao.commit()
    conexao.close()