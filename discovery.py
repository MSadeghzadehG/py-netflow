import ast

from time import sleep

from threadPool import ThreadPool
from services.udpService import UDPService


class DiscoveryService(UDPService):

    def __init__(self, ip, port, initial_nodes, period):
        super(DiscoveryService, self).__init__(
            name='Discovery',
            ip=ip,
            port=port
        )
        self.period = period
        self.nodes = initial_nodes
        self.threadpool = ThreadPool(2)

    def start_service(self):
        self.threadpool.add_task(self.discovery_job)
        self.threadpool.add_task(self.start_server)
        self.threadpool.wait_completion()

    def discovery_job(self):
        while True:
            self.send_nodes_to_others()
            sleep(self.period)

    def update_nodes(self, discovered_list):
        for discovered_node in discovered_list:
            if (
                discovered_node not in self.nodes and
                discovered_node is not self.ip
            ):
                self.nodes.append(discovered_node)

    def process_server_response(self, message, address):
        self.update_nodes(ast.literal_eval(message))
        print(
            "Nodes list updated by Discovery service's server: " +
            str(self.nodes)
        )

    def send_nodes_to_others(self):
        message = str(self.nodes)
        for node in self.nodes:
            self.send_message(
                str_message=message,
                address=(node, self.port),
                socket=self.client_socket
            )
