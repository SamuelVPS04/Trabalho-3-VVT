from __future__ import annotations

import pytest

from app import buscar_por_codigo, conectar_mysql, inserir_codigo, listar_codigos


@pytest.fixture
def conn():
    try:
        connection = conectar_mysql()
    except Exception as exc:
        pytest.skip(f"MySQL não disponível para teste de integração: {exc}")

    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def limpar_dados_teste(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM codigos_sequenciais WHERE Pais = 'ZZ'")
    conn.commit()
    cursor.close()


def test_conexao_python_mysql(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()
    cursor.close()

    assert resultado == (1,)


def test_insercao_real_e_query_de_validacao(conn):
    inserted_id, codigo, sec = inserir_codigo(conn, grupo="Z", tipo_alimento="A", pais="ZZ")

    assert inserted_id is not None
    assert sec == 1
    assert codigo == "ZZZ0001A"

    registro = buscar_por_codigo(conn, codigo)
    assert registro is not None
    assert registro[1] == "ZZZ0001A"
    assert registro[2] == 1
    assert registro[3] == "Z"
    assert registro[4] == "A"
    assert registro[5] == "ZZ"


def test_incremento_real_do_sec_no_mesmo_grupo(conn):
    _, codigo1, sec1 = inserir_codigo(conn, grupo="Z", tipo_alimento="A", pais="ZZ")
    _, codigo2, sec2 = inserir_codigo(conn, grupo="Z", tipo_alimento="B", pais="ZZ")

    assert codigo1 == "ZZZ0001A"
    assert codigo2 == "ZZZ0002B"
    assert sec1 == 1
    assert sec2 == 2


def test_listagem_retorna_dados(conn):
    inserir_codigo(conn, grupo="Z", tipo_alimento="A", pais="ZZ")
    registros = listar_codigos(conn)

    assert isinstance(registros, list)
    assert len(registros) > 0


def test_entrada_invalida_em_integracao(conn):
    with pytest.raises(ValueError):
        inserir_codigo(conn, grupo="", tipo_alimento="A", pais="ZZ")