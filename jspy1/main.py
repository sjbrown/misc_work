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

@traceParseAction
def debugParseAction(toks):
    pass


def test(toker_name, tests, fail_fast=True, debug=False):
    toker = globals()[toker_name]
    print '\n', toker_name, ':', toker

    if debug:
        toker.setParseAction(debugParseAction)
    success_fail = [0,0]
    l = [x.strip() for x in tests.split('\n') if x.strip() != '']
    for test in l:
        print test, ':',
        try:
            print toker.parseString(test)
            success_fail[0] += 1
        except Exception as e:
            logging.exception(e)
            success_fail[1] += 1
        if fail_fast and success_fail[1] != 0:
            return

m_integer = W(nums)
m_string  = quotedString
m_literal = m_integer ^ m_string

m_and = K('and')
m_or = K('or')

test('m_and', 'and')
test('m_or', 'or')


m_logical_operator = m_and ^ m_or

test('m_logical_operator', '''
and
or
''')


m_identifier = W(initChars = alphas + alphas8bit + '_',
                 bodyChars = alphas + alphas8bit + '_' + nums)

test('m_identifier', '''
a
abc
abc xxx
''')


m_infix_operator = m_logical_operator
m_prefix_operator = K('not')

m_expression = Forward()
#m_subexpression = nestedExpr(content=m_expression)
m_subexpression = nestedExpr()

m_evaluant = m_literal ^ m_identifier ^ m_subexpression
test('m_evaluant', '''
9
"abc"
(9)
''')

#m_infix_expression = m_expression + m_infix_operator + m_expression
m_infix_expression = m_evaluant + m_infix_operator + m_expression ^\
                     m_expression + m_infix_operator + m_evaluant ^\
                     m_evaluant + m_infix_operator + m_evaluant

m_prefix_expression = m_prefix_operator + m_expression

m_expression = m_evaluant ^ m_prefix_expression ^ m_infix_expression

test('m_expression', '''
9
"abc"
( 9 )
foo
(foo)
a and b
a or b
_a or b0
''')


m_assignment = m_identifier + '=' + m_expression

print m_assignment.parseString('ccc = _a or b0')

test('m_assignment', '''
a = 9
b = "abc"
c = ( 9 )
d = ( False and 7) or 99
foo = _a or b0
''')
