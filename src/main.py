import argparse


from loterias import opcoes_loterias, loteria_factory


def main(args):
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    parser.add_argument('-d', '--dezenas', type=int, nargs='*')
    parser.add_argument('-c', '--concurso', type=int, nargs='?')
    args = parser.parse_args(args.split())

    loteria = loteria_factory(args.loteria)
    registrar_aposta = True

    if not args.dezenas:
        escolha = '1'
        while escolha not in '23':
            args.dezenas = loteria.surpresinha()
            print(*args.dezenas, sep=' ')
            escolha = input(
                f'[1] Gerar novas dezenas  [2] Confirmar  [3] Sair: ')[0]
            if escolha == '3':
                registrar_aposta = False

    if registrar_aposta:
        aposta = loteria.criar_aposta(args.dezenas, args.concurso)

    loteria._adb.close_db()


if __name__ == '__main__':
    main('mega -c 2675')
