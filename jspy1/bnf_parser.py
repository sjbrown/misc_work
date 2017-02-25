# pythonGrammarParser.py
#
# Copyright, 2006, by Paul McGuire
#

from pyparsing import *

grammar = '''

# Start symbols for the grammar:
#       single_input is a single interactive statement;
#       file_input is a module or sequence of commands read from an input file;

single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE
file_input: (NEWLINE | stmt)* ENDMARKER

decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE
decorators: decorator+

funcdef: 'def' NAME parameters ['->' test] ':' suite

parameters: '(' [typedargslist] ')'
typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [',' [
        '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
      | '**' tfpdef [',']]]
  | '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
  | '**' tfpdef [','])
tfpdef: NAME [':' test]
varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [',' [
        '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
      | '**' vfpdef [',']]]
  | '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
  | '**' vfpdef [',']
)
vfpdef: NAME

stmt: simple_stmt | compound_stmt
simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
small_stmt: (expr_stmt | del_stmt | flow_stmt |
             import_stmt | assert_stmt)
expr_stmt: testlist_star_expr (annassign | augassign (yield_expr|testlist) |
                     ('=' (yield_expr|testlist_star_expr))*)
annassign: ':' test ['=' test]
testlist_star_expr: (test|star_expr) (',' (test|star_expr))* [',']
augassign: ('+=' | '-=' | '*=' )

# For normal and annotated assignments, additional restrictions enforced by the interpreter
del_stmt: 'del' NAME

flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt

break_stmt: 'break'
continue_stmt: 'continue'
return_stmt: 'return' [testlist]
yield_stmt: yield_expr
raise_stmt: 'raise' [test ['from' test]]

import_stmt: import_name | import_from
import_name: 'import' dotted_as_names

# note below: the ('.' | '...') is necessary because '...' is tokenized as ELLIPSIS
import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
              'import' ('*' | '(' import_as_names ')' | import_as_names))
import_as_name: NAME ['as' NAME]
dotted_as_name: dotted_name ['as' NAME]
import_as_names: import_as_name (',' import_as_name)* [',']
dotted_as_names: dotted_as_name (',' dotted_as_name)*
dotted_name: NAME ('.' NAME)*

assert_stmt: 'assert' test [',' test]

compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt
async_stmt: ASYNC (funcdef | with_stmt | for_stmt)
if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]
while_stmt: 'while' test ':' suite ['else' ':' suite]
for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]
try_stmt: ('try' ':' suite
           ((except_clause ':' suite)+
            ['else' ':' suite]
            ['finally' ':' suite] |
           'finally' ':' suite))
with_stmt: 'with' with_item (',' with_item)*  ':' suite
with_item: test ['as' expr]
# NB compile.c makes sure that the default except clause is last
except_clause: 'except' [test ['as' NAME]]
suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT

test: or_test ['if' or_test 'else' test] | lambdef
test_nocond: or_test | lambdef_nocond
lambdef: 'lambda' [varargslist] ':' test
lambdef_nocond: 'lambda' [varargslist] ':' test_nocond
or_test: and_test ('or' and_test)*
and_test: not_test ('and' not_test)*
not_test: 'not' not_test | comparison
comparison: expr (comp_op expr)*
# <> isn't actually a valid comparison operator in Python. It's here for the
# sake of a __future__ import described in PEP 401 (which really works :-)
comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
star_expr: '*' expr
expr: xor_expr ('|' xor_expr)*
xor_expr: and_expr ('^' and_expr)*
and_expr: shift_expr ('&' shift_expr)*
shift_expr: arith_expr (('<<'|'>>') arith_expr)*
arith_expr: term (('+'|'-') term)*
term: factor (('*'|'@'|'/'|'%'|'//') factor)*
factor: ('+'|'-'|'~') factor | power
power: atom_expr ['**' factor]
atom_expr: [AWAIT] atom trailer*
atom: ('(' [yield_expr|testlist_comp] ')' |
       '[' [testlist_comp] ']' |
       '{' [dictorsetmaker] '}' |
       NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
testlist_comp: (test|star_expr) ( comp_for | (',' (test|star_expr))* [','] )
trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
subscriptlist: subscript (',' subscript)* [',']
subscript: test | [test] ':' [test] [sliceop]
sliceop: ':' [test]
exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
testlist: test (',' test)* [',']
dictorsetmaker: ( ((test ':' test | '**' expr)
                   (comp_for | (',' (test ':' test | '**' expr))* [','])) |
                  ((test | star_expr)
                   (comp_for | (',' (test | star_expr))* [','])) )

classdef: 'class' NAME ['(' [arglist] ')'] ':' suite

arglist: argument (',' argument)*  [',']

# The reason that keywords are test nodes instead of NAME is that using NAME
# results in an ambiguity. ast.c makes sure it's a NAME.
# "test '=' test" is really "keyword '=' test", but we have no such token.
# These need to be in a single rule to avoid grammar that is ambiguous
# to our LL(1) parser. Even though 'test' includes '*expr' in star_expr,
# we explicitly match '*' here, too, to give it proper precedence.
# Illegal combinations and orderings are blocked in ast.c:
# multiple (test comp_for) arguments are blocked; keyword unpackings
# that precede iterable unpackings are blocked; etc.
argument: ( test [comp_for] |
            test '=' test |
            '**' test |
            '*' test )

comp_iter: comp_for | comp_if
comp_for: [ASYNC] 'for' exprlist 'in' or_test [comp_iter]
comp_if: 'if' test_nocond [comp_iter]

# not used in grammar, but may appear in "node" passed from Parser to Compiler
encoding_decl: NAME

yield_expr: 'yield' [yield_arg]
yield_arg: 'from' test | testlist
'''

