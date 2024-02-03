from .loteria import Limites, Loteria, Loterias


class MegaSena(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.MEGASENA, nome_apresentacao='Mega-Sena',
                         limites=Limites(1, 60, 6, 20), faixas=3)
