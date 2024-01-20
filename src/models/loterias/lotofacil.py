from .loteria import Limites, Loteria, Loterias


class Lotofacil(Loteria):
    def __init__(self):
        super().__init__(nome=Loterias.LOTOFACIL, nome_apresentacao='Lotofácil',
                         limites=Limites(1, 25, 15, 20))
