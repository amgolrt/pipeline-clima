import pandas as pd


def transformar(dados):
    """Converte a resposta da API em uma tabela limpa (uma linha por dia)"""
    diario = dados["daily"]

    tabela = pd.DataFrame(
        {
            "cidade": dados["cidade"],
            "data": pd.to_datetime(diario["time"]),
            "temp_max": diario["temperature_2m_max"],
            "temp_min": diario["temperature_2m_min"],
            "precipitacao_mm": diario["precipitation_sum"],
        }
    )

    # Limpeza: a API pode devolver valores nulos; precipitação nula vira 0
    tabela["precipitacao_mm"] = tabela["precipitacao_mm"].fillna(0)
    tabela = tabela.dropna(subset=["temp_max", "temp_min"])

    # Coluna derivada: amplitude térmica do dia
    tabela["amplitude"] = (tabela["temp_max"] - tabela["temp_min"]).round(1)

    return tabela