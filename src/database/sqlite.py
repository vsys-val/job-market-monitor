import sqlite3
from datetime import datetime

from models.job import Job


DATABASE_PATH = "data/jobs.db"


def criar_tabela() -> None:
    with sqlite3.connect(DATABASE_PATH) as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                empresa TEXT NOT NULL,
                localizacao TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                categoria TEXT,
                tipo_contrato TEXT,
                data_publicacao TEXT,
                salario TEXT,
                fonte TEXT NOT NULL
            )
            """
        )


def salvar_vagas(vagas: list[Job]) -> int:
    with sqlite3.connect(DATABASE_PATH) as conexao:
        alteracoes_antes = conexao.total_changes

        conexao.executemany(
            """
            INSERT OR IGNORE INTO jobs (
                titulo,
                empresa,
                localizacao,
                url,
                categoria,
                tipo_contrato,
                data_publicacao,
                salario,
                fonte
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    vaga.titulo,
                    vaga.empresa,
                    vaga.localizacao,
                    vaga.url,
                    vaga.categoria,
                    vaga.tipo_contrato,
                    vaga.data_publicacao,
                    vaga.salario,
                    vaga.fonte,
                )
                for vaga in vagas
            ],
        )

        return conexao.total_changes - alteracoes_antes


def criar_tabela_coletas() -> None:
    with sqlite3.connect(DATABASE_PATH) as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS collection_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                termo_busca TEXT NOT NULL,
                iniciada_em TEXT NOT NULL,
                finalizada_em TEXT NOT NULL,
                vagas_encontradas INTEGER NOT NULL,
                vagas_salvas INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """
        )


def registrar_coleta(
    termo_busca: str,
    iniciada_em: datetime,
    finalizada_em: datetime,
    vagas_encontradas: int,
    vagas_salvas: int,
    status: str,
) -> None:
    with sqlite3.connect(DATABASE_PATH) as conexao:
        conexao.execute(
            """
            INSERT INTO collection_runs (
                termo_busca,
                iniciada_em,
                finalizada_em,
                vagas_encontradas,
                vagas_salvas,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                termo_busca,
                iniciada_em.isoformat(),
                finalizada_em.isoformat(),
                vagas_encontradas,
                vagas_salvas,
                status,
            ),
        )


def buscar_ultima_coleta() -> dict | None:
    with sqlite3.connect(DATABASE_PATH) as conexao:
        conexao.row_factory = sqlite3.Row

        resultado = conexao.execute(
            """
            SELECT
                termo_busca,
                iniciada_em,
                finalizada_em,
                vagas_encontradas,
                vagas_salvas,
                status
            FROM collection_runs
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if resultado is None:
        return None

    return dict(resultado)
