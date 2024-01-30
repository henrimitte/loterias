import json
import urllib.request

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from random import sample

from config import config_logger
from db import ApostaDB, ResultadoDB
from models import Aposta, Resultado


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

    def criar_aposta(self, dezenas: list[int] = None, concurso: int = None, jogos: int = 1) -> None:
        if not concurso:
            logger.debug('CONCURSO não fornecido.')
            if not self.resultados_estao_atualizados:
                self.busca_e_registra_resultado()
            concurso = self.proximo_concurso
        if not concurso:
            logger.error('Não foi possível definir o concurso da aposta. Aposta não foi registrada.', self.nome_apresentacao)
            return

        if not dezenas:
            logger.debug('DEZENAS não fornecidas.')
            dezenas = self.escolher_dezenas()
        if not self.dezenas_sao_validas(dezenas):
            return

        try:
            if jogos:
                logger.debug(
                    'Aposta %s de %s dezenas, concurso %s até %s criada com sucesso!', self.nome_apresentacao, len(dezenas), concurso, concurso + (jogos - 1))
                apostas = [Aposta(loteria=self.nome, concurso=n, dezenas=dezenas) for n in range(concurso, concurso + jogos)]
                self._adb.registrar_apostas(apostas)
            else:
                logger.debug(
                    'Aposta %s de %s dezenas, concurso %s criada com sucesso!', self.nome_apresentacao, len(dezenas), concurso)
                aposta = Aposta(loteria=self.nome, concurso=concurso, dezenas=dezenas)
                self.salvar_aposta(aposta)
        except Exception as e:
            logger.error('A aposta não foi criada.')

    def salvar_aposta(self, aposta: Aposta) -> None:
        if aposta:
            self._adb.registrar_aposta(aposta)
            logger.info('Aposta foi salva.')
        else:
            logger.error('Não foi possível salvar a aposta.')

    def listar_apostas(self, concurso: int = None) -> None:
        if concurso:
            apostas = self._adb.ler_apostas_por_loteria_e_concurso(self.nome, concurso)
        else:
            apostas = self._adb.ler_apostas_por_loteria(self.nome)
        if not apostas:
            logger.info('Nenhuma aposta da %s registrada', self.nome_apresentacao)
            return
        logger.info('Listando apostas da %s', self.nome_apresentacao)
        print('ID | CONCURSO | DEZENAS | ACERTOS | PREMIAÇÃO (R$)')
        for aposta in apostas:
            self.apresentar_aposta(aposta)

    def apresentar_aposta(self, aposta: Aposta) -> None:
        nums_coloridos = self._coloriza_dezenas(aposta)
        print(f'{aposta._id:0>2}',
              aposta.concurso,
              nums_coloridos,
              f'{aposta.quantidadeAcertos:>2}',
              aposta.valorPremiacao,
              sep=' | ')

    def _coloriza_dezenas(self, aposta: Aposta) -> list[str]:
        if not aposta.quantidadeAcertos:
            return ' '.join(map(lambda n: f'{n:0>2}', aposta.dezenas))
        nums_coloridos = []
        for n in aposta.dezenas:
            if n not in aposta.dezenasAcertadas:
                n_colorido = '\033[37m' + f'{n:0>2}' + '\033[m'
            else:
                n_colorido = '\033[1;30;42m' + f'{n:0>2}' + '\033[m'
            nums_coloridos.append(n_colorido)
        return ' '.join(nums_coloridos)

    @property
    def resultados_estao_atualizados(self) -> bool:
        resultado = self._rdb.ultimo_resultado_registrado_por_loteria(self.nome)
        if not resultado:
            return False
        data_prox_sorteio = datetime.strptime(resultado.dataProximoConcurso + ' 21:30', '%d/%m/%Y %H:%M')
        atualizado = data_prox_sorteio >= datetime.today()
        logger.debug('Resultados da %s estão atualizados? %s', self.nome_apresentacao, 'Sim' if atualizado else 'Não')
        return atualizado

    @property
    def ultimo_concurso_sorteado(self) -> int:
        if self.resultados_estao_atualizados:
            resultado = self._rdb.ultimo_resultado_registrado_por_loteria(self.nome)
            return resultado.concurso
        resultado = self.busca_e_registra_resultado()
        if resultado:
            return resultado.concurso

    @property
    def proximo_concurso(self) -> int:
        ucs = self.ultimo_concurso_sorteado
        return ucs + 1 if ucs else None

    def conferir_apostas(self, concurso: int = None) -> None:
        if concurso:
            apostas = [ap for ap in self._adb.ler_apostas_por_loteria_e_concurso(self.nome, concurso) if not ap.conferida]
        else:
            apostas = [ap for ap in self._adb.ler_apostas_por_loteria(self.nome) if not ap.conferida]
        ultimo = self.ultimo_concurso_sorteado
        if not apostas:
            logger.debug('Nenhuma aposta para conferir.')
        for aposta in apostas:
            if aposta.concurso <= ultimo:
                logger.debug('Conferindo aposta %s da %s para o concurso %s.', aposta.dezenas, self.nome_apresentacao, aposta.concurso)
                self.confere_resultado_aposta(aposta)

    def confere_resultado_aposta(self, aposta: Aposta) -> None:
        resultado = self._rdb.ler_resultado_por_loteria_e_concurso(aposta.loteria, aposta.concurso) or self.busca_e_registra_resultado(aposta.concurso)
        if not resultado:
            logger.debug('Não foi possível obter o resultado da loteria %s para o concurso %s. Aposta não conferida.', aposta.loteria, aposta.concurso)
            return
        aposta.dezenasAcertadas = sorted(set(map(int, resultado.dezenas)) & set(aposta.dezenas))
        aposta.quantidadeAcertos = len(aposta.dezenasAcertadas)
        aposta.conferida = True
        aposta.valorPremiacao = 0.0
        self._adb.atualizar_aposta(aposta)

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

    def busca_e_registra_resultado(self, concurso: int = None) -> Resultado:
        resultado = self.buscar_resultado_online(concurso)
        self.salvar_resultado(resultado)
        return resultado

    def buscar_resultado_online(self, concurso: int = None) -> Resultado:
        if concurso is not None and concurso <= 0:
            logger.error('Concurso deve ser MAIOR que 0.')
        logger.debug('Buscando resultado da %s. Concurso: %s', self.nome_apresentacao, concurso if concurso else "ÚLTIMO")
        url = f'https://loteriascaixa-api.herokuapp.com/api/{self.nome}/{concurso if concurso else "latest"}'
        try:
            with urllib.request.urlopen(url) as req:
                resultado = json.load(req)
                return Resultado.from_json(resultado)
        except Exception as e:
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
