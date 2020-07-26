from services.tcpService import TCPService

from checkFile import CheckFileService
from threadPool import ThreadPool


class FileTransferService(TCPService):
    def __init__(self, ip, port, directory):
        super(FileTransferService, self).__init__(
            name='FileTransfer',
            ip=ip,
            port=port
        )
        self.directory = directory
        self.threadpool = ThreadPool(2)
        
    def start_service(self):
        self.threadpool.add_task(self.start_server, ('', 0))
        self.threadpool.wait_completion()

    def process_server_response(self, message, address):
        needed_file = open(self.directory + '/' + file_path)

    def get_server_port(self):
        return self.server_socket.getsockname()[1]

    def get_file_from_node(self, node_ip, node_port, file_path):
        pass
