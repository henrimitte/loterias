from .loteria import Loteria, Loterias
from .duplasena import DuplaSena
from .lotofacil import Lotofacil
from .lotomania import Lotomania
from .megasena import MegaSena
from .quina import Quina


opcoes_loterias = [
    Loterias.DUPLASENA, 
    Loterias.LOTOFACIL, 
    Loterias.LOTOMANIA, 
    Loterias.MEGASENA, 
    Loterias.QUINA]


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
