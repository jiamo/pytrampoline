from functools import partial, wraps, lru_cache
from .trampoline import trampoline
import traceback


@lru_cache
def fib(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


@trampoline
def fib_cps(n, k):
    if n == 0:
        return k(1)
    elif n == 1:
        return k(1)
    else:
        return fib_cps(n - 1, lambda v1: fib_cps(n - 2, lambda v2: k(v1 + v2)))

def fib_cps_wrapper(n):
    return fib_cps(n, lambda i:i)



@trampoline
def fib_tail(n, acc1=1, acc2=1):
    if n < 2:
        return acc1
    else:
        return fib_tail(n - 1, acc1 + acc2, acc1)



def fib_cps2(n, cont):
    if n < 2:
        return cont(1)
    else:
        return lambda: fib_cps2(
                         n - 1,
                         lambda value1:
                           lambda: fib_cps2(
                                     n - 2,
                                     lambda value2:
                                       lambda: cont(value1 + value2)))


def f(n):
    a, b = 1, 1
    for i in range(0, n):
        a, b = b, a + b
    return a

def trampoline2(f, *args):
    v = f(*args)
    while callable(v):
        v = v()
    return v




if __name__ == "__main__":
    print(fib(100))
    print(fib_tail(10000))
    print(trampoline2(fib_cps2, 25, lambda i:i))  # 25 was too slow
    print(fib_cps_wrapper(25))
