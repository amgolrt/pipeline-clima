import pandas as pd

from extract import CIDADES, buscar_clima
from transform import transformar


def rodar():
    tabelas = []
    for nome, (lat, lon) in CIDADES.items():
        bruto = buscar_clima(nome, lat, lon)
        tabelas.append(transformar(bruto))

    resultado = pd.concat(tabelas, ignore_index=True)
    return resultado


if __name__ == "__main__":
    df = rodar()
    print(df.head(10))
    print()
    print(df.info())