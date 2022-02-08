
inspired from https://github.com/tiancaiamao/shen-go/blob/master/cora/eval.go

try:

```
python -m pytrampoline.cps
```

add an cps example


```
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



```

TODO: why this is so slow....