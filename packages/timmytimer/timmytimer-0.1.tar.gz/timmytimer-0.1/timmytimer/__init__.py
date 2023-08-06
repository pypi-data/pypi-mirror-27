import time
import datetime as dt
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def timmy(function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = function(*args, **kwargs)
        t2 = time.time()

        log.debug('function:{0} args:{2} kwargs:{3} - time: {1}'.format(
                  function.__name__, t2 - t1, args, kwargs))
        return result
    return wrapper


def timmyprint(function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = function(*args, **kwargs)
        t2 = time.time()

        pre_string = '{} - {}'.format(dt.datetime.now().isoformat(), __name__)
        func_string = '{0}({1},{2})'.format(function.__name__, args, kwargs)
        time_string = 'time: {}'.format(t2 - t1)
        print(pre_string, ' - ', func_string, ' - ', time_string)
        return result
    return wrapper


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    @timmy
    def func(greeting, name='Henrik'):
        print('{} {}'.format(greeting, name))

    @timmyprint
    def funcprint(greeting, name='Henrik'):
        print('{} {}'.format(greeting, name))

    func('Hello', name='Gustav')
    funcprint('Hello', name='Ellinor')
