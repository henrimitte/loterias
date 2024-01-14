import json


class Aposta:
    def __init__(self, loteria, concurso, dezenas, **kwargs) -> None:
        self.loteria = loteria
        self.concurso = concurso
        self.dezenas = dezenas
        self.conferida = False
        self.quantidadeAcertos = 0
        self.dezenasAcertadas = []
        self.valorPremiacao = 0.0
    
    def to_db(self) -> dict:
        return {'loteria': self.loteria,
                'concurso': self.concurso,
                'dezenas': json.dumps(self.dezenas),
                'conferida': int(self.conferida),
                'quantidadeAcertos': self.quantidadeAcertos,
                'dezenasAcertadas': json.dumps(self.dezenasAcertadas),
                'valorPremiacao': self.valorPremiacao,}

    @classmethod
    def from_db(cls, aposta):
        _, *aposta = aposta
        return Aposta(loteria=aposta[0],
                      concurso=aposta[1],
                      dezenas=json.loads(aposta[2]),
                      conferida=bool(aposta[3]),
                      quantidadeAcertos=aposta[4],
                      dezenasAcertadas=json.loads(aposta[5]),
                      valorPremiacao=aposta[6])