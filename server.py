import multiprocessing
import socket

from command import CommandDistribution

class Server:
    def __init__(self, address, port:int, timeout:int = 5):
        self._is_running = False
        self.server_inet_address = (address, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = timeout
        self.run()

    def run(self):
        self._is_running = True
        self.server_socket.bind(self.server_inet_address)
        self.server_socket.listen()
        print(f"Server started at {self.server_inet_address}")
        while self._is_running:
            connection, client_inet_address = self.server_socket.accept()
            multiprocessing.Process(target=ClientHandler, args=(connection, client_inet_address, self.timeout)).start()

class ClientHandler:
    def __init__(self, connection, client_inet_address, timeout):
        self.connection = connection
        self.timeout = timeout
        self.ip = client_inet_address
        self.commandHandling = CommandDistribution()
        self.client()

    def client(self):
        self.connection.settimeout(self.timeout)
        with self.connection:
            while True:
                data = self.connection.recv(256)
                if not data:
                    break

                response = self.commandHandling.distribute(data)
                self.log(response)
                self.connection.sendall((response + "\n").encode("utf-8"))

    def log(self, operation:str):
        with open("log.txt", "a") as f:
            f.write(f"{operation} from {self.ip}\n")