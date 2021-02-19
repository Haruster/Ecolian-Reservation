import time


class UntilDoDecorator:
    def __init__(self, interval_time, err_msg: str):
        self.interval_time = interval_time
        self.err_msg = err_msg

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    r = func(*args, **kwargs)
                    break
                except Exception:
                    print(self.err_msg, time.ctime())
                    time.sleep(self.interval_time)
            return r
        return wrapper

