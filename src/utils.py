from pathlib import Path

from config import config_logger
from config import DATA_DIR, LOGS_DIR


logger = config_logger(__name__)


def limpar_dir(directory: Path) -> None:
    if not directory.exists():
        return
    for file in directory.iterdir():
        if file.is_file():
            logger.debug('Excluindo arquivo %s...', file.name)
            file.unlink()

def limpar_dados() -> None:
    logger.debug('Limpando dados em %s...', DATA_DIR)
    limpar_dir(DATA_DIR)

def limpar_logs() -> None:
    logger.debug('Limpando logs em %s...', LOGS_DIR)
    limpar_dir(LOGS_DIR)

def limpar_tudo() -> None:
    limpar_dados()
    limpar_logs()
