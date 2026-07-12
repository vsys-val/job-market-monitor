from api.remotive import buscar_vagas
from models.job import Job


def test_buscar_vagas_retorna_lista_de_jobs(mocker):
    resposta_falsa = mocker.Mock()
    resposta_falsa.json.return_value = {
        "jobs": [
            {
                "title": "Data Analyst",
                "company_name": "Empresa Fictícia",
                "candidate_required_location": "Brasil",
                "url": "https://exemplo.com/vaga",
                "category": "Data",
                "job_type": "full_time",
                "publication_date": "2026-07-12T10:00:00",
                "salary": None,
            }
        ]
    }

    mocker.patch(
        "api.remotive.requests.get",
        return_value=resposta_falsa,
    )

    vagas = buscar_vagas("data")

    assert isinstance(vagas, list)
    assert len(vagas) == 1
    assert isinstance(vagas[0], Job)
    assert vagas[0].titulo == "Data Analyst"
    assert vagas[0].empresa == "Empresa Fictícia"
    assert vagas[0].localizacao == "Brasil"
    assert vagas[0].url == "https://exemplo.com/vaga"
    assert vagas[0].categoria == "Data"
    assert vagas[0].tipo_contrato == "full_time"
    assert vagas[0].data_publicacao == "2026-07-12T10:00:00"
    assert vagas[0].salario is None
    assert vagas[0].fonte == "remotive"