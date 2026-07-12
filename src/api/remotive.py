import requests

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"


def buscar_vagas(termo: str) -> list[dict]:
    response = requests.get(
        REMOTIVE_API_URL,
        params={"search": termo},
        timeout=10,
    )

    response.raise_for_status()

    dados = response.json()

    return dados["jobs"]