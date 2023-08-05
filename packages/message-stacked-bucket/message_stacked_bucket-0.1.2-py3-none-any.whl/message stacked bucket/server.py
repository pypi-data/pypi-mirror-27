import sys
from b_server.server_main import MyMessServer


'''
Главный скрипт для старта сервера
'''
if __name__ == '__main__':
    print('Запускаю сервер')
    # Получаем аргументы скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    name = 'server'
    server = MyMessServer(name, addr, port)
    server.main_loop()
