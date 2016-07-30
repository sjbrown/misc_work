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
 * Per-variable scopes seem really dumb / special-casey.  Couldn't per-block
   scopes suffice (eg let/var in JS, global/nonlocal in Python)
   - research needed here

Javascript
 * long lines
 * semicolons
 * curly braces
 * requiring var - common should be default
 * var / let / global
 * typing "console.log();" versus "print ..." is tiresome [1]
 * no negative array indexes
 * all the legacy stuff from being embedded in HTML
  * document and window and location as keywords
  * support for <!--, -->
 * You need to make an object foo = {} and then set a key with foo[k] = x
   if the key is stored inside a variable
 * Deep stacks are encouraged (anon function passing is easy, local variable
   creation is hard), so stacktraces are enormous
 * For the same reasons, there's fewer instrumentation points
 * Chained promises makes success/fail/catch cases difficult to see
 * Anon functions are hard to mock & test

Python
 * "def" should be "func" or "function"
 * Corallory to the one in Javascript, you have to put quotes around all
 your key names when you're making a struct-like dict
 * "is" and == is confusing. Novices often want to use "is" everywhere
 * instrumentation got harder in Python 3 with print()
 * "self" or "cls" must be the first-by-order argument in a function signature

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
* No floats.  Math is rare in programming, and half the time people use
  floats, they actually want decimal.
 * Where to draw the line? strings, ints, lists, dicts, functions, classes?
* Annotations.  People seem to love them. (static typing) - maybe a way to
  make decorators more pretty.  Colon might be a good symbol here.
 * But colon is used by dicts {'a':33}.  Maybe "as".  See below.
 * Maybe ⊩ which is "forces" in Unicode
* When the language evolves, and you want to add a keyword, but everyone has
  already written code using that keyword - that sucks.  So maybe reserve @
  for interpretation/compilation affecting keywords.  This also makes
  @classmethod and @property look like Python

----

Annotate methods so that you don't have to type "self" or "cls" all the time.

But: this breaks static analysis!

    z = function(a, b=3, c="foo") \
        ⊩ @method
        self.baz = a + b
        self.zap = c + self.baz

    z = ⦗a ⊩ @int, b=3, c="foo"⦘ ⊩ (
        @classmethod,
        @returns_int,
        )
        cls.baz = a + b
        cls.zap = c + self.baz
        return cls.baz

----

Per-block scopes

    baz = []

    a = function(a, b=3) ⊩ @scope('inherit')
        baz.append(a + b) # baz comes from above scope

    b = function(a, b=3) ⊩ @scope('isolate')
        baz = [1, 2] # does not affect outer baz

    a(1) # baz is [4]

    b(1) # baz is still [4]

    c = function(a, b=3) ⊩ @scope_isolate
        baz.append(a + b) # Static analysis error - baz not defined

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

Should also reserve another character for users' auto-transforms. Maybe |

----

I do like Python's ability to do raw strings with r"/foo/\bar" for example.
Maybe simulate that with a special-case of one-argument functions that only
take strings and return strings and have no side-effects.

But maybe special cases aren't special enough to justify this.

----

Inline operators:
 * Enforce that whitespace must be around them
 * Precedence is just simple function precedence
  * Warn when there are two on the same line without parens making precedence
    safe
 * Classes implement their own __inline_+(self, other) methods, eg.
 * also, when encountering a = <SYMBOL> 3, search up scopes for
   a __inline_<SYMBOL> function (eg, like for raw strings in python a = r"\t")
   MAYBE.  could be complicated.

----

* z = 1
* z = "foo"
* z = tuple([3, foo"]) or (3, "foo") but parens collide semantically and tuples are rare
* z = list([3, foo"]) or z = [3, "foo"]
* z = dict(a=3, b="foo") or z = {"a":3, "b": "foo"}
 * It's annoying that dicts use colon, especially because I wanted to use colon for
   annotations, but it's too ingrained to break the pattern.
 * maybe annotations should just use "as".  It would collide with "with X as x", but it's
   compact and makes english-parsing sense.
* z = function(a, b=3, c="foo") ⇥ return c+a ⇤  or z = ⦗a, b=3, c="foo"⦘ ⇥ return c+a ⇤
 * is function special enough to get its own syntax?  Isn't it just a callable instance?
 * it is really common though.
* Z = class(inherit=A) ⇥ a = 1 ⇤  or ...? Z = ⟬inherit=A⟭ ⇥ a = 1 ⇤ 
* what about z = object(class=A) ? z = A()
* what about? z = ⦃⦄ # empty instance all it has is an id
 * but sometimes instances don't make sense without values

----

Args and kwargs

    z = foo(a, *args)

versus

    z = foo(a *args) # Actually does multiplication. Easy-to-make hard-to-spot error

So maybe instead of *, use ^.

    def foo(a, ^args, ^^kwargs):
        pass

    z = foo(a, ^args, ^^kwargs)

    z = foo(a ^ args) # Syntax error

