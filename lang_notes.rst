==========
Annoyances
==========

In General
 * characters that mean 2+ things
  * They make grepping a real pain `grep &`
  * they make googling a real pain `google bash &`, `google bash $(`
  * =, ==
  * < less than, or start JSX Component?
  * /, //, /*
  * () for function definitions, function calls, and tuples and sub-expressions
  * . for attribute access and ... for JS "destructuring"
  * remembering if the language uses ! or not, && or and
  * different languages have different precedence rules, so I've always got to
    test / reference
 * Languages should make common-to-the-point-of-default effortless, and
   uncommon forced-explicit
 * Languages should benefit all programmer activities:
  * Writing code
  * Reading code
  * Debugging code:
   * Instrumenting
   * Reading stack traces
  * Documenting code with prose

Javascript
 * long lines
 * semicolons
 * curly braces
 * var
 * typing "console.log()" versus "print ..." is tiresome [1]
 * no negative array indexes
 * all the legacy stuff from being embedded in HTML
  * document and window as keywords
  * support for <!--, -->
 * You need to make an object foo = {} and then set a key with foo[k] = x
   if the key is stored inside a variable
 * Deep stacks are encouraged (anon function passing is easy, local variable
   creation is hard), so stacktraces are enormous
 * For the same reasons, there's fewer instrumentation points
 * Chained promises makes success/fail/catch cases difficult to see

Python
 * "def" should be "func"
 * Corallory to the one in Javascript, you have to put quotes around all
 your key names when you're making a struct-like dict
 * "is" and == is confusing. Novices often want to use "is" everywhere
 * instrumentation got harder in Python 3 with print()

Coffeescript
 * allowing no-paren functions causes ambiguity

==========
Ideas
==========

* [1] make log a keyword that exposes hooks
 * maybe paralleLOGram or math log ▱  ㏒ or "information" 🛈
 * Maybe reserve ㏒ to be a "rich instrumentation" keyword, not merely a
   synonym for "print:
  * '㏒ "some string", some_name' should act like "print"
  * but it should also be something you're able to put at the beginning of any
    line and it gives useful output when the line is run, maybe caching the
    evaluation of one level deep
  * '㏒ if a < 55:' should print "Line 63: if a < 55: | 44 < 55"
  * '㏒ foo = 88' should print "Line 64: foo = 88"
  * '㏒ foo = bar()' should print "Line 65: foo = bar() | 88"
* give most keywords a utf8 symbol
 * this might throw off alignment when we need fixed width - a test is needed
* grammatical INDENT, like python
* could be literal indent or symbols for "lambdas"
 * Candidate symbols:
  * ⇥ ⇤
  * ⦗ ⦘
  * ⭲ ⭰
  * various lambdas: 𝚲𝛌  𝛬𝜆  𝝠𝝺  𝞚𝞴 Λᴧ
* Other use of utf8:
 * null, None, ␀

----

Favour *early* understanding.  For instance, the decorator in Python could
have been implemented with an assignment after the function body, but you'd
have to read all the way to the end of the block to know it wasn't what it
seemed to be based on the reading of the first line.

So maybe a rule: readers should be able to understand the jist in the first
2 lines of 80 columns

----

Since it's hard to type utf8 chars, make & a reserved character and vim 
bindings to see when it's been typed and then auto-transform &> to ⇥, for
example

log: &L, null: &N, turtle parens: &(, &), integer literal type: &Z (ℤ)
string type: ✎ or ⅏ or ⁗ or ❠

autocmd FileType jspy :iabbrev <buffer> &Z ℤ
