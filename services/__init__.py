import socket

from abc import ABC


class Service(ABC):

    def __init__(
        self, name, ip, port, socket_type, buffer_size=1024, encoding='utf-8'
    ):
        self.name = name
        self.buffer_size = buffer_size
        self.encoding = encoding
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(
            family=socket.AF_INET, type=socket_type
        )
        self.client_socket = socket.socket(
            family=socket.AF_INET, type=socket_type
        )

    def process_server_response(self, message, address):
        pass

    def start_service(self):
        pass

    def start_server(self, address=None):
        # Bind to address and ip
        address = address or (self.ip, self.port)
        self.server_socket.bind(address)
        print(
            self.name +
            " service's server up and listening on " +
            str(address)
        )

    def get_message(self, socket):
        pass

    def send_message(self, str_message, address, socket):
        pass
