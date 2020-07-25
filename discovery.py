import socket
import sys
import ast

from time import sleep
from threadpool import ThreadPool


class DiscoveryService():

    def __init__(self, ip, port, initial_nodes, period):
        self.period = period
        self.buffer_size = 1024
        self.ip = ip
        self.port = port
        self.nodes = initial_nodes
        # Create a datagram socket
        self.client_discovery_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )
        self.threadpool = ThreadPool(2)
        self.threadpool.add_task(self.discovery_job)
        self.threadpool.add_task(self.start_discovery_server)
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

    def get_nodes(self):
        return self.nodes

    def start_discovery_server(self):
        # Create a datagram socket
        server_discovery_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM
        )
        # Bind to address and ip
        print(server_discovery_socket)
        server_identifier = (self.ip, self.port)
        server_discovery_socket.bind(server_identifier)
        print(
            "Discovery service's server up and listening on " +
            str(server_identifier)
        )
        # Listen for incoming datagrams
        while(True):
            message_pair = server_discovery_socket.recvfrom(
                self.buffer_size
            )
            message = message_pair[0]
            address = message_pair[1]
            self.update_nodes(ast.literal_eval(message.decode('utf-8')))
            print(
                "Nodes list updated by Discovery service's server: " +
                str(self.nodes)
            )

    def send_nodes_to_others(self):
        message = str(self.nodes)
        bytes_to_send = str.encode(message, 'utf-8')
        for node in self.nodes:
            self.send_nodes_to_one(node, bytes_to_send)

    def send_nodes_to_one(self, node_ip, byte_message):
        server_identifier = (node_ip, self.port)
        self.client_discovery_socket.sendto(byte_message, server_identifier)
