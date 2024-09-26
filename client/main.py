import socket
import random
from ipHandler import IPHandler
from fileHandler import FileHandler
from exceptions import IPMissingError, InvalidRegistry

class Client:
    def __init__(self):
        reg_path = r"Software\CyberIsGood\Client"
        self.ipHandler = IPHandler(reg_path)
        self.fileHandler = FileHandler('call_numbers.tmp', reg_path)

        try:
            ip, port = self.ipHandler.extract_from_registry()
        except InvalidRegistry:
            print('Registry setup is invalid, run setup.bat')
            return #exit if registry is invalid
        except IPMissingError:
            ip, port = self.read_address_from_input()

        connected = self.create_socket(ip, port)
        if not connected: return #exit if connection failed

        self.commuincate_with_server()
        self.client_socket.close()

    def create_socket(self, ip: str, port: int):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind(('', 6464))
        try: 
            self.client_socket.connect((ip, port))
        except ConnectionError:
            print('Failed to connect to server')
            return False
        
        return True
    
    def commuincate_with_server(self):
        number = random.randint(1, 20000)
        self.fileHandler.write_number(number)

        self.client_socket.send(str(number).encode())
        call_counter = self.client_socket.recv(1024).decode()
        print(f'# of calls to server: {call_counter}')

    def read_address_from_input(self):
        while True:
            server_ip = input('Enter IP to server: ')
            server_port = input('Enter port to server: ')

            try:
                self.ipHandler.update_ip_port(server_ip, server_port)
            except ValueError as e:
                print(e)
            else:
                return (server_ip, int(server_port))

if __name__ == '__main__':
    Client()