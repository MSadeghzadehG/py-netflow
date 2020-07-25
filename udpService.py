import socket

from abc import ABC


class UDPService(ABC):

    def __init__(self, name, ip, port, buffer_size=1024, encoding='utf-8'):
        self.name = name
        self.buffer_size = buffer_size
        self.encoding = encoding
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )
        self.client_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )

    def process_server_response(self, message, address):
        pass

    def start_service(self):
        pass

    def start_server(self):
        # Bind to address and ip
        address = (self.ip, self.port)
        self.server_socket.bind(address)
        print(
            self.name +
            " service's UDP server up and listening on " +
            str(address)
        )
        while(True):
            request = self.get_message(self.server_socket)
            self.process_server_response(**request)

    def get_message(self, socket):
        # Listen for incoming datagrams
        message_pair = socket.recvfrom(self.buffer_size)
        return {
            "message": message_pair[0].decode(self.encoding),
            "address": message_pair[1]
        }

    def send_message(self, str_message, address, socket):
        byte_message = str.encode(str_message, self.encoding)
        socket.sendto(byte_message, address)
