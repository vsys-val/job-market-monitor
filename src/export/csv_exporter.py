import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("data/jobs.db")
OUTPUT_PATH = Path("data/processed/jobs_clean.csv")


def exportar_vagas_csv() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as conexao:
        vagas = pd.read_sql_query(
            "SELECT * FROM jobs_clean",
            conexao,
        )

    vagas.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )

    return len(vagas)