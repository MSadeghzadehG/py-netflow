from checkFile import CheckFileService
from discovery import DiscoveryService
from threadPool import ThreadPool


def main():
    node_list = ["0.0.0.0", "localhost"]
    main_pool = ThreadPool(2)
    discovery_service = DiscoveryService(
        ip="127.0.0.1",
        port=3000,
        initial_nodes=node_list,
        period=5
    )
    check_file_service = CheckFileService(
        ip="127.0.0.1",
        port=3001,
        nodes=node_list,
        timeout=0.0004,
        directory='files/'
    )
    main_pool.add_task(discovery_service.start_service)
    main_pool.add_task(check_file_service.start_service)
    from time import sleep
    sleep(1)
    print(check_file_service.get_nodes_response_times('hello.txt'))
    main_pool.wait_completion()

if __name__ == "__main__":
    main()
