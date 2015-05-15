from multiprocessing import Process, Queue
from functools import wraps


class TimeoutError(Exception):
    pass


class ProcessRunner(Process):

    def __init__(self, func, *args, **kwargs):
        self.queue = Queue(maxsize=1)
        run_args = (func, ) + args
        super(ProcessRunner, self).__init__(target=self.runner, args=run_args,
                                            kwargs=kwargs)

    def runner(self, func, *args, **kwargs):
        try:
            response = func(*args, **kwargs)
            self.queue.put((True, response))
        except Exception as e:
            self.queue.put((False, e))

    def response(self):
        return self.queue.get()


def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            process = ProcessRunner(func, *args, **kwargs)
            process.start()
            process.join(timeout=seconds)
            if process.is_alive():
                process.terminate()
                raise TimeoutError()
            success, response = process.response()
            if not success:
                process.terminate()
                raise response
            process.terminate()
            return response
        return wrapper
    return decorator
