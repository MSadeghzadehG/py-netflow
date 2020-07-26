import socket

from . import Service


class UDPService(Service):

    def __init__(self, **kwargs):
        super(UDPService, self).__init__(**kwargs, socket_type=socket.SOCK_DGRAM)

    def process_server_response(self, message, address):
        pass

    def start_service(self):
        pass

    def start_server(self, address=None):
        super(UDPService, self).start_server(address)
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
