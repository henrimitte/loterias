from .dbmanager import DBManager
from config import config_logger, DATA_DIR
from models.resultado import Resultado


logger = config_logger(__name__)


class ResultadoDB(DBManager):
    def __init__(self) -> None:
        super().__init__('resultados')
        self.criar_tabela(self.tabela_sql)

    @property
    def tabela_sql(self) -> str:
        return f'''CREATE TABLE IF NOT EXISTS {self.nome_tabela} (
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
            PRIMARY KEY (loteria, concurso))'''

    def registrar_resultado(self, resultado: Resultado) -> None:
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
        self.cursor.execute(sql, resultado.to_db())
        self.commit_db()

    def registrar_resultados(self, resultados: list[Resultado]) -> None:
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
        self.cursor.executemany(sql, (resultado.to_db()
                                for resultado in resultados))
        self.commit_db()

    def ler_todos_resultados(self) -> list[Resultado]:
        sql = f'SELECT * FROM {self.nome_tabela}'
        querry = self.cursor.execute(sql).fetchall()
        return [Resultado.from_db(r) for r in querry] if querry else []

    def ler_resultados_por_loteria(self, loteria: str) -> list[Resultado]:
        sql = f'SELECT * FROM resultados WHERE loteria = "{loteria}"'
        querry = self.cursor.execute(sql).fetchall()
        return [Resultado.from_db(r) for r in querry] if querry else []

    def ler_resultado_por_loteria_e_concurso(self, loteria: str, concurso: int) -> Resultado:
        sql = f'SELECT * FROM resultados WHERE (loteria, concurso) = ("{loteria}", {concurso})'
        querry = self.cursor.execute(sql).fetchone()
        return Resultado.from_db(querry) if querry else None

    def ultimo_resultado_registrado_por_loteria(self, loteria: str) -> Resultado:
        sql = f'SELECT MAX(concurso),* FROM {self.nome_tabela} WHERE loteria = "{loteria}"'
        querry = self.cursor.execute(sql).fetchone()
        _, *resultado = querry
        return Resultado.from_db(resultado) if resultado else None
