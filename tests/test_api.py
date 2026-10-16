import sqlite3

import pytest
from fastapi.testclient import TestClient

import api
import load


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    """Cria um banco temporário com 2 linhas e aponta a API para ele"""
    caminho = tmp_path / "teste.db"
    monkeypatch.setattr(load, "CAMINHO_BANCO", caminho)
    monkeypatch.setattr(api, "CAMINHO_BANCO", caminho)

    conexao = sqlite3.connect(caminho)
    load.criar_tabela(conexao)
    conexao.executemany(
        "INSERT INTO clima_diario VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("Salvador", "2026-10-01", 30.0, 24.0, 0.0, 6.0),
            ("Salvador", "2026-10-02", 29.0, 23.0, 2.0, 6.0),
        ],
    )
    conexao.commit()
    conexao.close()
    return TestClient(api.app)


def test_listar_cidades(cliente):
    resposta = cliente.get("/cidades")
    assert resposta.status_code == 200
    assert resposta.json() == ["Salvador"]


def test_clima_da_cidade(cliente):
    resposta = cliente.get("/clima/Salvador")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_busca_ignora_maiusculas(cliente):
    resposta = cliente.get("/clima/salvador")
    assert resposta.status_code == 200


def test_cidade_inexistente_retorna_404(cliente):
    resposta = cliente.get("/clima/Paris")
    assert resposta.status_code == 404


def test_resumo(cliente):
    resposta = cliente.get("/resumo")
    assert resposta.status_code == 200
    assert resposta.json()[0]["media_max"] == 29.5