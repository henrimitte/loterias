from aposta import Aposta
from config import config_logger
from .dbmanager import DBManager


class ApostaDB(DBManager):
    def __init__(self) -> None:
        super().__init__('apostas')
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

    def registrar_aposta(self, aposta: Aposta) -> None:
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

    def ler_apostas_por_loteria(self, loteria: str) -> list[Aposta]:
        sql = f'SELECT * FROM {self.nome_tabela} WHERE loteria = "{loteria}" ORDER BY concurso'
        querry = self.cursor.execute(sql).fetchall()
        return [Aposta.from_db(ap) for ap in querry] if querry else []

    def ler_apostas_por_loteria_e_concurso(self, loteria: str, concurso: int) -> list[Aposta]:
        sql = f'SELECT * FROM {self.nome_tabela} WHERE (loteria, concurso) = ("{loteria}", {concurso}) ORDER BY concurso'
        querry = self.cursor.execute(sql).fetchall()
        return [Aposta.from_db(ap) for ap in querry] if querry else []

    def ler_todas_apostas(self) -> list[Aposta]:
        sql = f'SELECT * FROM {self.nome_tabela} ORDER BY (loteria, concurso)'
        querry = self.cursor.execute(sql).fetchall()
        return [Aposta.from_db(ap) for ap in querry] if querry else []

    def atualizar_aposta(self, aposta: Aposta) -> None:
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
            id = :_id)'''
        self.cursor.execute(sql, aposta.to_db())
        self.commit_db()

    def atualizar_apostas(self, apostas: list[Aposta]) -> None:
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
            id = :_id)'''
        self.cursor.executemany(sql, (aposta.to_db() for aposta in apostas))
        self.commit_db()

    def excluir_aposta(self, aposta: Aposta) -> None:
        sql = f'DELETE FROM {self.nome_tabela} WHERE id = {aposta._id}'
        self.cursor.execute(sql)
        self.commit_db()

    def excluir_apostas(self, apostas: list[Aposta]) -> None:
        sql = f'DELETE FROM {self.nome_tabela} WHERE id = ?'
        self.cursor.executemany(sql, (aposta._id for aposta in apostas))
        self.commit_db()
