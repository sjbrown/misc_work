import sys
from grako.walkers import NodeWalker
from calc_parser import CalcParser
from calc_model import CalcModelBuilderSemantics


class CalcWalker(NodeWalker):
    def walk_object(self, node):
        return node

    def walk_Add(self, node):
        return self.walk(node.left) + self.walk(node.right)

    def walk_Subtract(self, node):
        return self.walk(node.left) - self.walk(node.right)

    def walk_Multiply(self, node):
        return self.walk(node.left) * self.walk(node.right)

    def walk_Divide(self, node):
        return self.walk(node.left) / self.walk(node.right)


def calc(text):
    parser = CalcParser(semantics=CalcModelBuilderSemantics())
    return parser.parse(text)


if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    model = calc(text)
    print(model)
    print(text.strip(), '=', CalcWalker().walk(model))
