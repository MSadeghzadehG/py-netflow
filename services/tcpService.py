import socket

from . import Service


class TCPService(Service):

    def __init__(self, **kwargs):
        super(TCPService, self).__init__(
            **kwargs,
            socket_type=socket.SOCK_STREAM
        )

    def process_server_response(self, message, address):
        pass

    def start_service(self):
        pass

    def start_server(self, address=None):
        super(TCPService, self).start_server(address)
        self.server_socket.listen(5)
        connection, address = self.server_socket.accept()
        while True:
            message = self.get_message(connection)
            self.process_server_response(message=message, address=address)

    def get_message(self, socket):
        message = socket.recv(self.buffer_size).decode(self.encoding)
        socket.close()
        return message

    def send_message(self, str_message, address, socket):
        byte_message = str.encode(str_message, self.encoding)
        socket.connect(address)
        socket.send(byte_message)
