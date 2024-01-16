import json
import urllib.request

from abc import ABC
from dataclasses import dataclass
from enum import StrEnum
from random import sample

from aposta import Aposta
from resultado import Resultado
from config import config_logger
from db_manager import ApostaDB, ResultadoDB


logger = config_logger(__name__)


@dataclass
class Limites:
    menor: int
    maior: int
    minimo: int
    maximo: int


class Loterias(StrEnum):
    DUPLASENA = 'duplasena'
    LOTOFACIL = 'lotofacil'
    LOTOMANIA = 'lotomania'
    MEGASENA = 'megasena'
    QUINA = 'quina'


class Loteria(ABC):
    def __init__(self, nome: str, nome_apresentacao: str, limites: Limites) -> None:
        self.nome = str(nome)
        self.nome_apresentacao = nome_apresentacao
        self.limites = limites
        self._adb = ApostaDB()
        self._rdb = ResultadoDB()
        logger.debug(f'Loteria {self.nome_apresentacao} iniciada.')

    def criar_aposta(self, dezenas: list[int] = None, concurso: int = None) -> Aposta:
        if concurso is None:
            logger.debug(f'CONCURSO não fornecido. Definindo como 0.')
            concurso = 0
        if dezenas is None:
            logger.debug(f'DEZENAS não fornecidas. Gerando aposta aleatoria.')
            dezenas = self.escolher_dezenas()
        if self.dezenas_sao_validas(dezenas):
            logger.debug(
                f'Aposta {self.nome_apresentacao} de {len(dezenas)} dezenas, concurso {concurso} criada com sucesso!')
            return Aposta(loteria=self.nome, concurso=concurso, dezenas=dezenas)
        logger.error(f'A aposta não foi criada.')

    def surpresinha(self, quantidade: int = None) -> list[int]:
        if quantidade is None:
            quantidade = self.limites.minimo
        if self.limites.minimo <= quantidade <= self.limites.maximo:
            logger.debug(f'Gerando SURPRESINHA com {quantidade} dezenas.')
            return sorted(sample(range(self.limites.menor, self.limites.maior + 1), k=quantidade))
        logger.error(
            f'Erro ao gerar SURPRESINHA.\QUANTIDADE de dezenas deve obedecer os limites: {self.limites.minimo} <= QUANTIDADE <= {self.limites.maximo}. QUANTIDADE fornecida = {quantidade}.')

    def salvar_aposta(self, aposta: Aposta) -> None:
        if aposta:
            self._adb.registrar_aposta(aposta)
            logger.info(f'Aposta salva com sucesso!')
        else:
            logger.error(f'Não foi possível salvar a aposta.')

    def dezenas_sao_validas(self, dezenas: list[int]) -> bool:
        if dezenas is None:
            logger.error(f'DEZENAS não pode ser None')
            return False

        qtd, mid, mad = len(dezenas), min(dezenas), max(dezenas)
        validar = True
        if not (self.limites.minimo <= qtd <= self.limites.maximo):
            logger.error(
                f'QUANTIDADE incorreta de dezenas. QUANTIDADE deve obedecer limites: {self.limites.minimo} <= QUANTIDADE <= {self.limites.maximo}. QUANTIDADE fornecida = {qtd}.')
            validar = False
        if not (mid >= self.limites.menor):
            logger.error(
                f'MENOR dezena deve ser >= {self.limites.menor}. MENOR dezena fornecida = {mid}.')
            validar = False
        if not (mad <= self.limites.maior):
            logger.error(
                f'MAIOR dezena deve ser <= {self.limites.maior}. MAIOR dezena fornecida = {mad}.')
            validar = False
        if not (len(set(dezenas)) == qtd):
            logger.error(f'DEZENAS não podem ser repetidas.')
            validar = False

        if validar:
            logger.debug(f'Dezenas fornecidas são válidas para {self.nome_apresentacao}.')
        return validar

    def escolher_dezenas(self) -> list[int]:
        done = False
        escolha = '1'
        dezenas = self.surpresinha()
        while not done:
            logger.info(f'{self.nome_apresentacao.upper()}: {" ".join(map(str, dezenas))}')
            escolha = input(
                f'[1] Gerar novas dezenas  [2] Confirmar  [3] Sair: ')
            match escolha:
                case '1':
                    dezenas = self.surpresinha()
                case '2' | '':
                    done = True
                    return dezenas
                case '3':
                    done = True

    def listar_apostas(self, concurso: int = None) -> None:
        apostas = self._adb.ler_apostas(self.nome, concurso)
        if apostas:
            print(f'{len(apostas)} encontradas para {self.nome_apresentacao}:')
            for ap in apostas:
                print(f'{" ".join((f"{n:0>2}" for n in ap.dezenas)):<30} Concurso: {ap.concurso:>4} Conferida: {ap.conferida}')
        else:
            print(f'Nenhuma aposta encontrada para {self.nome_apresentacao}.')

    def encerrar(self):
        self._adb.close_db()
        self._rdb.close_db()
        logger.debug(f'Loteria {self.nome_apresentacao} encerrada.')

    def buscar_resultado_online(self, concurso: int) -> Resultado:
        logger.debug('Buscando resultado da %s para o concurso %s', self.nome_apresentacao, concurso)
        url = f'https://loteriascaixa-api.herokuapp.com/api/{self.nome}/{concurso}'
        with urllib.request.urlopen(url) as req:
            resultado = json.load(req)
            return Resultado.from_json(**resultado)
        logger.error('Erro ao procurar resultado online.')


class DuplaSena(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.DUPLASENA, nome_apresentacao='Dupla-Sena',
                         limites=Limites(1, 50, 6, 15))


class Lotofacil(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.LOTOFACIL, nome_apresentacao='Lotofácil',
                         limites=Limites(1, 25, 15, 20))


class Lotomania(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.LOTOMANIA, nome_apresentacao='Lotomania',
                         limites=Limites(1, 100, 50, 50))


class MegaSena(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.MEGASENA, nome_apresentacao='Mega-Sena',
                         limites=Limites(1, 60, 6, 20))


class Quina(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.QUINA, nome_apresentacao='Quina',
                         limites=Limites(1, 80, 5, 15))


opcoes_loterias = [Loterias.DUPLASENA, Loterias.LOTOFACIL, Loterias.LOTOMANIA, Loterias.MEGASENA, Loterias.QUINA]


def loteria_factory(loteria: str) -> Loteria:
    match loteria:
        case Loterias.DUPLASENA:
            return DuplaSena()
        case Loterias.LOTOFACIL:
            return Lotofacil()
        case Loterias.LOTOMANIA:
            return Lotomania()
        case Loterias.MEGASENA:
            return MegaSena()
        case Loterias.QUINA:
            return Quina()
