import time


class Clock:

    def __init__(self, interval=10):
        self.interval = interval
        while interval > 0:
            print('.', end='')
            time.sleep(1)
            interval = interval - 1
        print('\n', end='')
