from .trampoline import trampoline


# mur

class Cont:
    pass


class Done(Cont):
    def __init__(self):
        super().__init__()


class Next(Cont):
    __match_args__ = ("value", "right", "cont")

    def __init__(self, value, right, cont: Cont):
        self.value = value
        self.right = right
        self.cont = cont
        super().__init__()


class Conc(Cont):
    __match_args__ = ("value1", "right", "cont")

    def __init__(self, value1, right, cont: Cont):
        self.value1 = value1
        self.right = right
        self.cont = cont
        super().__init__()


def apply(cont: Cont, value):
    match cont, value:
        case Done(), value:
            return value
        case Next(value, rgt, c), ls:
            return fib(rgt, Conc(ls, value, c))
        case Conc(ls, s, c), rs:
            return apply(c, ls + s + rs)


def fib(s, k):
    match s:
        case s if s < 2:
            return apply(k, 1)
        case s:
            left = s - 1
            right = s - 2
            v = 0
            return fib(left, Next(v, right, k))


if __name__ == "__main__":
    print(fib(25, Done()))
