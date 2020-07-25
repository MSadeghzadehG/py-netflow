from socket import timeout
from os import path
from time import time

from threadPool import ThreadPool
from udpService import UDPService


class CheckFileService(UDPService):

    def __init__(self, ip, port, nodes, timeout, directory):
        super(CheckFileService, self).__init__(
            name='CheckFile',
            ip=ip,
            port=port
        )
        self.nodes = nodes
        self.directory = directory
        self.client_socket.settimeout(timeout)
        self.threadpool = ThreadPool(2)

    def start_service(self):
        self.threadpool.add_task(self.start_server)
        self.threadpool.wait_completion()

    def process_server_response(self, message, address):
        file_existance = str(self.check_file_existance(message))
        self.send_message(
            str_message=file_existance,
            address=address,
            socket=self.server_socket
        )

    def check_file_existance(self, file_path):
        return path.exists(self.directory + '/' + file_path)

    def get_nodes_response_times(self, file_path):
        message = file_path
        response_times = []
        for node in self.nodes:
            if node is not self.ip:
                address = (node, self.port)
                start_time = time()
                self.send_message(
                    str_message=message,
                    address=address,
                    socket=self.client_socket
                )
                try:
                    response = self.get_message(self.client_socket)
                    # print(response)
                    if response["message"] == "True":
                        response_times.append((node, time() - start_time))
                except timeout:
                    print(node + " node timed out")
                    pass
        print(response_times)
        if response_times:
            return min(response_times, key=lambda t: t[1])[0]
        else:
            return None
