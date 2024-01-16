import argparse


from loterias import opcoes_loterias, loteria_factory





def main():
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    parser.add_argument('-d', '--dezenas', type=int, nargs='*')
    parser.add_argument('-c', '--concurso', type=int, nargs='?')
    args = parser.parse_args()

    loteria = loteria_factory(args.loteria)

    aposta = loteria.criar_aposta(args.dezenas, args.concurso)
    if aposta:
        loteria.salvar_aposta(aposta)

    loteria._adb.close_db()


if __name__ == '__main__':
    main()
