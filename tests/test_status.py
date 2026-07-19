from main import exibir_status


def test_exibir_status_mostra_ultima_coleta(
    mocker,
    capsys,
):
    mocker.patch(
        "main.buscar_ultima_coleta",
        return_value={
            "termo_busca": "data analyst",
            "iniciada_em": "2026-07-18T20:00:00",
            "finalizada_em": "2026-07-18T20:00:05",
            "vagas_encontradas": 12,
            "vagas_salvas": 3,
            "status": "sucesso",
        },
    )

    exibir_status()

    saida = capsys.readouterr().out

    assert "data analyst" in saida
    assert "sucesso" in saida
    assert "Encontradas: 12" in saida
    assert "Novas: 3" in saida


def test_exibir_status_sem_coletas(
    mocker,
    capsys,
):
    mocker.patch(
        "main.buscar_ultima_coleta",
        return_value=None,
    )

    exibir_status()

    saida = capsys.readouterr().out

    assert "Nenhuma coleta foi registrada ainda." in saida