import requests
import logging

from api.himalayas import converter_vaga, formatar_localizacoes
from models.job import Job
from main import coletar_vagas

def test_formatar_localizacoes_com_strings():
    localizacoes = ["Brazil", "Portugal"]

    resultado = formatar_localizacoes(localizacoes)

    assert resultado == "Brazil, Portugal"


def test_formatar_localizacoes_com_dicionarios():
    localizacoes = [
        {"name": "Brazil"},
        {"name": "Portugal"},
    ]

    resultado = formatar_localizacoes(localizacoes)

    assert resultado == "Brazil, Portugal"


def test_formatar_localizacoes_vazias():
    resultado = formatar_localizacoes([])

    assert resultado == "Worldwide"


def test_converter_vaga_himalayas_retorna_job():
    vaga_himalayas = {
        "title": "Data Analyst",
        "companyName": "Empresa Teste",
        "locationRestrictions": ["Brazil"],
        "applicationLink": "https://exemplo.com/vaga",
        "categories": ["Data", "Analytics"],
        "employmentType": "Full Time",
        "pubDate": "2026-07-14",
        "minSalary": 4000,
        "maxSalary": 6000,
        "currency": "USD",
    }

    vaga = converter_vaga(vaga_himalayas)

    assert isinstance(vaga, Job)
    assert vaga.titulo == "Data Analyst"
    assert vaga.empresa == "Empresa Teste"
    assert vaga.localizacao == "Brazil"
    assert vaga.url == "https://exemplo.com/vaga"
    assert vaga.categoria == "Data, Analytics"
    assert vaga.tipo_contrato == "Full Time"
    assert vaga.data_publicacao == "2026-07-14"
    assert vaga.salario == "USD 4000 - 6000"
    assert vaga.fonte == "himalayas"


def test_converter_vaga_sem_salario():
    vaga_himalayas = {
        "title": "BI Analyst",
        "companyName": "Empresa Teste",
        "locationRestrictions": [],
        "applicationLink": "https://exemplo.com/bi",
        "categories": [],
        "employmentType": None,
        "pubDate": None,
        "minSalary": None,
        "maxSalary": None,
        "currency": None,
    }

    vaga = converter_vaga(vaga_himalayas)

    assert vaga.localizacao == "Worldwide"
    assert vaga.categoria is None
    assert vaga.salario is None


def test_buscar_vagas_himalayas_retorna_jobs(mocker):
    resposta_falsa = mocker.Mock()
    resposta_falsa.json.return_value = {
        "jobs": [
            {
                "title": "Data Analyst",
                "companyName": "Empresa Teste",
                "locationRestrictions": ["Brazil"],
                "applicationLink": "https://exemplo.com/vaga",
                "categories": ["Data"],
                "employmentType": "Full Time",
                "pubDate": "2026-07-14",
                "minSalary": None,
                "maxSalary": None,
                "currency": None,
            }
        ]
    }

    get_mock = mocker.patch(
        "api.himalayas.requests.get",
        return_value=resposta_falsa,
    )

    from api.himalayas import buscar_vagas

    vagas = buscar_vagas("data analyst")

    assert len(vagas) == 1
    assert isinstance(vagas[0], Job)
    assert vagas[0].titulo == "Data Analyst"

    get_mock.assert_called_once_with(
        "https://himalayas.app/jobs/api/search",
        params={
            "q": "data analyst",
            "sort": "recent",
        },
        timeout=10,
    )

    resposta_falsa.raise_for_status.assert_called_once()



def test_coleta_registra_erro_quando_api_falha(mocker):
    mocker.patch(
        "main.buscar_vagas_himalayas",
        side_effect=requests.RequestException("API indisponível"),
    )

    registrar_mock = mocker.patch("main.registrar_coleta")
    mocker.patch("main.criar_tabela")
    mocker.patch("main.criar_tabela_coletas")

    coletar_vagas(
        termo_busca="data analyst",
        fonte="himalayas",
    )

    registrar_mock.assert_called_once()

    argumentos = registrar_mock.call_args.kwargs

    assert argumentos["status"] == "erro"
    assert argumentos["vagas_encontradas"] == 0
    assert argumentos["vagas_salvas"] == 0


def test_coleta_registra_erro_quando_api_falha(
    mocker,
    caplog,
):
    mocker.patch(
        "main.buscar_vagas_himalayas",
        side_effect=requests.RequestException("API indisponível"),
    )

    registrar_mock = mocker.patch("main.registrar_coleta")
    mocker.patch("main.criar_tabela")
    mocker.patch("main.criar_tabela_coletas")

    with caplog.at_level(logging.ERROR):
        coletar_vagas(
            termo_busca="data analyst",
            fonte="himalayas",
        )

    argumentos = registrar_mock.call_args.kwargs

    assert argumentos["status"] == "erro"
    assert argumentos["vagas_encontradas"] == 0
    assert argumentos["vagas_salvas"] == 0
    assert "API indisponível" in caplog.text

