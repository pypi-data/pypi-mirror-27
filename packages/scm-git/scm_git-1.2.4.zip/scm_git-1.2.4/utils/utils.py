import time
from pprint import pprint


def pretty_print(value, pretty):
    ''' For better print '''
    if value is None:
        return
    if pretty:
        pprint(value)
    else:
        print(value)


def timeit(func):
    ''' Display the time a function spend '''
    def timed(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()

        if kwargs.has_key('time'):
            print('[TimeIt] Run in {}s'.format(te - ts))
        return result
    return timed


def try_except(func):
    ''' Handling expceptions in a place'''
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except ValueError as ex:
            print(ex)
        except UnboundLocalError:
            pass
        else:
                if kwargs.has_key('pretty'):
                    pretty_print(res, kwargs['pretty'])
    return wrapper
