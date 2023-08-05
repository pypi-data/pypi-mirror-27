import argparse


def get_params():
    '''параметры запуска сервера'''
    parser = argparse.ArgumentParser(description="Параметры для чат сервера")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-addr", type=str, default="localhost",
                       help="Задать IP адресс для прослушивания - по умолчанию все")
    parser.add_argument("-port", type=int, default=7777,
                        help="Установить PORT сервера, по умолчанию 7777")
    args = parser.parse_args()

    return args.addr, args.port