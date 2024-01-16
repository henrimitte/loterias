import sqlite3

from pathlib import Path

from aposta import Aposta
from config import config_logger


logger = config_logger(__name__)


class DBManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        logger.debug(f'DBManager iniciado. Caminho: {self.db_path}')

    def close_db(self):
        if self.conn:
            self.conn.close()
            logger.debug(f'DBManager em {self.db_path} fechado com sucesso!')

    def commit_db(self):
        if self.conn:
            self.conn.commit()
            logger.debug(f'Commit em {self.db_path} executado com sucesso!')


class ApostaDB(DBManager):
    nome_tabela = 'apostas'

    def __init__(self, db_path: str = None) -> None:
        if db_path is None:
            db_path = f'{self.nome_tabela}.db'
        super().__init__(db_path)
        self.criar_tabela()

    def criar_tabela(self):
        sql = f'''CREATE TABLE IF NOT EXISTS {self.nome_tabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loteria TEXT,
            concurso TEXT,
            dezenas TEXT,
            conferida INTEGER,
            quantidadeAcertos INTEGER,
            dezenasAcertadas TEXT,
            valorPremiacao REAL)'''
        self.cursor.execute(sql)
        self.commit_db()
        logger.debug(f'Tabela {self.nome_tabela} criada com sucesso!')

    def registrar_aposta(self, aposta) -> None:
        params = aposta.to_db()
        sql = f'''INSERT INTO {self.nome_tabela} (
            loteria,
            concurso,
            dezenas,
            conferida,
            quantidadeAcertos,
            dezenasAcertadas,
            valorPremiacao)
                VALUES (
            :loteria,
            :concurso,
            :dezenas,
            :conferida,
            :quantidadeAcertos,
            :dezenasAcertadas,
            :valorPremiacao)'''
        self.cursor.execute(sql, aposta.to_db())
        self.commit_db()
        logger.info(f'Registro inserido com sucesso em "{self.nome_tabela}"!')

    def ler_apostas(self, loteria: str, concurso: int = None) -> None:
        logger.debug(f'Lendo apostas de {loteria=} e {concurso=}')
        filtro = '(loteria, concurso) = (?, ?)' if concurso else 'loteria = ?'
        sql = f'SELECT * FROM {self.nome_tabela} WHERE {filtro}'
        querry = self.cursor.execute(
            sql, [arg for arg in (loteria, concurso) if arg])
        apostas = [Aposta.from_db(ap) for ap in querry.fetchall()]
        return apostas
