import sqlite3

import pandas as pd

from load import CAMINHO_BANCO

CONSULTAS = {
    "Resumo por cidade": """
        SELECT cidade,
               ROUND(AVG(temp_max), 1) AS media_max,
               ROUND(AVG(temp_min), 1) AS media_min,
               ROUND(SUM(precipitacao_mm), 1) AS chuva_total_mm
        FROM clima_diario
        GROUP BY cidade
        ORDER BY media_max DESC
    """,
    "Dia mais quente de cada cidade": """
        SELECT cidade, data, temp_max
        FROM (
            SELECT cidade, data, temp_max,
                   ROW_NUMBER() OVER (PARTITION BY cidade ORDER BY temp_max DESC) AS posicao
            FROM clima_diario
        )
        WHERE posicao = 1
    """,
    "Média móvel de 3 dias da temperatura máxima": """
        SELECT cidade, data, temp_max,
               ROUND(AVG(temp_max) OVER (
                   PARTITION BY cidade
                   ORDER BY data
                   ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ), 1) AS media_movel_3d
        FROM clima_diario
        ORDER BY cidade, data
    """,
}


if __name__ == "__main__":
    conexao = sqlite3.connect(CAMINHO_BANCO)
    for titulo, sql in CONSULTAS.items():
        print(f"\n=== {titulo} ===")
        print(pd.read_sql_query(sql, conexao).to_string(index=False))
    conexao.close()