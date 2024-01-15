import argparse


from loterias import opcoes_loterias, loteria_factory


def main(args):
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    parser.add_argument('-d', '--dezenas', type=int, nargs='*')
    args = parser.parse_args(args.split())

    loteria = loteria_factory(args.loteria)
    
    aposta = loteria.criar_aposta(args.dezenas)
    if aposta:
        print(aposta.dezenas)

    loteria._adb.close_db()

if __name__ == '__main__':
    main('mega -d 2 13 17 44 47 65')
