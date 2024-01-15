import json

from dataclasses import dataclass, field


@dataclass
class Aposta:
    loteria: str
    concurso: int
    dezenas: list[int]
    conferida: bool = field(default=False)
    quantidadeAcertos: int = field(default=0)
    dezenasAcertadas: list[int] = field(default_factory=list)
    valorPremiacao: float = field(default=0.0)
    _id: int = field(repr=False, default=None)

    def to_db(self) -> dict:
        return {'loteria': self.loteria,
                'concurso': self.concurso,
                'dezenas': json.dumps(self.dezenas),
                'conferida': self.conferida,
                'quantidadeAcertos': self.quantidadeAcertos,
                'dezenasAcertadas': json.dumps(self.dezenasAcertadas),
                'valorPremiacao': self.valorPremiacao, }

    @classmethod
    def from_db(cls, aposta):
        return Aposta(_id=aposta[0],
                      loteria=aposta[1],
                      concurso=aposta[2],
                      dezenas=json.loads(aposta[3]),
                      conferida=bool(aposta[4]),
                      quantidadeAcertos=aposta[5],
                      dezenasAcertadas=json.loads(aposta[6]),
                      valorPremiacao=aposta[7],)
