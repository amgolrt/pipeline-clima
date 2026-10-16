import sqlite3
from pathlib import Path

# O banco fica em pipeline-clima/data/clima.db
CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "data" / "clima.db"


def conectar():
    CAMINHO_BANCO.parent.mkdir(exist_ok=True)
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela(conexao):
    # A chave primária (cidade + data) impede duas linhas para o mesmo dia
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS clima_diario (
            cidade TEXT NOT NULL,
            data TEXT NOT NULL,
            temp_max REAL,
            temp_min REAL,
            precipitacao_mm REAL,
            amplitude REAL,
            PRIMARY KEY (cidade, data)
        )
        """
    )


def carregar(df):
    """Grava o DataFrame no banco. Rodar de novo atualiza, sem duplicar"""
    colunas = ["cidade", "data", "temp_max", "temp_min", "precipitacao_mm", "amplitude"]
    registros = df.assign(data=df["data"].dt.strftime("%Y-%m-%d"))
    linhas = list(registros[colunas].itertuples(index=False, name=None))

    conexao = conectar()
    criar_tabela(conexao)
    conexao.executemany(
        "INSERT OR REPLACE INTO clima_diario VALUES (?, ?, ?, ?, ?, ?)", linhas
    )
    conexao.commit()
    conexao.close()
    return len(linhas)