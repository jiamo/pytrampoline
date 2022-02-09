import functools
from dataclasses import dataclass
from typing import Optional, Any


START = 0
CONTINUE = 1
CONTINUE_END = 2
RETURN = 3


@dataclass
class CTX:
    kind: int
    result: Any
    args: Optional[list]
    kwargs: Optional[dict]


def trampoline(f):
    ctx = CTX(START, None, None, None)

    @functools.wraps(f)
    def decorator(*args, **kwargs):
        nonlocal ctx
        if ctx.kind in (CONTINUE, CONTINUE_END):
            ctx.args = args
            ctx.kwargs = kwargs
            ctx.kind = CONTINUE
            return
        elif ctx.kind == START:
            ctx.args = args
            ctx.kwargs = kwargs
            ctx.kind = CONTINUE

        result = None
        while ctx.kind != RETURN:

            args = ctx.args
            kwargs = ctx.kwargs
            # key = tuple(args) + tuple(kwargs)
            result = f(*args, **kwargs)
            # the result continue is call f again?
            if ctx.kind == CONTINUE_END:
                ctx.kind = RETURN
            else:
                ctx.kind = CONTINUE_END

        return result

    return decorator


def fib2(n):
    @trampoline     # it is too slow
    def fib_helper(n, a, b): # there is too acc
        if n == 1:
            return a
        return fib_helper(n-1, b, a+b)

    return fib_helper(n, 1, 1)


if __name__ == "__main__":
    print(fib2(1000))
