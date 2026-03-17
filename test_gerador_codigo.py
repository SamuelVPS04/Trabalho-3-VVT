from __future__ import annotations

import pytest

from app import gerar_codigo


class FakeCursor:
    def __init__(self, fetchone_results: list[tuple]):
        # Lista de tuplas que serão retornadas em chamadas sucessivas a fetchone()
        self._fetchone_results = fetchone_results
        self.executed: list[tuple[str, tuple]] = []

    def execute(self, query: str, params: tuple = ()):  # type: ignore[override]
        self.executed.append((query, params))

    def fetchone(self) -> tuple | None:
        if not self._fetchone_results:
            return None
        return self._fetchone_results.pop(0)


def test_gera_codigo_para_grupo_existente_incrementa_sec():
    # Quando já existe sec=3 para o grupo, o próximo deve ser 4.
    cursor = FakeCursor(fetchone_results=[(3,), (0,)])
    codigo, sec = gerar_codigo(cursor, grupo="C", tipo_alimento="A", pais="BR")

    assert sec == 4
    assert codigo == "BRC0004A"


def test_gera_codigo_para_grupo_novo_comeca_em_1():
    # Quando não há registros para o grupo, MAX(sec) retorna NULL.
    cursor = FakeCursor(fetchone_results=[(None,), (0,)])
    codigo, sec = gerar_codigo(cursor, grupo="X", tipo_alimento="Z", pais="BR")

    assert sec == 1
    assert codigo == "BRX0001Z"


@pytest.mark.parametrize(
    "sec, expected",
    [
        (1, "0001"),
        (15, "0015"),
        (100, "0100"),
        (9999, "9999"),
    ],
)
def test_zerofill_quatro_digitos(sec: int, expected: str):
    cursor = FakeCursor(fetchone_results=[(sec - 1,), (0,)])
    codigo, _ = gerar_codigo(cursor, grupo="A", tipo_alimento="B", pais="BR")

    assert codigo[3:7] == expected


def test_entrada_invalida_gera_value_error():
    cursor = FakeCursor(fetchone_results=[(None,), (0,)])

    with pytest.raises(ValueError):
        gerar_codigo(cursor, grupo="", tipo_alimento="A", pais="BR")

    with pytest.raises(ValueError):
        gerar_codigo(cursor, grupo="C", tipo_alimento="", pais="BR")

    with pytest.raises(ValueError):
        gerar_codigo(cursor, grupo="C", tipo_alimento="A", pais="B")

    with pytest.raises(ValueError):
        gerar_codigo(cursor, grupo="C", tipo_alimento="A", pais="BRA")


def test_gera_codigo_duplicado_gera_value_error():
    # Simula que o SELECT COUNT retorna 1 para o código gerado.
    cursor = FakeCursor(fetchone_results=[(1,), (1,)])

    with pytest.raises(ValueError):
        gerar_codigo(cursor, grupo="C", tipo_alimento="A", pais="BR")
