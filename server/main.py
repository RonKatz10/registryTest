import socket
from registryHandler import RegistryHandler

class Server:
    def __init__(self, port: int) -> None:
        self.reg_handler = RegistryHandler()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))

        self.sockets = []

    def handle_clients(self):
        self.server_socket.listen()

        while True:
            client_soc, client_addr = self.server_socket.accept()
            formatted_addr = f'{client_addr[0]}:{client_addr[1]}'
            print(f'{formatted_addr} connected')
            call_counter = self.update_registry_counter(formatted_addr)

            number = client_soc.recv(1024).decode()
            print(number)

            client_soc.send(str(call_counter).encode())
            client_soc.close()

    def update_registry_counter(self, address):
        return self.reg_handler.increment_or_create_counter(address)


if __name__ == '__main__':
    s = Server(8080)
    s.handle_clients()