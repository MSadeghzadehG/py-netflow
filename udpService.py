import socket

from abc import ABC


class UDPService(ABC):

    def __init__(self, name, ip, port, buffer_size=1024):
        self.name = name
        self.buffer_size = buffer_size
        self.ip = ip
        self.port = port
        # Create a datagram socket
        self.client_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )

    def parse_message(self, message, address):
        pass

    def start_service(self):
        pass

    def start_server(self):
        # Create a datagram socket
        server_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )
        # Bind to address and ip
        server_identifier = (self.ip, self.port)
        server_socket.bind(server_identifier)
        print(
            self.name +
            " service's UDP server up and listening on " +
            str(server_identifier)
        )
        # Listen for incoming datagrams
        while(True):
            message_pair = server_socket.recvfrom(self.buffer_size)
            self.parse_message(
                message=message_pair[0], address=message_pair[1]
            )

    def send_message(self, ip, byte_message):
        server_identifier = (ip, self.port)
        self.client_socket.sendto(byte_message, server_identifier)
