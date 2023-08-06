from multiprocessing import Pool


class EzPool:

    def __init__(self, threads=4):
        self.threads = threads
        self.pool = Pool(processes=threads)

    def submit(self, func, *args):
        """
        Submit a new task to the pool

        :param func: The function to run
        :param args: Its arguments

        :return: EzFuture
        """
        future = EzFuture()
        future.start(self.pool.apply_async(func, args, callback=future))
        return future

    def await(self):
        """
        Close the pool and wait until all tasks complete
        """
        self.pool.close()
        self.pool.join()

    def kill(self):
        """
        Kill the pool and ignore task states
        """
        self.pool.terminate()
        self.pool.join()


class EzFuture:

    def __init__(self):
        self.result = None
        self.callbacks = []

    def start(self, result):
        self.result = result

    def callback(self, func, *args):
        """
        Register a new callback

        :param func: The function to call
        :param args: Additional arguments
        """
        self.callbacks.append((func, args))

    def __call__(self, *args, **kwargs):
        for callback in self.callbacks:
            func, a = callback
            func(*a, *args)


def pool():
    """
    Create a new thread pool

    :return: EzPool
    """
    return EzPool()
