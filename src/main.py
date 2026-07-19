import argparse
import logging
from datetime import datetime
from requests import RequestException

from config.logging_config import configurar_logging
from api.himalayas import buscar_vagas as buscar_vagas_himalayas
from api.remotive import buscar_vagas as buscar_vagas_remotive
from database.sqlite import (
    criar_tabela,
    criar_tabela_coletas,
    registrar_coleta,
    salvar_vagas,
    buscar_ultima_coleta,
)
from export.csv_exporter import exportar_vagas_csv

logger = logging.getLogger(__name__)
configurar_logging()


def coletar_vagas(termo_busca: str, fonte: str) -> None:
    iniciada_em = datetime.now()

    logger.info(
        "Iniciando coleta para '%s' usando a fonte '%s'.",
        termo_busca,
        fonte,
    )

    criar_tabela()
    criar_tabela_coletas()

    try:
        if fonte == "remotive":
            vagas = buscar_vagas_remotive(termo_busca)

        elif fonte == "himalayas":
            vagas = buscar_vagas_himalayas(termo_busca)

        else:
            raise ValueError(f"Fonte não suportada: {fonte}")

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
            "%s vagas encontradas e %s vagas novas salvas.",
            len(vagas),
            vagas_salvas,
        )

    except RequestException as erro:
        finalizada_em = datetime.now()

        registrar_coleta(
            termo_busca=termo_busca,
            iniciada_em=iniciada_em,
            finalizada_em=finalizada_em,
            vagas_encontradas=0,
            vagas_salvas=0,
            status="erro",
        )

        logger.error(
            "Falha ao consultar a fonte '%s': %s",
            fonte,
            erro,
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

    collect_parser.add_argument(
    "--source",
    choices=["remotive", "himalayas"],
    default="remotive",
    help="Fonte utilizada na coleta.",
    )
    
    subparsers.add_parser(
        "export",
        help="Exporta os dados tratados para CSV.",
    )

    subparsers.add_parser(
    "status",
    help="Exibe informações da última coleta.",
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

    all_parser.add_argument(
    "--source",
    choices=["remotive", "himalayas"],
    default="remotive",
    help="Fonte utilizada na coleta.",
    )

    return parser


def exibir_status() -> None:
    ultima_coleta = buscar_ultima_coleta()

    if ultima_coleta is None:
        print("Nenhuma coleta foi registrada ainda.")
        return

    print("Última coleta")
    print(f"Busca: {ultima_coleta['termo_busca']}")
    print(f"Status: {ultima_coleta['status']}")
    print(f"Encontradas: {ultima_coleta['vagas_encontradas']}")
    print(f"Novas: {ultima_coleta['vagas_salvas']}")
    print(f"Início: {ultima_coleta['iniciada_em']}")
    print(f"Fim: {ultima_coleta['finalizada_em']}")


def main() -> None:
    parser = criar_parser()
    argumentos = parser.parse_args()

    if argumentos.comando == "collect":
        coletar_vagas(
            termo_busca=argumentos.search,
            fonte=argumentos.source,
        )

    elif argumentos.comando == "all":
        coletar_vagas(
            termo_busca=argumentos.search,
            fonte=argumentos.source,
        )
        exportar_dados()

    elif argumentos.comando == "export":
        exportar_dados()

    elif argumentos.comando == "status":
        exibir_status()

if __name__ == "__main__":
    main()