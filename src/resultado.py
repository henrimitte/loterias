import json

from dataclasses import dataclass, field


@dataclass
class Resultado:
    '''Retorna um Resultado das Loterias Caixa.'''
    acumulou: bool
    concurso: int
    data: str
    dataProximoConcurso: str
    dezenas: list[str]
    dezenasOrdemSorteio: list[str]
    estadosPremiados: list
    local: str
    localGanhadores: list
    loteria: str
    mesSorte: str
    observacao: str
    premiacoes: list[dict]
    proximoConcurso: int
    timeCoracao: str
    trevos: list[str]
    valorAcumuladoConcursoEspecial: float
    valorAcumuladoConcurso_0_5: float
    valorAcumuladoProximoConcurso: float
    valorArrecadado: float
    valorEstimadoProximoConcurso: int
    _id: int = field(repr=False, default=None)

    def to_db(self) -> dict:
        '''Exporta como dicionário para salvar no Banco de Dados.'''
        return {'acumulou': self.acumulou,
                'concurso': self.concurso, 
                'data': self.data, 
                'dataProximoConcurso': self.dataProximoConcurso, 
                'dezenas': json.dumps(self.dezenas), 
                'dezenasOrdemSorteio': json.dumps(self.dezenasOrdemSorteio), 
                'estadosPremiados': json.dumps(self.estadosPremiados), 
                'local': self.local, 
                'localGanhadores': json.dumps(self.localGanhadores), 
                'loteria': self.loteria, 
                'mesSorte': self.mesSorte, 
                'observacao': self.observacao, 
                'premiacoes': json.dumps(self.premiacoes), 
                'proximoConcurso': self.proximoConcurso, 
                'timeCoracao': self.timeCoracao, 
                'trevos': json.dumps(self.trevos), 
                'valorAcumuladoConcursoEspecial': self.valorAcumuladoConcursoEspecial, 
                'valorAcumuladoConcurso_0_5': self.valorAcumuladoConcurso_0_5, 
                'valorAcumuladoProximoConcurso': self.valorAcumuladoProximoConcurso, 
                'valorArrecadado': self.valorArrecadado, 
                'valorEstimadoProximoConcurso': self.valorEstimadoProximoConcurso}

    @classmethod
    def from_db(cls, resultado):
        '''Retorna um Resultado a partir de uma querry do Banco de Dados.'''
        if resultado: 
            return Resultado(
                _id= resultado[0],
                acumulou = bool(resultado[1]),
                concurso = resultado[2],
                data = resultado[3],
                dataProximoConcurso = resultado[4],
                dezenas = json.loads(resultado[5]),
                dezenasOrdemSorteio = json.loads(resultado[6]),
                estadosPremiados = json.loads(resultado[7]),
                local = resultado[8],
                localGanhadores = json.loads(resultado[9]),
                loteria = resultado[10],
                mesSorte = resultado[11],
                observacao = resultado[12],
                premiacoes = json.loads(resultado[13]),
                proximoConcurso = resultado[14],
                timeCoracao = resultado[15],
                trevos = json.loads(resultado[16]),
                valorAcumuladoConcursoEspecial = resultado[17],
                valorAcumuladoConcurso_0_5 = resultado[18],
                valorAcumuladoProximoConcurso = resultado[19],
                valorArrecadado = resultado[20],
                valorEstimadoProximoConcurso = resultado[21],)

    @classmethod
    def from_json(cls, resultado):
        if resultado:
            return Resultado(
                acumulou = bool(resultado['acumulou']),
                concurso = resultado['concurso'],
                data = resultado['data'],
                dataProximoConcurso = resultado['dataProximoConcurso'],
                dezenas = resultado['dezenas'],
                dezenasOrdemSorteio = resultado['dezenasOrdemSorteio'],
                estadosPremiados = resultado['estadosPremiados'],
                local = resultado['local'],
                localGanhadores = resultado['localGanhadores'],
                loteria = resultado['loteria'],
                mesSorte = resultado['mesSorte'],
                observacao = resultado['observacao'],
                premiacoes = resultado['premiacoes'],
                proximoConcurso = resultado['proximoConcurso'],
                timeCoracao = resultado['timeCoracao'],
                trevos = resultado['trevos'],
                valorAcumuladoConcursoEspecial = resultado['valorAcumuladoConcursoEspecial'],
                valorAcumuladoConcurso_0_5 = resultado['valorAcumuladoConcurso_0_5'],
                valorAcumuladoProximoConcurso = resultado['valorAcumuladoProximoConcurso'],
                valorArrecadado = resultado['valorArrecadado'],
                valorEstimadoProximoConcurso = int(resultado['valorEstimadoProximoConcurso']),)