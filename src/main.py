import argparse

from api.remotive import buscar_vagas
from database.sqlite import criar_tabela, salvar_vagas
from export.csv_exporter import exportar_vagas_csv


def coletar_vagas() -> None:
    criar_tabela()

    vagas = buscar_vagas("data")
    salvar_vagas(vagas)

    print(f"{len(vagas)} vagas processadas.")


def exportar_dados() -> None:
    quantidade = exportar_vagas_csv()

    print(f"{quantidade} vagas exportadas.")


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Coleta, armazena e exporta vagas de dados."
    )

    parser.add_argument(
        "comando",
        choices=["collect", "export", "all"],
        help="Ação que será executada.",
    )

    return parser


def main() -> None:
    parser = criar_parser()
    argumentos = parser.parse_args()

    if argumentos.comando == "collect":
        coletar_vagas()

    elif argumentos.comando == "export":
        exportar_dados()

    elif argumentos.comando == "all":
        coletar_vagas()
        exportar_dados()


if __name__ == "__main__":
    main()