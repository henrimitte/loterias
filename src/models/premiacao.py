from dataclasses import dataclass, field


@dataclass(order=False)
class Premiacao:
    descricao: str
    faixa: int = field(compare=True)
    ganhadores: int
    valorPremio: float
