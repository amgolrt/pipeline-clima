import sqlite3

from fastapi import FastAPI, HTTPException

from load import CAMINHO_BANCO

app = FastAPI(title="API de Clima", description="Consulta os dados do pipeline de clima.")


def consultar(sql, parametros=()):
    """Executa uma consulta no SQLite e devolve uma lista de dicionários"""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    try:
        linhas = conexao.execute(sql, parametros).fetchall()
    finally:
        conexao.close()
    return [dict(linha) for linha in linhas]


@app.get("/cidades")
def listar_cidades():
    """Lista as cidades disponíveis no banco"""
    linhas = consultar("SELECT DISTINCT cidade FROM clima_diario ORDER BY cidade")
    return [linha["cidade"] for linha in linhas]


@app.get("/clima/{cidade}")
def clima_da_cidade(cidade: str):
    """Devolve o clima diário de uma cidade"""
    linhas = consultar(
        """
        SELECT cidade, data, temp_max, temp_min, precipitacao_mm, amplitude
        FROM clima_diario
        WHERE LOWER(cidade) = LOWER(?)
        ORDER BY data
        """,
        (cidade,),
    )
    if not linhas:
        raise HTTPException(status_code=404, detail=f"Cidade '{cidade}' não encontrada.")
    return linhas


@app.get("/resumo")
def resumo():
    """Devolve médias de temperatura e chuva total por cidade"""
    return consultar(
        """
        SELECT cidade,
               ROUND(AVG(temp_max), 1) AS media_max,
               ROUND(AVG(temp_min), 1) AS media_min,
               ROUND(SUM(precipitacao_mm), 1) AS chuva_total_mm
        FROM clima_diario
        GROUP BY cidade
        ORDER BY media_max DESC
        """
    )