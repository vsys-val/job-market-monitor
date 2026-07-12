import sqlite3

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


def salvar_vagas(vagas: list[Job]) -> None:
    with sqlite3.connect(DATABASE_PATH) as conexao:
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