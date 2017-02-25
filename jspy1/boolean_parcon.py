#! /usr/bin/env python

from parcon import (
    Word,
    Literal,
    SignificantLiteral,
    Forward,
    Return,
    alpha_chars,
)

m_boolean = Literal("True")[lambda x: True] | Literal("False")[lambda x: False]

m_and = SignificantLiteral('and')(name='AND')
m_or = SignificantLiteral('or')(name='OR')

m_logical_operator = m_and | m_or

m_identifier = (Word(alpha_chars) - m_logical_operator)

m_expression = Forward()

m_subexpression = '(' + m_expression + ')'

m_term = m_boolean | m_identifier | m_subexpression

m_expression_tail= Forward()
m_infix_expression = m_term + m_expression_tail
m_expression_tail << (
    (m_logical_operator + m_expression + m_expression_tail)
    |
    (Return(None))
)

m_expression << (m_infix_expression | m_term)

def test(toker, tests):
    print '\n'

    l = [x.strip() for x in tests.split('\n') if x.strip() != '']
    for test in l:
        print test, ':',
        print toker.parse_string(test)

test(m_subexpression, '''
(True)
(foo)
''')
test(m_term, '''
True
foo
(True)
''')
test(m_infix_expression, '''
a and b
True and False
''')
test(m_expression, '''
True
( True )
True and False
a and b
True or (b)
a and (False)
foo
(foo)
(a or b) and (c or d)
''')
