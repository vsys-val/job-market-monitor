from api.remotive import buscar_vagas


def test_buscar_vagas_retorna_lista():
    vagas = buscar_vagas("data")

    assert isinstance(vagas, list)
