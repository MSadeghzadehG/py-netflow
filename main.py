from discovery import DiscoveryService
from threadPool import ThreadPool


def main():
    node_list = ["127.0.0.1", "localhost"]
    main_pool = ThreadPool(2)
    discovery_service = DiscoveryService(
        ip="127.0.0.1",
        port=3000,
        initial_nodes=node_list,
        period=5
    )
    main_pool.add_task(discovery_service.start_service)
    
    main_pool.wait_completion()

if __name__ == "__main__":
    main()
