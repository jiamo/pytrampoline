

`trampoline.py`  inspired from  
https://github.com/tiancaiamao/shen-go/blob/master/cora/eval.go


the `trampoline2` in `trampoline_cache.py` come from
https://davywybiral.blogspot.com/2008/11/trampolining-for-recursion.html

`trampoline_mutual_recursion` come from  
https://github.com/0x65/trampoline


Example: 

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

TODO:  
1. make `trampoline.py` support cache like `trampoline_cache.py`
2. make `trampoline.py` support mutual recursion like `trampoline_mutual_recursion` 

