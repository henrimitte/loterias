import argparse

from utils import limpar_tudo


from models.loterias import opcoes_loterias, loteria_factory


def main():
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    parser.add_argument('-d', '--dezenas', type=int, nargs='*')
    parser.add_argument('-c', '--concurso', type=int)
    parser.add_argument('-j', '--jogos', type=int)
    parser.add_argument('-l', '--listar', action='store_true')
    parser.add_argument('-r', '--resultado', action='store_true')

    args = parser.parse_args()
    loteria = loteria_factory(args.loteria)

    if args.resultado:
        loteria.conferir_apostas(args.concurso)

    if args.listar:
        loteria.listar_apostas(args.concurso)

    if not args.resultado and not args.listar:
        aposta = loteria.criar_aposta(args.dezenas, args.concurso, args.jogos)

    loteria.encerrar()


if __name__ == '__main__':
    main()