class SemanticGroup(object):
    def __init__(self,contents):
        self.contents = contents
        while self.contents[-1].__class__ == self.__class__:
            self.contents = self.contents[:-1] + self.contents[-1].contents
        
    def __str__(self):
        return "%s(%s)" % (self.label, 
                " ".join([isinstance(c,basestring) and c or str(c) for c in self.contents]) )
        
class OrList(SemanticGroup):
    label = "OR"
    pass
    
class AndList(SemanticGroup):
    label = "AND"
    pass

class OptionalGroup(SemanticGroup):
    label = "OPT"
    pass
    
class Atom(SemanticGroup):
    def __init__(self,contents):
        if len(contents) > 1:
            self.rep = contents[1]
        else:
            self.rep = ""
        if isinstance(contents,basestring):
            self.contents = contents
        else:
            self.contents = contents[0]
            
    def __str__(self):
        return "%s%s" % (self.rep, self.contents)
    
def makeGroupObject(cls):
    def groupAction(s,l,t):
        try:
            return cls(t[0].asList())
        except:
            return cls(t)
    return groupAction


# bnf punctuation
LPAREN = Suppress("(")
RPAREN = Suppress(")")
LBRACK = Suppress("[")
RBRACK = Suppress("]")
COLON  = Suppress(":")
ALT_OP = Suppress("|")

# bnf grammar
ident = Word(alphanums+"_")
bnfToken = Word(alphanums+"_") + ~FollowedBy(":")
repSymbol = oneOf("* +")
bnfExpr = Forward()
optionalTerm = Group(LBRACK + bnfExpr + RBRACK).setParseAction(makeGroupObject(OptionalGroup))
bnfTerm = ( (bnfToken | quotedString | optionalTerm | ( LPAREN + bnfExpr + RPAREN )) + Optional(repSymbol) ).setParseAction(makeGroupObject(Atom))
andList = Group(bnfTerm + OneOrMore(bnfTerm)).setParseAction(makeGroupObject(AndList))
bnfFactor = andList | bnfTerm
orList = Group( bnfFactor + OneOrMore( ALT_OP + bnfFactor ) ).setParseAction(makeGroupObject(OrList))
bnfExpr <<  ( orList | bnfFactor )
bnfLine = ident + COLON + bnfExpr

bnfComment = "#" + restOfLine

# build return tokens as a dictionary
bnf = Dict(OneOrMore(Group(bnfLine)))
bnf.ignore(bnfComment)

# bnf is defined, parse the grammar text
bnfDefs = bnf.parseString(grammar)

print bnfDefs
# correct answer is 78
expected = 78
assert len(bnfDefs) == expected, \
    "Error, found %d BNF defns, expected %d" % (len(bnfDefs), expected)

# list out defns in order they were parsed (to verify accuracy of parsing)
for k,v in bnfDefs:
    print k,"=",v
print

# list out parsed grammar defns (demonstrates dictionary access to parsed tokens)
for k in bnfDefs.keys():
    print k,"=",bnfDefs[k]
