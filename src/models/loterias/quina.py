from .loteria import Limites, Loteria, Loterias


class Quina(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.QUINA, nome_apresentacao='Quina',
                         limites=Limites(1, 80, 5, 15))
