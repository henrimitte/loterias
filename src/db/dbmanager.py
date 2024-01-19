import sqlite3

from abc import ABC

from config import config_logger, DATA_DIR


logger = config_logger(__name__)


class DBManager(ABC):
    def __init__(self, db_path: str) -> None:
        self.db_path = DATA_DIR / db_path
        logger.debug('Iniciando DBManager em: %s', self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def criar_tabela(self, sql: str) -> None:
        logger.debug('Criando tabela "%s"', self.nome_tabela)
        self.cursor.execute(sql)

    def close_db(self) -> None:
        logger.debug('Fechando DBManager em %s', self.db_path)
        if self.conn:
            self.conn.close()

    def commit_db(self) -> None:
        logger.debug('Commitando em %s', self.db_path)
        if self.conn:
            self.conn.commit()
