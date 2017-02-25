#! /usr/bin/env python
# encoding: utf-8

import string
import logging

from pyparsing import (
    alphas8bit,
)
from parcon import (
    Word as W,
    Literal,
    SignificantLiteral as K,
    Regex as R,
    Exact,
    OneOrMore,
    Optional,
    Forward,
    InfixExpr,
    ZeroOrMore,
    AnyChar,
    CharIn,
    Return,

    integer,
    digit_chars,
    alphanum_chars,
    alpha_chars,
)

keywords = '''\
False      class      finally               return
None       continue   for        lambda     try
True                  from                  while
and        del                   not        with
as         elif       if         or         yield
assert     else       import     pass
break      except     in         raise
'''

# These are Python keywords, so I want to make big bold warnings for them
reserved_words = '''\
def
global
elseif
is
nonlocal
'''


def test(toker_name, tests, fail_fast=True, debug=False):
    toker = globals()[toker_name]
    print '\n', toker_name, ':', getattr(toker, 'name', toker)

    if debug:
        toker.setDebug()
        #toker.setParseAction(debugParseAction)

    success_fail = [0,0]
    l = [x.strip() for x in tests.split('\n') if x.strip() != '']
    for test in l:
        print test, ':',
        try:
            print toker.parse_string(test)
            success_fail[0] += 1
        except Exception as e:
            if fail_fast:
                raise
            logging.exception(e)
            success_fail[1] += 1

m_2quote_string = ('"' + Exact(ZeroOrMore(AnyChar() - CharIn('"'))) +  '"')["".join]
test('m_2quote_string', r'''
"foo"
"foo bar baz"
''')
#"foo \" bar"

m_boolean = Literal("True")[lambda x: True] | Literal("False")[lambda x: False]
test('m_boolean', '''
True
False
''')

m_integer = integer(name='INT')[int]
m_string  = m_2quote_string(name='STR')
m_literal = m_boolean | m_integer | m_string

test('m_integer', '8')

m_and = K('and')(name='AND')
m_or = K('or')(name='OR')
m_not = K('not')(name='NOT')

test('m_and', 'and')
test('m_or', 'or')
test('m_not', 'not')

m_logical_operator = m_and | m_or

test('m_logical_operator', '''
and
or
''')

m_keywords = m_and | m_or | m_not

m_identifier = W(alphanum_chars + alphas8bit + '_' ,
                 init_chars = alpha_chars + alphas8bit + '_') - m_keywords

m_identifier = m_identifier(name='NAME')

test('m_identifier', '''
a
abc
_abc
abc1
''')



m_expression = Forward()
m_infix_operator = m_logical_operator(name='⧽X⧼')
m_prefix_operator = m_not
m_subexpression = '(' + m_expression + ')'

m_term = m_literal | (m_identifier) | (m_subexpression)

m_expression_tail= Forward()
m_infix_expression = m_term + m_expression_tail
m_expression_tail << (
    (m_infix_operator + m_expression + m_expression_tail)
    |
    (Return(None))
    )
"""
m_infix_expression = (
    | (m_term + m_infix_operator + m_expression)
    | (m_expression + m_infix_operator + m_term)
    )
    """

m_prefix_expression = (m_prefix_operator + m_term)

m_expression << (m_term | m_prefix_expression | m_infix_expression)
t = (m_term | m_infix_expression)
#m_expression << ( m_prefix_expression | m_infix_expression | m_term )(name="EXPR")

#m_expression.draw_productions_to_png({}, "syntax.png")

test('m_subexpression', '(9)')
test('m_prefix_expression', 'not False')
test('m_infix_expression', '''
0 and 1
888 and 1
a and b
True and False
''')
test('m_term', '''
888
"abc"
(9)
foo
''')
test('t', '''
9
"abc"
( 9 )
True and False
"a" and "b"
888 and 1
not False
a and b
a and (b)
foo
(foo)
a or b
_a or b0
(a or b) and (c or d)
''')


m_assignment = m_identifier + '=' + m_expression

test('m_assignment', '''
a = 9
b = "abc"
c = ( 9 )
d = ( False and 7) or 99
foo = _a or b0
''')
