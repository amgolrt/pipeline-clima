from transform import transformar


def dados_exemplo():
    """Resposta falsa da API, no mesmo formato da real"""
    return {
        "cidade": "Teste",
        "daily": {
            "time": ["2026-10-01", "2026-10-02", "2026-10-03"],
            "temperature_2m_max": [30.0, 28.0, None],
            "temperature_2m_min": [20.0, 21.5, 19.0],
            "precipitation_sum": [None, 5.0, 1.0],
        },
    }


def test_colunas_esperadas():
    tabela = transformar(dados_exemplo())
    assert list(tabela.columns) == [
        "cidade", "data", "temp_max", "temp_min", "precipitacao_mm", "amplitude",
    ]


def test_descarta_linha_com_temperatura_nula():
    tabela = transformar(dados_exemplo())
    # A terceira linha tem temp_max nula e deve sair
    assert len(tabela) == 2


def test_precipitacao_nula_vira_zero():
    tabela = transformar(dados_exemplo())
    assert tabela.loc[0, "precipitacao_mm"] == 0


def test_amplitude_calculada():
    tabela = transformar(dados_exemplo())
    assert tabela.loc[0, "amplitude"] == 10.0
    assert tabela.loc[1, "amplitude"] == 6.5