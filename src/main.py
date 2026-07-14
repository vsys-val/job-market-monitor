import argparse
import logging
from datetime import datetime

from config.logging_config import configurar_logging
from api.remotive import buscar_vagas
from database.sqlite import (
    criar_tabela,
    criar_tabela_coletas,
    registrar_coleta,
    salvar_vagas,
)
from export.csv_exporter import exportar_vagas_csv

logger = logging.getLogger(__name__)
configurar_logging()


def coletar_vagas(termo_busca: str) -> None:
    iniciada_em = datetime.now()

    logger.info(
        "Iniciando coleta para o termo '%s'.",
        termo_busca,
    )

    criar_tabela()
    criar_tabela_coletas()

    vagas = buscar_vagas(termo_busca)
    vagas_salvas = salvar_vagas(vagas)

    finalizada_em = datetime.now()

    registrar_coleta(
        termo_busca=termo_busca,
        iniciada_em=iniciada_em,
        finalizada_em=finalizada_em,
        vagas_encontradas=len(vagas),
        vagas_salvas=vagas_salvas,
        status="sucesso",
    )

    logger.info(
        "%s vagas encontradas e %s novas vagas salvas.",
        len(vagas),
        vagas_salvas,
    )


def exportar_dados() -> None:
    logger.info("Iniciando exportação dos dados.")

    quantidade = exportar_vagas_csv()

    logger.info(
        "%s vagas exportadas para CSV.",
        quantidade,
    )


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