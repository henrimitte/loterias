from aposta import Aposta
from .dbmanager import DBManager

from config import config_logger, DATA_DIR


logger = config_logger(__name__)


class ApostaDB(DBManager):
    nome_tabela = 'apostas'

    def __init__(self, db_path: str = None) -> None:
        if db_path is None:
            db_path = f'{self.nome_tabela}.db'
        super().__init__(db_path)
        self.criar_tabela(self.tabela_sql)

    @property
    def tabela_sql(self) -> str:
        return f'''CREATE TABLE IF NOT EXISTS {self.nome_tabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loteria TEXT,
            concurso INTEGER,
            dezenas TEXT,
            conferida INTEGER,
            quantidadeAcertos INTEGER,
            dezenasAcertadas TEXT,
            valorPremiacao REAL)'''

    def registrar_aposta(self, aposta) -> None:
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

    def ler_apostas(self, loteria: str, concurso: int = None) -> list[Aposta]:
        logger.debug('Lendo apostas em "%s"', self.nome_tabela)
        filtro = '(loteria, concurso) = (?, ?)' if concurso else 'loteria = ?'
        sql = f'SELECT * FROM {self.nome_tabela} WHERE {filtro}'
        querry = self.cursor.execute(
            sql, [arg for arg in (loteria, concurso) if arg])
        return [Aposta.from_db(ap) for ap in querry.fetchall()] if querry else []

    def ler_todas_apostas(self) -> list[Aposta]:
        sql = f'SELECT * FROM {self.nome_tabela}'
        querry = self.cursor.execute(sql)
        return [Aposta.from_db(ap) for ap in querry.fetchall()] if querry else []

    def ler_apostas_por_loteria(self, loteria: str) -> list[Aposta]:
        sql = f'SELECT * FROM {self.nome_tabela} WHERE loteria = "{loteria}"'
        querry = self.conn.execute(sql)
        return [Aposta.from_db(ap) for ap in querry.fetchall()] if querry else []

    def ler_apostas_por_loteria_e_concurso(self, loteria: str, concurso: int) -> list[Aposta]:
        sql = f'SELECT * FROM {self.nome_tabela} WHERE (loteria, concurso) = ("{loteria}", {concurso})'
        querry = self.conn.execute(sql)
        return [Aposta.from_db(ap) for ap in querry.fetchall()] if querry else []

    def atualizar_aposta(self, aposta: Aposta) -> None:
        logger.debug('Atualizando aposta')
        sql = f'''UPDATE {self.nome_tabela} SET (
            conferida,
            dezenasAcertadas,
            quantidadeAcertos,
            valorPremiacao)
                = (
            :conferida,
            :dezenasAcertadas,
            :quantidadeAcertos,
            :valorPremiacao)
                WHERE (
            id = {aposta._id})'''
        self.cursor.execute(sql, aposta.to_db())
        self.commit_db()
