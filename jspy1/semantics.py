import sys
from attempt import Jspyr1Parser

class JSemantics(object):
    def number(self, ast):
        print 'number. ast is', ast
        return int(ast)

    def addition(self, ast):
        return ast.L + ast.R

    def subtraction(self, ast):
        return ast.L - ast.R

    def multiplication(self, ast):
        return ast.L * ast.R

    def division(self, ast):
        return ast.L / ast.R

def calc(text):
    parser = Jspyr1Parser(semantics=JSemantics())
    return parser.parse(text)

if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    result = calc(text)
    print text.strip()
    print result
