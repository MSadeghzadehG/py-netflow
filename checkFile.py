from socket import timeout
from os import path
from time import time

from threadPool import ThreadPool
from services.udpService import UDPService


class CheckFileService(UDPService):

    def __init__(self, ip, port, nodes, timeout, directory, file_transfer_service):
        super(CheckFileService, self).__init__(
            name='CheckFile',
            ip=ip,
            port=port
        )
        self.nodes = nodes
        self.directory = directory
        self.client_socket.settimeout(timeout)
        self.threadpool = ThreadPool(2)
        self.file_transfer_service = file_transfer_service

    def start_service(self):
        self.threadpool.add_task(self.start_server)
        self.threadpool.wait_completion()

    def process_server_response(self, message, address):
        file_existance = str(self.check_file_existance(message))
        tcp_server_port = str(self.file_transfer_service.get_server_port())
        self.send_message(
            str_message=file_existance + ',' + tcp_server_port,
            address=address,
            socket=self.server_socket
        )

    def check_file_existance(self, file_path):
        return path.exists(self.directory + '/' + file_path)

    def get_nodes_response_times(self, file_request_message):
        nodes_responses = []
        for node in self.nodes:
            if node is not self.ip:
                address = (node, self.port)
                start_time = time()
                self.send_message(
                    str_message=file_request_message,
                    address=address,
                    socket=self.client_socket
                )
                try:
                    response = self.get_message(self.client_socket)
                    nodes_responses.append(
                        {
                            "node": node,
                            "response": response,
                            "response_time": time() - start_time
                        }
                    )
                except timeout:
                    print(node + " node timed out")
                    pass
        return nodes_responses

    def process_get_file_request(self, file_path):
        file_request_message = file_path
        nodes_responses = self.get_nodes_response_times(file_request_message)
        nodes_has_file = []
        for node_response in nodes_responses:
            response_message = nodes_responses["response"]["message"].split(',')
            node_has_file = response_message[0] == "True"
            if node_has_file:
                nodes_has_file.append(
                    {
                        "node": node_response["node"], 
                        "node_port": response_message[1],
                        "response_time": node_response["response_time"]
                    }
                )
        if nodes_has_file is not None:
            return min(nodes_has_file, key=lambda t: t["response_time"])
        else:
            return None
