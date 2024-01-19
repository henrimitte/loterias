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
        dct = {'loteria': self.loteria,
               'concurso': self.concurso,
               'dezenas': json.dumps(self.dezenas),
               'conferida': self.conferida,
               'quantidadeAcertos': self.quantidadeAcertos,
               'dezenasAcertadas': json.dumps(self.dezenasAcertadas),
               'valorPremiacao': self.valorPremiacao, }
        if self._id:
            dct['_id'] = self._id
        return dct

    @classmethod
    def from_db(cls, aposta):
        return Aposta(loteria=aposta[0],
                      concurso=aposta[1],
                      dezenas=json.loads(aposta[2]),
                      conferida=bool(aposta[3]),
                      quantidadeAcertos=aposta[4],
                      dezenasAcertadas=json.loads(aposta[5]),
                      valorPremiacao=aposta[6],
                      _id=aposta[7],)
