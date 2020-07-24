from threadpool import ThreadPool


def main():
    from random import randrange
    from time import sleep

    # Function to be executed in a thread
    def wait_delay(d):
        print("sleeping for (%d)sec" % d)
        sleep(d)

    # Generate random delays
    delays = [randrange(3, 7) for i in range(5)]

    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(5)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map(wait_delay, delays)
    pool.wait_completion()

if __name__ == "__main__":
    main()
