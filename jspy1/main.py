#! /usr/bin/env python
# encoding: utf-8

import string

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

    nums,
    alphanums,
    alphas,
    alphas8bit,
    commaSeparatedList,
    pythonStyleComment,
    quotedString,

    traceParseAction,
)

@traceParseAction
def debugParseAction(toks):
    pass

def debug(toker):
    toker.setParseAction(debugParseAction)

m_integer = W(nums)
m_string  = quotedString
m_literal = m_integer ^ m_string

m_and = White() + K('and') + White()
m_and = K('and')
m_or = White() + K('or') + White()
m_or = K('or')

print m_and.parseString('and')
print m_or.parseString('or')
print m_and.parseString(' and ')
print m_or.parseString(' or ')


m_logical_operator = m_and ^ m_or

print m_logical_operator.parseString('and')
print m_logical_operator.parseString('or')


m_identifier = W(initChars = alphas + alphas8bit + '_',
                 bodyChars = alphas + alphas8bit + '_' + nums)

print m_identifier.parseString('a')
print m_identifier.parseString('abc')
print m_identifier.parseString('abc xxx')

m_infix_operator = m_logical_operator

m_infix_expression = m_identifier + m_infix_operator + m_identifier
m_prefix_expression = ('@PY' + m_identifier) ^ ('@PY' + m_literal)

m_expression = m_infix_expression ^ m_prefix_expression
debug(m_expression)

m_assignment = m_identifier + '=' + m_expression
debug(m_expression)


print m_expression.parseString('a and b')
print m_expression.parseString('a or b')
print m_expression.parseString(' a or b')
print m_expression.parseString('a or b ')
print m_expression.parseString('_a or b0')


print m_assignment.parseString('ccc = _a or b0')
