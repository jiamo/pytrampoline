import functools
from dataclasses import dataclass
from typing import Optional, Any, Callable


START = 0
CONTINUE = 1
CONTINUE_END = 2
RETURN = 3


@dataclass
class CTX:
    kind: int
    result: Any    # TODO ......
    f: Callable
    args: Optional[list]
    kwargs: Optional[dict]


def trampoline(f):
    ctx = CTX(START, None, None, None, None)

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
            result = f(*args, **kwargs)
            if ctx.kind == CONTINUE_END:
                ctx.kind = RETURN
            else:
                ctx.kind = CONTINUE_END

        return result

    return decorator