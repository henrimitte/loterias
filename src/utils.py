from pathlib import Path

from config import config_logger
from config import DATA_DIR, LOGS_DIR


logger = config_logger(__name__)


def limpar_dir(directory: Path) -> None:
    logger.debug('Limpando diretório em %s...', directory)
    if not directory.exists():
        return
    for item in directory.iterdir():
        if item.is_file():
            logger.debug('Removendo arquivo %s...', item.name)
            item.unlink()
        elif item.is_dir():
            limpar_dir(item)
            logger.debug('Removendo diretório %s...', item.name)
            item.rmdir()

def limpar_dados() -> None:
    limpar_dir(DATA_DIR)

def limpar_logs() -> None:
    limpar_dir(LOGS_DIR)

def limpar_tudo() -> None:
    limpar_dados()
    limpar_logs()
