import argparse


from loterias import opcoes_loterias


def main(args):
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    args = parser.parse_args(args.split())

    loteria = opcoes_loterias[args.loteria]
    loteria._adb.close_db()

if __name__ == '__main__':
    main('mega')
