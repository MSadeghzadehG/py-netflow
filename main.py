from discovery import Discovery
from threadpool import ThreadPool


def main():
    main_pool = ThreadPool(2)

    discovery_service = Discovery("127.0.0.1", 3000, ["0.0.0.0", "localhost"], 5)
    main_pool.add_task(discovery_service.start_discovery_server)
    for i in range(10):
        discovery_service.send_nodes_to_others()
    main_pool.wait_completion()

if __name__ == "__main__":
    main()
