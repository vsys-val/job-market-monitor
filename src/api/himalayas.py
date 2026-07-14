import requests

from models.job import Job


HIMALAYAS_API_URL = "https://himalayas.app/jobs/api/search"


def converter_vaga(vaga_himalayas: dict) -> Job:
    localizacoes = vaga_himalayas.get("locationRestrictions", [])
    categorias = vaga_himalayas.get("categories", [])

    salario_minimo = vaga_himalayas.get("minSalary")
    salario_maximo = vaga_himalayas.get("maxSalary")
    moeda = vaga_himalayas.get("currency")

    salario = None

    if salario_minimo is not None and salario_maximo is not None:
        salario = f"{moeda} {salario_minimo} - {salario_maximo}"

    return Job(
        titulo=vaga_himalayas["title"],
        empresa=vaga_himalayas["companyName"],
        localizacao=formatar_localizacoes(localizacoes),
        url=vaga_himalayas["applicationLink"],
        categoria=", ".join(categorias) if categorias else None,
        tipo_contrato=vaga_himalayas.get("employmentType"),
        data_publicacao=str(vaga_himalayas.get("pubDate")),
        salario=salario,
        fonte="himalayas",
    )


def buscar_vagas(termo_busca: str) -> list[Job]:
    response = requests.get(
        HIMALAYAS_API_URL,
        params={
            "q": termo_busca,
            "sort": "recent",
        },
        timeout=10,
    )

    response.raise_for_status()
    dados = response.json()

    return [
        converter_vaga(vaga)
        for vaga in dados["jobs"]
    ]


def formatar_localizacoes(localizacoes: list) -> str:
    if not localizacoes:
        return "Worldwide"

    nomes = []

    for localizacao in localizacoes:
        if isinstance(localizacao, str):
            nomes.append(localizacao)

        elif isinstance(localizacao, dict):
            nome = localizacao.get("name")

            if nome:
                nomes.append(nome)

    return ", ".join(nomes) if nomes else "Worldwide"