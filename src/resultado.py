import json

from dataclasses import dataclass


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
                'valorEstimadoProximoConcurso': int(self.valorEstimadoProximoConcurso)}

    @classmethod
    def from_db(cls, resultado):
        '''Retorna um Resultado a partir de uma querry do Banco de Dados.'''
        if resultado:
            return Resultado(
                acumulou=bool(resultado[0]),
                concurso=resultado[1],
                data=resultado[2],
                dataProximoConcurso=resultado[3],
                dezenas=json.loads(resultado[4]),
                dezenasOrdemSorteio=json.loads(resultado[5]),
                estadosPremiados=json.loads(resultado[6]),
                local=resultado[7],
                localGanhadores=json.loads(resultado[8]),
                loteria=resultado[9],
                mesSorte=resultado[10],
                observacao=resultado[11],
                premiacoes=json.loads(resultado[12]),
                proximoConcurso=resultado[13],
                timeCoracao=resultado[14],
                trevos=json.loads(resultado[15]),
                valorAcumuladoConcursoEspecial=resultado[16],
                valorAcumuladoConcurso_0_5=resultado[17],
                valorAcumuladoProximoConcurso=resultado[18],
                valorArrecadado=resultado[19],
                valorEstimadoProximoConcurso=int(resultado[20]),)

    @classmethod
    def from_json(cls, resultado):
        if resultado:
            return Resultado(
                acumulou=bool(resultado['acumulou']),
                concurso=resultado['concurso'],
                data=resultado['data'],
                dataProximoConcurso=resultado['dataProximoConcurso'],
                dezenas=resultado['dezenas'],
                dezenasOrdemSorteio=resultado['dezenasOrdemSorteio'],
                estadosPremiados=resultado['estadosPremiados'],
                local=resultado['local'],
                localGanhadores=resultado['localGanhadores'],
                loteria=resultado['loteria'],
                mesSorte=resultado['mesSorte'],
                observacao=resultado['observacao'],
                premiacoes=resultado['premiacoes'],
                proximoConcurso=resultado['proximoConcurso'],
                timeCoracao=resultado['timeCoracao'],
                trevos=resultado['trevos'],
                valorAcumuladoConcursoEspecial=resultado['valorAcumuladoConcursoEspecial'],
                valorAcumuladoConcurso_0_5=resultado['valorAcumuladoConcurso_0_5'],
                valorAcumuladoProximoConcurso=resultado['valorAcumuladoProximoConcurso'],
                valorArrecadado=resultado['valorArrecadado'],
                valorEstimadoProximoConcurso=int(resultado['valorEstimadoProximoConcurso']),)
