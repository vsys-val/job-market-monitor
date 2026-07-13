import argparse

from api.remotive import buscar_vagas
from database.sqlite import criar_tabela, salvar_vagas
from export.csv_exporter import exportar_vagas_csv


def coletar_vagas(termo_busca: str) -> None:
    criar_tabela()

    vagas = buscar_vagas(termo_busca)
    salvar_vagas(vagas)

    print(
        f"{len(vagas)} vagas processadas "
        f"para a busca '{termo_busca}'."
    )


def exportar_dados() -> None:
    quantidade = exportar_vagas_csv()

    print(f"{quantidade} vagas exportadas.")


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Coleta, armazena e exporta vagas de dados."
    )

    subparsers = parser.add_subparsers(
        dest="comando",
        required=True,
    )

    collect_parser = subparsers.add_parser(
        "collect",
        help="Coleta e salva vagas.",
    )

    collect_parser.add_argument(
        "--search",
        required=True,
        help="Termo usado para buscar vagas.",
    )

    subparsers.add_parser(
        "export",
        help="Exporta os dados tratados para CSV.",
    )

    all_parser = subparsers.add_parser(
        "all",
        help="Executa coleta e exportação.",
    )

    all_parser.add_argument(
        "--search",
        required=True,
        help="Termo usado para buscar vagas.",
    )

    return parser


def main() -> None:
    parser = criar_parser()
    argumentos = parser.parse_args()

    if argumentos.comando == "collect":
        coletar_vagas(argumentos.search)

    elif argumentos.comando == "export":
        exportar_dados()

    elif argumentos.comando == "all":
        coletar_vagas(argumentos.search)
        exportar_dados()


if __name__ == "__main__":
    main()