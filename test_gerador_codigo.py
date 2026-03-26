from __future__ import annotations

import pytest

from app import gerar_codigo, validar_parametros


class FakeCursor:
    def __init__(self, fetchone_results: list[tuple]):
        self._fetchone_results = fetchone_results
        self.executed: list[tuple[str, tuple]] = []

    def execute(self, query: str, params: tuple = ()):  # type: ignore[override]
        self.executed.append((query, params))

    def fetchone(self) -> tuple | None:
        if not self._fetchone_results:
            return None
        return self._fetchone_results.pop(0)


def test_gera_codigo_para_grupo_existente_incrementa_sec():
    cursor = FakeCursor(fetchone_results=[(3,), (0,)])
    codigo, sec = gerar_codigo(cursor, grupo="C", tipo_alimento="A", pais="BR")

    assert sec == 4
    assert codigo == "BRC0004A"


def test_gera_codigo_para_grupo_novo_comeca_em_1():
    cursor = FakeCursor(fetchone_results=[(0,), (0,)])
    codigo, sec = gerar_codigo(cursor, grupo="X", tipo_alimento="Z", pais="BR")

    assert sec == 1
    assert codigo == "BRX0001Z"


@pytest.mark.parametrize(
    "sec_atual, esperado",
    [
        (0, "0001"),
        (14, "0015"),
        (99, "0100"),
        (9998, "9999"),
    ],
)
def test_zerofill_quatro_digitos(sec_atual: int, esperado: str):
    cursor = FakeCursor(fetchone_results=[(sec_atual,), (0,)])
    codigo, _ = gerar_codigo(cursor, grupo="A", tipo_alimento="B", pais="BR")

    assert codigo[3:7] == esperado


def test_parametros_invalidos_disparam_value_error():
    with pytest.raises(ValueError):
        validar_parametros("", "A", "BR")

    with pytest.raises(ValueError):
        validar_parametros("C", "", "BR")

    with pytest.raises(ValueError):
        validar_parametros("C", "A", "B")

    with pytest.raises(ValueError):
        validar_parametros("C", "A", "BRA")


def test_parametros_sao_normalizados():
    grupo, tipo, pais = validar_parametros(" c ", " a ", " br ")
    assert grupo == "C"
    assert tipo == "A"
    assert pais == "BR"


def test_gera_codigo_duplicado_dispara_value_error():
    cursor = FakeCursor(fetchone_results=[(3,), (1,)])

    with pytest.raises(ValueError):
        gerar_codigo(cursor, grupo="C", tipo_alimento="A", pais="BR")