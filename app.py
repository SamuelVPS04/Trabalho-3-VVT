from __future__ import annotations

from typing import Optional, Tuple

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


def conectar_mysql(host: str, user: str, password: str, database: str) -> MySQLConnection:
    # Cria e retorna uma conexão com o banco MySQL.
    # Conecta ao banco com autocommit desabilitado para controlar transações manualmente
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        autocommit=False,
    )


def validar_parametros(grupo: str, tipo_alimento: str, pais: str) -> None:
    # Valida os parâmetros utilizados para gerar o código do produto.

    # Grupo deve ter exatamente 1 caractere
    if not grupo or len(grupo.strip()) != 1:
        raise ValueError("O parâmetro 'grupo' deve ser 1 caractere não vazio.")

    # Tipo de alimento deve ter exatamente 1 caractere
    if not tipo_alimento or len(tipo_alimento.strip()) != 1:
        raise ValueError("O parâmetro 'tipo_alimento' deve ser 1 caractere não vazio.")

    # País deve ter exatamente 2 caracteres
    if not pais or len(pais.strip()) != 2:
        raise ValueError("O parâmetro 'pais' deve conter exatamente 2 caracteres.")


def gerar_codigo(cursor: MySQLCursor, grupo: str, tipo_alimento: str, pais: str) -> Tuple[str, int]:
    # Gera o código do produto e calcula o próximo valor de sec para o grupo.

    # Valida parâmetros de entrada antes de acessar o banco
    validar_parametros(grupo, tipo_alimento, pais)

    # 1) Busca o maior sec já usado para o grupo
    cursor.execute(
        "SELECT MAX(sec) FROM produtos WHERE Grupo = %s", (grupo,)
    )
    row = cursor.fetchone()
    maior_sec: Optional[int] = None
    if row:
        maior_sec = row[0]

    # 2) Calcula o novo valor de sec
    sec = 1 if not maior_sec else (maior_sec + 1)

    # 3) Formata com 4 dígitos (zerofill)
    sec_str = f"{sec:04d}"

    # 4) Monta o código final
    codigo = f"{pais}{grupo}{sec_str}{tipo_alimento}"

    # 5) Verifica duplicidade (garantir que não existe código igual já inserido)
    cursor.execute("SELECT COUNT(1) FROM produtos WHERE codigo = %s", (codigo,))
    count_row = cursor.fetchone()
    if count_row and count_row[0] and int(count_row[0]) > 0:
        raise ValueError(f"Código já existe: {codigo}")

    return codigo, sec


def inserir_produto(
    conn: MySQLConnection, grupo: str, tipo_alimento: str, pais: str
) -> Tuple[int, str]:
    # Insere um novo produto no banco usando o código gerado automaticamente.

    cursor = conn.cursor()
    try:
        # Gera código e sec antes de inserir
        codigo, sec = gerar_codigo(cursor, grupo, tipo_alimento, pais)

        # Insere novo registro utilizando o código gerado
        cursor.execute(
            "INSERT INTO produtos (codigo, sec, Grupo, Tipo_Alimento, Pais) VALUES (%s, %s, %s, %s, %s)",
            (codigo, sec, grupo, tipo_alimento, pais),
        )

        # Confirma a transação e retorna o id gerado
        conn.commit()
        inserted_id = cursor.lastrowid
        return inserted_id, codigo
    except Exception:
        # Volta a transação em caso de erro
        conn.rollback()
        raise
    finally:
        cursor.close()


def listar_produtos(conn: MySQLConnection) -> list[tuple]:
    # Retorna todos os produtos cadastrados (apenas para consulta).

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, codigo, sec, Grupo, Tipo_Alimento, Pais FROM produtos ORDER BY id")
        return cursor.fetchall()
    finally:
        cursor.close()


if __name__ == "__main__":
    # Exemplo de uso rápido (ajuste as credenciais conforme necessário)
    import os

    host = os.environ.get("MYSQL_HOST", "localhost")
    user = os.environ.get("MYSQL_USER", "root")
    password = os.environ.get("MYSQL_PASSWORD", "")
    database = os.environ.get("MYSQL_DATABASE", "db_produtos")

    conn = conectar_mysql(host, user, password, database)
    try:
        inserted_id, codigo = inserir_produto(conn, grupo="C", tipo_alimento="A", pais="BR")
        print(f"Inserido id={inserted_id} com código {codigo}")

        # Exemplo de consulta (SELECT) para verificar dados existentes
        produtos = listar_produtos(conn)
        print("\nProdutos cadastrados:")
        for p in produtos:
            print(p)
    finally:
        conn.close()
