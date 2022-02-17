
# the answer from my question https://stackoverflow.com/questions/71037285/how-to-speed-up-the-trampolined-cps-version-fib-function-and-support-mutual-recu



from collections import namedtuple
import functools

TailRecArguments = namedtuple('TailRecArguments', ['wrapped_func', 'args', 'kwargs'])
def tail_recursive(f):
    f._first_call = True
    f._cache = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if f._first_call:
            f._new_args = args
            f._new_kwargs = kwargs
        
            try:
                f._first_call = False
                while True:
                    cache_key = functools._make_key(f._new_args, f._new_kwargs, False)
                    if cache_key in f._cache:
                        return f._cache[cache_key]

                    result = f(*f._new_args, **f._new_kwargs)

                    if not isinstance(result, TailRecArguments):
                        f._cache[cache_key] = result

                    if isinstance(result, TailRecArguments) and result.wrapped_func == f:
                        f._new_args = result.args
                        f._new_kwargs = result.kwargs
                    else:
                        break

                return result
            finally:
                f._first_call = True
        else:
            return TailRecArguments(f, args, kwargs)

    return wrapper




@tail_recursive
def even(n):
    """
    >>> import sys
    >>> sys.setrecursionlimit(30)
    >>> even(100)
    True
    >>> even(101)
    False
    """
    return True if n == 0 else odd(n - 1)

@tail_recursive
def odd(n):
    """
    >>> import sys
    >>> sys.setrecursionlimit(30)
    >>> odd(100)
    False
    >>> odd(101)
    True
    """
    return False if n == 0 else even(n - 1)

@tail_recursive
def fact(n, acc=1):
    """
    >>> import sys
    >>> sys.setrecursionlimit(30)
    >>> fact(30)
    265252859812191058636308480000000
    """
    return acc if n <= 1 else fact(n - 1, acc * n)

@tail_recursive
def fib(n, a = 0, b = 1):
    """
    >>> import sys
    >>> sys.setrecursionlimit(20)
    >>> fib(30)
    832040
    """
    return a if n == 0 else b if n == 1 else fib(n - 1, b, a + b)


@tail_recursive
def fib_cps(n, k):
    if n == 0:
        return k(1)
    elif n == 1:
        return k(1)
    else:
        return fib_cps(n - 1, lambda v1: fib_cps(n - 2, lambda v2: k(v1 + v2)))

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    print(fib_cps(20, lambda i:i))