from abc import ABC
from dataclasses import dataclass
from random import sample

from aposta import Aposta
from db_manager import ApostaDB


@dataclass
class Limites:
    menor: int
    maior: int
    minimo: int
    maximo: int


class Loteria(ABC):
    def __init__(self, nome: str, nome_apresentacao: str, limites: Limites) -> None:
        self.nome = nome
        self.nome_apresentacao = nome_apresentacao
        self.limites = limites
        self._adb = ApostaDB()

    def criar_aposta(self, dezenas: list[int] = None, concurso: int = None) -> Aposta:
        if concurso is None:
            concurso = 0
        if dezenas is None:
            dezenas = self.surpresinha()
        return Aposta(loteria=self.nome, concurso=concurso, dezenas=dezenas)

    def surpresinha(self, quantidade: int = None) -> list[int]:
        if quantidade is None:
            quantidade = self.limites.minimo
        if self.limites.minimo <= quantidade <= self.limites.maximo:
            return sorted(sample(range(self.limites.menor, self.limites.maior + 1), k=quantidade))

    def salvar_aposta(self, aposta: Aposta) -> None:
        self._adb.registrar_aposta(aposta)


class DuplaSena(Loteria):
    def __init__(self):
        super().__init__(nome='duplasena', nome_apresentacao='Dupla-Sena',
                         limites=Limites(1, 50, 6, 15))


class Lotofacil(Loteria):
    def __init__(self):
        super().__init__(nome='lotofacil', nome_apresentacao='Lotofácil',
                         limites=Limites(1, 25, 15, 20))


class Lotomania(Loteria):
    def __init__(self):
        super().__init__(nome='lotomania', nome_apresentacao='Lotomania',
                         limites=Limites(1, 100, 50, 50))


class MegaSena(Loteria):
    def __init__(self):
        super().__init__(nome='megasena', nome_apresentacao='Mega-Sena',
                         limites=Limites(1, 60, 6, 20))


class Quina(Loteria):
    def __init__(self):
        super().__init__(nome='lotofacil', nome_apresentacao='Quina',
                         limites=Limites(1, 80, 5, 15))


opcoes_loterias = {'duplasena': DuplaSena(),
                   'lotofacil': Lotofacil(), 
                   'lotomania': Lotomania(), 
                   'mega': MegaSena(), 
                   'quina': Quina()}