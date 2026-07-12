import requests

from models.job import Job


REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"


def converter_vaga(vaga_remotive: dict) -> Job:
    return Job(
        titulo=vaga_remotive["title"],
        empresa=vaga_remotive["company_name"],
        localizacao=vaga_remotive["candidate_required_location"],
        url=vaga_remotive["url"],
    )


def buscar_vagas(termo_busca: str) -> list[Job]:
    response = requests.get(
        REMOTIVE_API_URL,
        params={"search": termo_busca},
        timeout=10,
    )

    response.raise_for_status()
    dados = response.json()

    return [converter_vaga(vaga) for vaga in dados["jobs"]]
    