from services.tcpService import TCPService

from checkFile import CheckFileService
from fileTransfer import FileTransferService
from threadPool import ThreadPool


class FileService():
    def __init__(self, ip, port, node_list, directory, timeout):
        self.check_file_service = CheckFileService(
            ip=ip,
            port=3001,
            nodes=node_list,
            timeout=timeout,
            directory=directory,
        )
        self.file_transfer_service = FileTransferService(
            ip=ip,
            port=3002,
            directory=directory
        )
        self.directory = directory
        self.threadpool = ThreadPool(2)

    def start_service(self):
        self.threadpool.add_task(self.check_file_service.start_server, ('', 0))
        self.threadpool.wait_completion()

    def get_file(self, file_path):
        fastest_node = self.check_file_service.process_get_file_request(
            file_path=file_path
        )
        requested_file = self.file_transfer_service.get_file_from_node(
            node_ip=fastest_node["node"],
            node_port=fastest_node["node_port"],
            file_path=file_path
        )
        self.save_file(requested_file)

    def save_file(self, file_path, file_to_be_saved):
        with open(file_path) as f:
            f.write(file_to_be_saved)
