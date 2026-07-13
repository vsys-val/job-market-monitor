import logging
from pathlib import Path


LOG_PATH = Path("logs/job-market-monitor.log")


def configurar_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                LOG_PATH,
                encoding="utf-8",
            ),
        ],
    )