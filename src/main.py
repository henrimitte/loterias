import argparse


from loterias import opcoes_loterias, loteria_factory





def main():
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    parser.add_argument('-d', '--dezenas', type=int, nargs='*')
    parser.add_argument('-c', '--concurso', type=int)
    parser.add_argument('-l', '--listar', action='store_true')

    args = parser.parse_args()
    loteria = loteria_factory(args.loteria)

    if args.listar:
        loteria.listar_apostas(args.concurso)
    else:
        aposta = loteria.criar_aposta(args.dezenas, args.concurso)
        loteria.salvar_aposta(aposta)

    loteria.encerrar()


if __name__ == '__main__':
    main()
