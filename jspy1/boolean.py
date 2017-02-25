#! /usr/bin/env python
# encoding: utf-8

import string
import logging

from pyparsing import (
    Word as W,
    Keyword as K,
    Regex as R,
    QuotedString,
    Empty,
    OneOrMore,
    Group,
    Optional,
    White,
    Forward,
    StringEnd,

    nums,
    alphanums,
    alphas,
    alphas8bit,
    commaSeparatedList,
    pythonStyleComment,
    quotedString,
    nestedExpr,

    traceParseAction,
)

def test(toker_name, tests, fail_fast=True, debug=False):
    toker = globals()[toker_name]
    print '\n', toker_name, ':', toker

    if debug:
        toker.setDebug()

    l = [x.strip() for x in tests.split('\n') if x.strip() != '']
    for test in l:
        print test, ':',
        try:
            print toker.parseString(test)
        except Exception as e:
            if fail_fast:
                raise
            logging.exception(e)

m_true = K('True')
m_false = K('False')
m_literal = m_true ^ m_false

test('m_literal', '''
True
False
''')

m_identifier = W(initChars = alphas + alphas8bit + '_',
                 bodyChars = alphas + alphas8bit + '_' + nums)

m_identifier.setName('NAME')

test('m_identifier', '''
a
abc
_abc
abc1
''')


m_and = K('and')
m_and.setName('AND')
m_or = K('or')
m_or.setName('OR')
m_not = K('not')
m_not.setName('NOT')

test('m_and', 'and')
test('m_or', 'or')

m_logical_operator = m_and ^ m_or

test('m_logical_operator', '''
and
or
''')


m_expression = Forward()
m_expression.setName('EXPR')
m_infix_operator = m_logical_operator
m_prefix_operator = m_not
m_subexpression = nestedExpr(content=m_expression)

m_term = m_literal ^ m_identifier ^ m_subexpression

m_infix_expression = (
    (m_term + m_infix_operator + m_expression)
    #^
    #(m_expression + m_infix_operator + m_term)
    ^
    (m_term + m_infix_operator + m_term)
)

m_prefix_expression = m_prefix_operator + m_expression

m_expression << (m_term ^ m_prefix_expression ^ m_infix_expression) + StringEnd()

test('m_subexpression', '(True)')
test('m_term', '''
True
abc
(True)
(abc)
''')

test('m_expression', '''
True
not False
( False )
foo
(foo)
a and b
a or b
True or True
False and False
True and (a and b)
(a or b) and False
(a or b) and (c or d)
''')


m_assignment = m_identifier + '=' + m_expression

test('m_assignment', '''
a = False
b = True
c = ( False )
d = ( False and True ) or True
foo = _a or b0
''')
