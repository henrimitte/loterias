import sqlite3

from pathlib import Path

from aposta import Aposta


class DBManager:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def close_db(self):
        if self.conn:
            self.conn.close()
    
    def commit_db(self):
        if self.conn:
            self.conn.commit()


class ApostaDB(DBManager):
    nome_tabela = 'apostas'
    def __init__(self, db_path: str = None) -> None:
        if db_path is None:
            db_path = 'apostas.db'
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

    def ler_apostas(self, loteria: str, concurso: int = None) -> None:
        filtro = '(loteria, concurso) = (?, ?)' if concurso else 'loteria = ?'
        sql = f'SELECT * FROM {self.nome_tabela} WHERE {filtro}'
        querry = self.cursor.execute(sql, [arg for arg in (loteria, concurso) if arg])
        apostas = [Aposta.from_db(ap) for ap in querry.fetchall()]
        return apostas