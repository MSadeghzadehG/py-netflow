from discovery import DiscoveryService
from threadpool import ThreadPool


def main():
    main_pool = ThreadPool(2)
    discovery_service = DiscoveryService(
        ip="127.0.0.1",
        port=3000,
        initial_nodes=["0.0.0.0", "localhost"],
        period=5
    )
    main_pool.wait_completion()

if __name__ == "__main__":
    main()
