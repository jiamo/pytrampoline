class Tree:
    pass


class Null(Tree):
    def __init__(self):
        super().__init__()


class Leaf(Tree):
    __match_args__ = ("value",)

    def __init__(self, value):
        self.value = value
        super().__init__()


class Node(Tree):
    __match_args__ = ("left", "value", "right")

    def __init__(self, left: Tree, value, right: Tree):
        self.left = left
        self.right = right
        self.value = value
        super().__init__()


class Cont:
    pass


class Done(Cont):
    def __init__(self):
        super().__init__()


class Next(Cont):
    __match_args__ = ("value", "tree", "cont")

    def __init__(self, value, tree: Tree, cont: Cont):
        self.value = value
        self.tree = tree
        self.cont = cont
        super().__init__()


class Conc(Cont):
    __match_args__ = ("value1", "value2", "cont")

    def __init__(self, value1, value2, cont: Cont):
        self.value1 = value1
        self.value2 = value2
        self.cont = cont
        super().__init__()


def apply(cont: Cont, value):
    match cont, value:
        case Done(), value:
            return value
        case Next(value, rgt, c), ls:
            return show(rgt, Conc(ls, value, c))
        case Conc(ls, s, c), rs:
            return apply(c, ls + s + rs)


def show(t, k):
    match t:
        case Leaf(s):
            return apply(k, s)
        case Node(lft, s, rgt):
            return show(lft, Next(s, rgt, k))


if __name__ == "__main__":
    tree = Node(Node(Leaf("1 "), "2 ", Leaf("3 ")),
                "4 ",
                Leaf("5 "))
    print(show(tree, Done()))
