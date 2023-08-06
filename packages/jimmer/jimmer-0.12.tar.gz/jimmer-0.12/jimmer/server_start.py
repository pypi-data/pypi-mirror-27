import argparse
from server.server import Server
from config.config_common import DEFAULT_ADDRESS, DEFAULT_PORT
from config.config_common import SERVER_ADDRESS_HELP, SERVER_PORT_HELP

if __name__ == '__main__':
    server = None
    address = 'address'
    port = 'port'
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, dest=address, default=DEFAULT_ADDRESS, help=SERVER_ADDRESS_HELP)
    parser.add_argument('-p', type=str, dest=port, default=DEFAULT_PORT, help=SERVER_PORT_HELP)
    try:
        host = parser.parse_args().address
        port = parser.parse_args().port
    except SystemExit:
        host = DEFAULT_ADDRESS
        port = DEFAULT_PORT

    server = Server(host=host, port=port).start()
