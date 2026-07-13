import requests

from models.job import Job


REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"


def converter_vaga(vaga_remotive: dict) -> Job:
    return Job(
        titulo=vaga_remotive["title"],
        empresa=vaga_remotive["company_name"],
        localizacao=vaga_remotive["candidate_required_location"],
        url=vaga_remotive["url"],
        categoria=vaga_remotive.get("category"),
        tipo_contrato=vaga_remotive.get("job_type"),
        data_publicacao=vaga_remotive.get("publication_date"),
        salario=vaga_remotive.get("salary"),
        fonte="remotive",
    )


def buscar_vagas(termo_busca: str) -> list[Job]:
    response = requests.get(
        REMOTIVE_API_URL,
        timeout=10,
    )

    response.raise_for_status()
    dados = response.json()

    vagas = [
        converter_vaga(vaga)
        for vaga in dados["jobs"]
    ]

    termo_normalizado = termo_busca.lower().strip()

    return [
        vaga
        for vaga in vagas
        if termo_normalizado in vaga.titulo.lower()
    ]