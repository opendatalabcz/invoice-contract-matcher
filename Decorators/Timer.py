from functools import wraps
from time import time

def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f'Finished in {round(te-ts,3)} sec')
        return result
    return wrap