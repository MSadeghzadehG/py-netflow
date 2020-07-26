from discovery import DiscoveryService
from fileService import FileService
from threadPool import ThreadPool


def main():
    node_list = ["0.0.0.0", "localhost"]
    main_pool = ThreadPool(3)
    discovery_service = DiscoveryService(
        ip="127.0.0.1",
        port=3000,
        initial_nodes=node_list,
        period=5
    )
    file_service = FileService(
        ip="127.0.0.1",
        port=3001,
        node_list=node_list,
        directory='files/',
        timeout=5
    )

    main_pool.add_task(discovery_service.start_service)
    main_pool.add_task(file_service.start_service)
    main_pool.wait_completion()

if __name__ == "__main__":
    main()
