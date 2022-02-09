# trampoline2
# https://davywybiral.blogspot.com/2008/11/trampolining-for-recursion.html

# trampoline1
# https://jupyter.brynmawr.edu/services/public/dblank/CS245%20Programming%20Languages/2014-Fall/Notes/Review,%20Continuations%20and%20CPS.ipynb
# but it is same like trampoline.py . it is slow
from types import FunctionType
from functools import lru_cache


class Call:
    def __init__(self, fn, *args, **kwargs):
        self.call = lambda: fn(*args, **kwargs)


def trampoline2(obj):
    while isinstance(obj, Call):
        obj = obj.call()
    return obj


def kmemoized2(func):
    cache = {}

    def decorator(k, *args):

        if args in cache:
            # print(args)  the args was just number
            return Call(k, cache[args])

        def with_value(value):
            cache[args] = value
            return Call(k, value)

        return Call(func, with_value, *args)

    return decorator


@kmemoized2
def fibonacci2(k, n):
    if n < 2:
        return Call(k, 1)

    def with_a(a):
        def with_b(b):
            return Call(k, a + b)

        return Call(fibonacci2, with_b, n - 1)

    return Call(fibonacci2, with_a, n - 2)


all_result = []
cache_set = set()


# @lru_cache
def apply(k, *args):
    # how to debug: we need add lru cache
    # key = encode(*args)
    # print(k, args)
    result = k(*args)
    # result_key = encode(*result)
    # cache_set.add((key, result_key))
    # all_result.append((key, result_key))
    return result


def encode(*args):
    keys = []
    for i in args:
        if isinstance(i, FunctionType):
            keys.append(str(id(i)))
        else:
            keys.append(str(i))
    return "_".join(keys)


def trampoline1(result):

    while isinstance(result, list):
        if result[0] == "apply-cont":
            result = result[1](result[2])
        elif result[0] == "goto":
            result = apply(result[1], *result[2:])
    return result


# It is import to cache this
# @lru_cache
def fib_cps1(n, k):
    if n == 0:
        return ["apply-cont", k, 1]
    elif n == 1:
        return ["apply-cont", k, 1]
    else:
        return ["goto", fib_cps1, n - 1,
                lambda v1: ["goto", fib_cps1, n - 2,
                            lambda v2: ["apply-cont", k, v1 + v2]]]


if __name__ == "__main__":
    print(trampoline2(fibonacci2(lambda x: x, 40)))
    print("-----------")
    print(trampoline1(fib_cps1(40, lambda i: i)))  # fib_cps1(40, lambda i: i)
    print("-----------")
    print("unique ", len(cache_set), "all ", len(all_result))

    # print(fibonacci(lambda x: x, 5))
    # print(fib_cps(lambda x: x, 5))
