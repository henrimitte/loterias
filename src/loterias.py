import json
import urllib.request

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
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
        logger.debug('Loteria %s iniciada.', self.nome_apresentacao)

    def criar_aposta(self, dezenas: list[int] = None, concurso: int = None) -> Aposta:
        if concurso is None:
            logger.debug('CONCURSO não fornecido.')
            ultimo, resultado = self._rdb.ultimo_concurso_resultado_registrado_por_loteria(self.nome)
            if ultimo is None:
                logger.debug('Nenhum concurso encontrado para %s. Atualizando banco de dados.', self.nome_apresentacao)
                res = self.busca_e_registra_resultado()
                concurso = res.concurso
            if ultimo:
                data_prox_sorteio = datetime.strptime(resultado.dataProximoConcurso + ' 21:30', '%d/%m/%Y %H:%M')
                if datetime.today() >= data_prox_sorteio:
                    logger.debug('Existem novos resultados disponiveis para %s.', self.nome_apresentacao)
                    resultado = self.buscar_resultado_online()
                    self.salvar_resultado(resultado)
                    logger.debug('Resultados da %s foram atualizados. Definindo concurso = %s', self.nome_apresentacao, resultado.concurso)
                    concurso = resultado.concurso
                else:
                    logger.debug('Resultados da %s estão atualizados. Definindo concurso = %s', self.nome_apresentacao, resultado.proximoConcurso)
                    concurso = ultimo
        if not concurso:
            logger.warning('Não foi possível obter último concurso da %s, deixando como 0.', self.nome_apresentacao)
            concurso = 0

        if dezenas is None:
            logger.debug('DEZENAS não fornecidas.')
            dezenas = self.escolher_dezenas()
        if self.dezenas_sao_validas(dezenas):
            logger.debug(
                'Aposta %s de %s dezenas, concurso %s criada com sucesso!', self.nome_apresentacao, len(dezenas), concurso)
            return Aposta(loteria=self.nome, concurso=concurso, dezenas=dezenas)
        logger.error('A aposta não foi criada.')

    def salvar_aposta(self, aposta: Aposta) -> None:
        if aposta:
            self._adb.registrar_aposta(aposta)
            logger.info('Aposta salva com sucesso!')
        else:
            logger.error('Não foi possível salvar a aposta.')

    def listar_apostas(self, concurso: int = None) -> None:
        apostas = self._adb.ler_apostas(self.nome, concurso)
        if apostas:
            logger.info('%s encontradas para %s:', len(apostas), self.nome_apresentacao)
            for ap in apostas:
                print(f'{" ".join((f"{n:0>2}" for n in ap.dezenas)):<30} Concurso: {ap.concurso:>4} Conferida: {ap.conferida}')
        else:
            logger.info('Nenhuma aposta encontrada para %s.', self.nome_apresentacao)

    def surpresinha(self, quantidade: int = None) -> list[int]:
        if quantidade is None:
            quantidade = self.limites.minimo
        if self.limites.minimo <= quantidade <= self.limites.maximo:
            logger.debug('Gerando SURPRESINHA com %s dezenas.', quantidade)
            return sorted(sample(range(self.limites.menor, self.limites.maior + 1), k=quantidade))
        logger.error(
            'Erro ao gerar SURPRESINHA. QUANTIDADE de dezenas deve obedecer os limites: %s <= QUANTIDADE <= %s. QUANTIDADE fornecida = %s.', self.limites.minimo, self.limites.maximo, quantidade)

    def dezenas_sao_validas(self, dezenas: list[int]) -> bool:
        if dezenas is None:
            logger.error('DEZENAS não pode ser None')
            return False

        qtd, mid, mad = len(dezenas), min(dezenas), max(dezenas)
        validar = True
        if not (self.limites.minimo <= qtd <= self.limites.maximo):
            logger.error(
                'QUANTIDADE incorreta de dezenas. QUANTIDADE deve obedecer limites: %s <= QUANTIDADE <= %s. QUANTIDADE fornecida = %s.', self.limites.minimo, self.limites.maximo, qtd)
            validar = False
        if not (mid >= self.limites.menor):
            logger.error(
                'MENOR dezena deve ser >= %s. MENOR dezena fornecida = %s.', self.limites.menor, mid)
            validar = False
        if not (mad <= self.limites.maior):
            logger.error(
                'MAIOR dezena deve ser <= %s. MAIOR dezena fornecida = %s.', self.limites.maior, mad)
            validar = False
        if not (len(set(dezenas)) == qtd):
            logger.error('DEZENAS não podem ser repetidas.')
            validar = False

        if validar:
            logger.debug('Dezenas fornecidas são válidas para %s.', self.nome_apresentacao)
        return validar

    def escolher_dezenas(self) -> list[int]:
        done = False
        escolha = '1'
        dezenas = self.surpresinha()
        while not done:
            logger.info('%s: %s', self.nome_apresentacao.upper(), " ".join(map(str, dezenas)))
            escolha = input(
                f'[1] Gerar novas dezenas  [2] Confirmar  [3] Sair: ')
            match escolha:
                case '1':
                    dezenas = self.surpresinha()
                case '2' | '':
                    return dezenas
                case '3':
                    done = True

    def busca_e_registra_resultado(self) -> Resultado:
        resultado = self.buscar_resultado_online()
        self.salvar_resultado(resultado)
        return resultado

    def buscar_resultado_online(self, concurso: int = None) -> Resultado:
        logger.debug('Buscando resultado da %s. Concurso: %s', self.nome_apresentacao, concurso if concurso else "ÚLTIMO")
        url = f'https://loteriascaixa-api.herokuapp.com/api/{self.nome}/{concurso if concurso else "latest"}'
        with urllib.request.urlopen(url) as req:
            resultado = json.load(req)
            return Resultado.from_json(resultado)
        logger.error('Erro ao procurar resultado online. URL usada: %s', url)

    def salvar_resultado(self, resultado: Resultado) -> None:
        if resultado:
            self._rdb.registrar_resultado(resultado)
            logger.info('Resultado salvo com sucesso!')
        else:
            logger.error('Não foi possível salvar o resultado.')

    def encerrar(self):
        self._adb.close_db()
        self._rdb.close_db()
        logger.debug('Loteria %s encerrada.', self.nome_apresentacao)


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
