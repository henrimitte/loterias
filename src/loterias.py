from abc import ABC
from dataclasses import dataclass
from random import sample

from aposta import Aposta
from config import config_logger
from db_manager import ApostaDB


logger = config_logger(__name__)


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
        logger.debug(f'Loteria {self.nome_apresentacao} iniciada.')

    def criar_aposta(self, dezenas: list[int] = None, concurso: int = None) -> Aposta:
        if concurso is None:
            logger.debug(f'CONCURSO não fornecido. Definindo como 0.')
            concurso = 0
        if dezenas is None:
            logger.debug(f'DEZENAS não fornecidas. Gerando aposta aleatoria.')
            dezenas = self.surpresinha()
        if self.dezenas_sao_validas(dezenas):
            logger.debug(
                f'Aposta {self.nome_apresentacao} de {len(dezenas)} dezenas, concurso {concurso} criada com sucesso!')
            return Aposta(loteria=self.nome, concurso=concurso, dezenas=dezenas)

    def surpresinha(self, quantidade: int = None) -> list[int]:
        if quantidade is None:
            quantidade = self.limites.minimo
        if self.limites.minimo <= quantidade <= self.limites.maximo:
            logger.debug(f'Gerando SURPRESINHA com {quantidade} dezenas.')
            return sorted(sample(range(self.limites.menor, self.limites.maior + 1), k=quantidade))
        logger.error(
            f'Erro ao gerar SURPRESINHA.\QUANTIDADE de dezenas deve obedecer os limites: {self.limites.minimo} <= QUANTIDADE <= {self.limites.maximo}. QUANTIDADE fornecida = {quantidade}.')

    def salvar_aposta(self, aposta: Aposta) -> None:
        self._adb.registrar_aposta(aposta)
        logger.info(f'Aposta salva com sucesso!')

    def dezenas_sao_validas(self, dezenas: list[int]) -> bool:
        qtd, mid, mad = len(dezenas), min(dezenas), max(dezenas)
        if not (self.limites.minimo <= qtd <= self.limites.maximo):
            logger.error(
                f'QUANTIDADE incorreta de dezenas. QUANTIDADE deve obedecer limites: {self.limites.minimo} <= QUANTIDADE <= {self.limites.maximo}. QUANTIDADE fornecida = {qtd}.')
            return False
        if not (mid >= self.limites.menor):
            logger.error(
                f'MENOR dezena deve ser >= {self.limites.menor}. MENOR dezena fornecida = {mid}.')
            return False
        if not (mad <= self.limites.maior):
            logger.error(
                f'MAIOR dezena deve ser <= {self.limites.maior}. MAIOR dezena fornecida = {mad}.')
            return False
        if not (len(set(dezenas)) == qtd):
            logger.error(f'DEZENAS não podem ser repetidas.')
            return False
        logger.debug(
            f'Dezenas fornecidas são válidas para {self.nome_apresentacao}.')
        return True


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


opcoes_loterias = ['duplasena', 'lotofacil', 'lotomania', 'mega', 'quina']


def loteria_factory(loteria: str) -> Loteria:
    match loteria:
        case 'duplasena':
            return DuplaSena()
        case 'lotofacil':
            return Lotofacil()
        case 'lotomania':
            return Lotomania()
        case 'mega':
            return MegaSena()
        case 'quina':
            return Quina()
