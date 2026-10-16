# Pipeline de Clima

Pipeline de dados de ponta a ponta: coleta o clima diário de várias cidades em uma API pública, trata os dados com Pandas, grava em um banco SQLite e expõe os resultados por uma API REST. O projeto inclui consultas SQL analíticas e testes automatizados.

## Visão geral

```
Open-Meteo API  ->  extract  ->  transform  ->  load  ->  SQLite  ->  API REST (FastAPI)
```

- **Extract**: consome a API pública [Open-Meteo](https://open-meteo.com/) (gratuita, sem chave) e busca os últimos 7 dias de cada cidade.
- **Transform**: converte o JSON aninhado em uma tabela limpa, trata valores nulos e cria a coluna derivada `amplitude` (temperatura máxima menos mínima).
- **Load**: grava no SQLite de forma **idempotente**. A chave primária (`cidade`, `data`) com `INSERT OR REPLACE` garante que rodar o pipeline várias vezes não duplica dados.
- **Consultas**: SQL analítico com `GROUP BY` e *window functions* (`ROW_NUMBER`, média móvel).
- **API**: endpoints REST que leem o banco, com tratamento de erro (404) e documentação automática.

## Tecnologias

Python, Pandas, Requests, SQLite, SQL, FastAPI, Uvicorn, Pytest.

## Estrutura do projeto

```
pipeline-clima/
├── src/
│   ├── extract.py      # coleta de dados na API
│   ├── transform.py    # limpeza e padronização com Pandas
│   ├── load.py         # criação da tabela e carga no SQLite
│   ├── pipeline.py     # orquestra extract -> transform -> load
│   ├── consultas.py    # consultas SQL analíticas
│   ├── api.py          # API REST com FastAPI
│   └── cliente.py      # exemplo de consumo da API
├── tests/
│   ├── test_transform.py
│   └── test_api.py
├── data/               # banco clima.db (gerado ao rodar, não versionado)
├── pytest.ini
├── requirements.txt
└── README.md
```

## Como executar

Pré-requisito: Python 3.10 ou superior.

**1. Clonar e criar o ambiente virtual**

```bash
git clone https://github.com/SEU-USUARIO/pipeline-clima.git
cd pipeline-clima
python -m venv .venv
```

Ativar o ambiente:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

**2. Instalar as dependências**

```bash
python -m pip install -r requirements.txt
```

**3. Rodar o pipeline** (cria e preenche o banco em `data/clima.db`)

```bash
python src/pipeline.py
```

**4. Rodar as consultas SQL**

```bash
python src/consultas.py
```

**5. Subir a API**

```bash
uvicorn api:app --reload --app-dir src
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Endpoints

| Método | Rota                | Descrição                                         |
|--------|---------------------|---------------------------------------------------|
| GET    | `/cidades`          | Lista as cidades disponíveis no banco             |
| GET    | `/clima/{cidade}`   | Clima diário de uma cidade (404 se não existir)   |
| GET    | `/resumo`           | Médias de temperatura e chuva total por cidade    |

Exemplo:

```bash
curl http://127.0.0.1:8000/clima/Salvador
```

## Testes

```bash
python -m pytest -v
```

- `test_transform.py`: testa a transformação com dados falsos (colunas, tratamento de nulos, cálculo da amplitude), sem depender de internet.
- `test_api.py`: testa os endpoints usando um banco temporário, sem tocar no `clima.db` real.

## Decisões de projeto

- **Idempotência**: o pipeline pode ser executado quantas vezes for preciso sem duplicar registros.
- **Separação de camadas**: o pipeline produz os dados; consultas e API apenas os consomem.
- **SQL parametrizado**: valores recebidos pela API entram na consulta via parâmetros (`?`), evitando SQL injection.
- **Testes isolados**: dados simulados e banco temporário tornam os testes rápidos e independentes da rede.
