import sqlite3

from pathlib import Path

from aposta import Aposta
from config import config_logger
from resultado import Resultado


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


class ResultadoDB(DBManager):
    '''Gerenciador do banco de dados dos resultados das Loterias Caixa.'''
    nome_tabela = 'resultados'

    def __init__(self, db_path: str = None) -> None:
        if db_path is None:
            db_path = f'{self.nome_tabela}.db'
        super().__init__(db_path)
        self.criar_tabela()

    def criar_tabela(self) -> None:
        '''Cria a tabela resultados no banco de dados.'''
        sql = f'''CREATE TABLE IF NOT EXISTS {self.nome_tabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acumulou INTEGER,
            concurso INTEGER,
            data TEXT,
            dataProximoConcurso TEXT,
            dezenas TEXT,
            dezenasOrdemSorteio TEXT,
            estadosPremiados TEXT,
            local TEXT,
            localGanhadores TEXT,
            loteria TEXT,
            mesSorte TEXT,
            observacao TEXT,
            premiacoes TEXT,
            proximoConcurso INTEGER,
            timeCoracao TEXT,
            trevos TEXT,
            valorAcumuladoConcursoEspecial REAL,
            valorAcumuladoConcurso_0_5 REAL,
            valorAcumuladoProximoConcurso REAL,
            valorArrecadado REAL,
            valorEstimadoProximoConcurso INTEGER,
            UNIQUE(loteria, concurso))'''
        self.cursor.execute(sql)
        self.commit_db()
        logger.debug('Tabela %s criada com sucesso!', self.nome_tabela)

    def registrar_resultado(self, resultado: dict) -> None:
        '''Registra um novo resultado no banco de dados'''
        sql = f'''INSERT INTO {self.nome_tabela} (
            acumulou,
            concurso,
            data,
            dataProximoConcurso,
            dezenas,
            dezenasOrdemSorteio,
            estadosPremiados,
            local,
            localGanhadores,
            loteria,
            mesSorte,
            observacao,
            premiacoes,
            proximoConcurso,
            timeCoracao,
            trevos,
            valorAcumuladoConcursoEspecial,
            valorAcumuladoConcurso_0_5,
            valorAcumuladoProximoConcurso,
            valorArrecadado,
            valorEstimadoProximoConcurso) 
                VALUES (
            :acumulou,
            :concurso,
            :data,
            :dataProximoConcurso,
            :dezenas,
            :dezenasOrdemSorteio,
            :estadosPremiados,
            :local,
            :localGanhadores,
            :loteria,
            :mesSorte,
            :observacao,
            :premiacoes,
            :proximoConcurso,
            :timeCoracao,
            :trevos,
            :valorAcumuladoConcursoEspecial,
            :valorAcumuladoConcurso_0_5,
            :valorAcumuladoProximoConcurso,
            :valorArrecadado,
            :valorEstimadoProximoConcurso)'''
        try:
            self.cursor.execute(sql, resultado.to_db())
            self.commit_db()
            logger.info('Registro inserido com sucesso em "%s"!', self.nome_tabela)
        except sqlite3.IntegrityError:
            logger.debug('Registro já existe, nada para fazer.')

    def ler_todos_resultados(self) -> list[Resultado]:
        logger.debug('Lendo todos os resultados...')
        querry = self.cursor.execute(f'SELECT * FROM {self.nome_tabela}').fetchall()
        return [Resultado.from_db(r) for r in querry]

    def ler_resultados_por_loteria(self, loteria: str, concurso: int = None) -> list[Resultado]:
        logger.debug(f'Lendo resultados da {loteria}. Concurso: {concurso if concurso else "TODOS"}...')
        filtros = f'(loteria, concurso) = ("{loteria}", {concurso})' if concurso else f'loteria = "{loteria}"'
        querry = self.cursor.execute(f'SELECT * FROM resultados WHERE {filtros}').fetchall()
        return [Resultado.from_db(r) for r in querry]

    def ultimo_concurso_resultado_registrado_por_loteria(self, loteria: str) -> tuple[int, Resultado]:
        logger.debug(f'Buscando último concurso registrado da {loteria}.')
        sql = f'SELECT MAX(concurso),* FROM {self.nome_tabela} WHERE loteria = "{loteria}"'
        querry = self.cursor.execute(sql).fetchone()
        concurso, *resultado = querry
        if concurso:
            return concurso, Resultado.from_db(resultado)
        return None, None