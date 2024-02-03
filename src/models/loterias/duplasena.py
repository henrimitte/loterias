from .loteria import Limites, Loteria, Loterias


class DuplaSena(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.DUPLASENA, nome_apresentacao='Dupla-Sena',
                         limites=Limites(1, 50, 6, 15), faixas=4)
