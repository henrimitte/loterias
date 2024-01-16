import argparse


from loterias import opcoes_loterias, loteria_factory


def escolher_dezenas(loteria) -> list[int]:
    done = False
    escolha = '1'
    dezenas = loteria.surpresinha()
    while not done:
        print(f'{loteria.nome_apresentacao.upper():=^20}')
        print(*dezenas, sep=' ')
        escolha = input(
            f'[1] Gerar novas dezenas  [2] Confirmar  [3] Sair: ')
        match escolha:
            case '1':
                dezenas = loteria.surpresinha()
            case '2' | '':
                done = True
                return dezenas
            case '3':
                done = True


def main(args):
    parser = argparse.ArgumentParser(prog='loteria')
    parser.add_argument('loteria', choices=opcoes_loterias)
    parser.add_argument('-d', '--dezenas', type=int, nargs='*')
    parser.add_argument('-c', '--concurso', type=int, nargs='?')
    args = parser.parse_args(args.split())

    loteria = loteria_factory(args.loteria)

    if not args.dezenas:
        args.dezenas = escolher_dezenas(loteria)

    if args.dezenas:
        aposta = loteria.criar_aposta(args.dezenas, args.concurso)
        loteria.salvar_aposta(aposta)

    loteria._adb.close_db()


if __name__ == '__main__':
    main('mega -c 2675')
