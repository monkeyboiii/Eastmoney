import time


def timestamp(func):
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        print('Initiated at {},'
              ' you start checking'.format(
            time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime())))
        stop = time.time_ns()
        print('We wasted {} nanoseconds for you'.format(stop - start))
        return func(*args, **kwargs)


    return wrapper


class Stock:
    # Constructor
    def __init__(self, stockCode, stockName):
        self.stockCode = stockCode
        self.stockName = stockName


    @timestamp
    def check(self):
        print('Waiting', end='')
        for i in range(1, 5):
            print('.', end='')
            time.sleep(0.3)
        print('\n Your stock code = {}'.format(str(self.stockCode)))
        if input('Shall we continue?') == 'Y' or 'y':
            self.check()
        else:
            return


if __name__ == '__main__':
    myStock = Stock(21432, 'WeChat')
    myStock.check()
