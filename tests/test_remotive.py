from api.remotive import buscar_vagas


def test_buscar_vagas_retorna_lista(mocker):
    resposta_falsa = mocker.Mock()
    resposta_falsa.json.return_value = {
        "jobs": [
            {
                "title": "Data Analyst",
                "company_name": "Empresa Fictícia",
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
    assert vagas[0]["title"] == "Data Analyst"