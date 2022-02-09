
# example
# https://matthewkrump.com/2017-05-25-trampoline/
# https://davywybiral.blogspot.com/2008/11/trampolining-for-recursion.html
# need curse
# @trampoline


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


def kmemoized(func):
    cache = {}

    def inner(k, args):
        if args in cache:
            return Call(k, cache[args])

        def with_value(value):
            cache[args] = value
            return Call(k, value)

        return Call(func, with_value, *args)

    def decorator(k, *args):
        # print(k)
        def with_value(value):
            cache[args] = value
            return Call(k, value)

        if args in cache:
            obj = Call(k, cache[args])
        else:
            obj = Call(func, with_value, *args)

        while isinstance(obj, Call):
            obj = obj.call()

        return obj

    return decorator


@kmemoized
def fibonacci(k, n):
    if n < 2:
        return Call(k, 1)

    def with_a(a):
        def with_b(b):
            return Call(k, a + b)

        return Call(fibonacci, with_b, n - 1)

    return Call(fibonacci, with_a, n - 2)



def fib(k, n):
    if n < 2:
        return Call(k, 1)

    def with_a(a):
        def with_b(b):
            return Call(k, a + b)

        return Call(fib, with_b, n - 1)

    return Call(fib, with_a, n - 2)




@kmemoized
def fib_cps(k, n):
    if n == 0:
        return k(1)
    elif n == 1:
        return k(1)
    else:
        return fib_cps(lambda v1: fib_cps(lambda v2: k(v1 + v2), n - 2), n - 1)


def even(n):
    if n == 0:
        return True
    else:
        return odd(n - 1)


# @trampoline
def odd(n):
    if n == 0:
        return False
    else:
        return even(n - 1)

def fib2(n):
    @kmemoized     # it is too slow
    def fib_helper(n, a, b): # there is too acc
        if n == 1:
            return a
        return fib_helper(n-1, b, a+b)

    return fib_helper(n, 1, 1)


if __name__ == "__main__":

    print(trampoline2(fibonacci2(lambda x: x, 1000)))
    print(fibonacci(lambda x: x, 1000))
    # print(fib_cps(lambda x: x, 5))
