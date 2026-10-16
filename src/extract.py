import requests

URL = "https://api.open-meteo.com/v1/forecast"

# Acrescentar novas cidades: nome -> (latitude, longitude)
CIDADES = {
    "Salvador": (-12.97, -38.50),
    "Itabuna": (-14.78, -39.27),
    "Sao Paulo": (-23.55, -46.63),
}


def buscar_clima(cidade, latitude, longitude):
    """Busca o clima diário dos últimos 7 dias de uma cidade."""
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "America/Sao_Paulo",
    }
    resposta = requests.get(URL, params=parametros, timeout=30)
    resposta.raise_for_status()
    dados = resposta.json()
    dados["cidade"] = cidade
    return dados


if __name__ == "__main__":
    for nome, (lat, lon) in CIDADES.items():
        resultado = buscar_clima(nome, lat, lon)
        print(nome, resultado["daily"]["time"][:2], resultado["daily"]["temperature_2m_max"][:2])