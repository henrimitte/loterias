from .loteria import Limites, Loteria, Loterias


class Lotomania(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.LOTOMANIA, nome_apresentacao='Lotomania',
                         limites=Limites(1, 100, 50, 50), faixas=6)
