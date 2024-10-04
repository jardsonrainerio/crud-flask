# db.py
import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Criação da tabela cliente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cliente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT
            )
        ''')
        # Criação da tabela fornecedor
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fornecedor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                produto TEXT,
                contato TEXT
            )
        ''')
        conn.commit()

import atexit
from flask import Flask

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Registro do fechamento da conexão ao final da aplicação
atexit.register(close_connection)
