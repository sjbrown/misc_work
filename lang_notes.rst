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
  * Talking about code
   * eg, being able to say "foo calls bar" rather than
     "the third anon fn calls bar"
  * Documenting code with prose
 * Per-variable scopes seem really dumb / special-casey.  Couldn't per-block
   scopes suffice (eg let/var in JS, global/nonlocal in Python)
   - research needed here
   - can I find an example where it's necessary or looks better?
 * Dealing with secrets (passwords, keys, etc)
 * Enumerated types or "strings", which usually just boil down to
  - This is a string that I don't want to typo
  - Maybe use one of these?  № ™ ℵ ⅇ ♯

Javascript
 * long lines
 * semicolons
 * curly braces
 * requiring var - common should be default
 * var / let / global
 * ['a'] === ['a'] is false
 * Boolean({}) is true, Boolean([]) is true, Boolean('') is false
 * {}.length is undefined
 * [1,2] + [3,4] is a string, "1,23,4"
 * strict mode is very different than non-strict mode
 * typing "console.log();" versus "print ..." is tiresome [1]
 * no negative array indexes
 * slicing in general is annoying compared to Python
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
 * Arrow functions! "this" is set to the this value of the enclosing
   execution context.  Just by the 2 characters ->.  Really fails the
   explicit-versus-implicit zen.
 * Creating a new Error class is a minefield: https://stackoverflow.com/questions/783818/how-do-i-create-a-custom-error-in-javascript
 * It's easy (easy => encouraged) can be written s.t. optional args can go
   *first* in the arg list.

Python
 * https://attrs.readthedocs.io/en/stable/examples.html attrs helps
 * "def" should be "func" or "function"
 * colons are: function signature enders, for/while loop enders,
   slice mini-lang delimiters, dict-constructing mini-lang delimiters
  * for slicing into an array: myarray⟦:-2:4⟧, myarray⟦:⟧ (or also myarray⟦⟧)
   * how does this work for assignment? myarray[3] = 33
   * maybe use the @ for that instead:
    * myarray@3 = 33
    * myarray@i+1 = 33  # ambiguous!!
    * mydict@'some key' = 33
    * mydict@('key a', 'key b') = 33, 88
   * best alternative may be different behaviour depending on which side of
     the equals sign the symbol is on.  But that seems not great.
  * dict-constructing mini-lang can still work d = {'a': 3}
  * maybe reserve colons for encloser mini-langs?
  * it's just really, really different, though.
  * different symbols: myarray⟦2~9⟧, myarray⟦~-2|4⟧, myarray⟦⟧, myarray⟦|4⟧
 * Corallory to the one in Javascript, you have to put quotes around all
 your key names when you're making a struct-like dict
 * single-item tuple: (1,) because (1) is algebra
 * "is" and == is confusing. Novices often want to use "is" everywhere
 * implicitly returning None can get you into trouble
  * Maybe when generating Python code, return an object whose magic methods
    ALL raise errors, and each one has a unique id (to foil "is" comparisons)
   * If the errors could lead back to the line of code where the guilty
     function returned, that'd be awesome
 * Do we want a symbol for return?
    z = ⦗a ⊧ "foo"⦘
      ⏎ a + "bar"
    z = ⦗a ⊧ "foo"⦘
      ⮐ ⭩ ⇦  ⇚  ⇐  ↵  ↶  a + "bar"
    z = ⦗a ⊧ "foo"⦘
      ⮐ a + "bar"
    z = ⦗a ⊧ "foo"⦘
      ↶ a + "bar"
 * instrumentation got harder in Python 3 with print()
 * "self" or "cls" must be the first-by-order argument in a function signature
 * "elif" is silly.  but "else if" would be two tokens - confusing to novice,
   so "elseif" is probably best.
 * None, True, and False are *values* distinguished from identifiers based
   solely on their first capitalized character
   * User must memorize these 3 exceptions
   * They look like Classes but behave nothing like them
   * Maybe @None, @null, @undefined, @True, @False would be better
 * Immutable objects:
  * strings have methods that look like they should mutate the string:
   - capitalize center encode expandtabs format ljust lower lstrip partition
   - replace rjust rpartition rstrip strip swapcase title translate upper zfill


Coffeescript / ES6
 * allowing no-paren functions causes ambiguity / precedence hell
  * foo a, bar c, d
  * foo (a,b) (c,d)

==========
Ideas
==========

* Motivation: I want to use Flask / Django to develop the backend API stuff
  because of lots of library support.  I want to use React / Redux to
  develop the frontend stuff because of library support & it HAS to be
  Javascript.  But validation code is going to look almost IDENTICAL.
  Wouldn't it be nice to just write the validation code once?

* [1] make log a keyword that exposes hooks
 * maybe paralleLOGram or math log ▱  ㏒ or "information" 🛈
  * I like 🛈 because it looks like a debugger symbol.  It's hella wide in
    this font though.
 * Maybe reserve 🛈  to be a "rich instrumentation" keyword, not merely a
   synonym for "print:
  * '🛈  "some string", some_name' should act like "print"
  * but it should also be something you're able to put at the beginning of any
    line and it gives useful output when the line is run, maybe caching the
    evaluation of one level deep
  * '🛈  if a < 55:' should print "Line 63: if a < 55: | 44 < 55"
  * '🛈  foo = 88' should print "Line 64: foo = 88"
  * '🛈  foo = bar()' should print "Line 65: foo = bar() | 88"
  * should '🛈  some_generator_fn()' print "<generator at 0x3poin>" or turn it into a list?
  * should '🛈  some_generator_fn()' print "<generator at 0x3poin 2, 4, 6, ...>"?
* give most keywords a utf8 symbol
 * this might throw off alignment when we need fixed width - a test is needed
* grammatical INDENT, like python
* could be literal indent or symbols for "lambdas"
 * Candidate symbols:
  * ⇥ ⇤
   * I like this one.
  * ⦗ ⦘
  * ⭲ ⭰
  * various lambdas: 𝚲𝛌  𝛬𝜆  𝝠𝝺  𝞚𝞴 Λᴧ
* Other use of utf8:
 * null, None, ␀
 * ⸨⸩〖〗【】⸦⸧  ⫍⫎⦅⦆⦇⦈⦋⦌⟪⟫❨❩◜◝◟◞⎿⏌⎡⎤⌁⌁⊏⊐⁅⁆
* No formatting mini-languages.  Python has too many:
 * "%s" % foo, "{}".format(foo), b"%x" % val
 * use the infix operator: "{} {}" ⧽fmt⧼ (a,b)
 * use the infix operator: "%s %2s" ⧽%⧼ (a,b)
  * kinda looks like a butterfly ("from butterflies import %")
  * hard to google for the definition
 * use the infix operator: "$foo $bar" ⧽$⧼ locals()
 * crazy idea:  "$foo $bar" ⧽⧽$ # implies arg2 is locals()
  * it's not very explicit, though. and I can't see other good uses
  * hard to google for the definition
* No floats.  Math is rare in programming, and half the time people use
  floats, they actually want decimal.
 * Also, bitwise operations are SUPER-rare, why do we have all these symbols
   reserved for that hairy stuff?
 * Where to draw the "it's too rare" line?
  * I think: strings, ints, lists, dicts, functions, classes?
   * Can these be interesting? expressions, operators, modules, ...
* If no floats, then what?
  * Decimal(0,40): can get cumbersome to type
  * Special decimal-creating operator: 0⋄51 (Python "decimal")
  * Special float-creating operator: 0⋆51
  * Default behaviour that creates a Decimal and spits out a warning: 0.51
    * But this reads as "take 0, apply the 51 query" - expensive at runtime
  * What about Rational numbers? 2ℚ3 2⟌3  52⅟33  5÷3  2÷3
  * Python ("fraction")
* Annotations.  People seem to love them. (static typing) - maybe a way to
  make decorators more pretty.  Colon might be a good symbol here.
 * But colon is used by dicts {'a':33}.  Maybe "as".  See below.
 * Maybe ⊩ which is "forces" in Unicode
* When the language evolves, and you want to add a keyword, but everyone has
  already written code using that keyword - that sucks.  So maybe reserve @
  for interpretation/compilation affecting keywords.  This also makes
  @classmethod and @property look like Python
* Get rid of `is` and check identity with some infix operator
 * ≡ seems perfect.

----

Dynamic infix operators, maybe one of these pairs:
 * ⨴mod⨵ ⸡mod⸠ ⭪mod⭬  ⧼mod⧽ ⥆mod⥅ ⟞mod⟝ ⚞mod⚟  ╡mod╞  ⍇mod⍈
 * ⍅mod⍆ ⊣mod⊢  ⇐mod⇒  ↫mod↬  ↤mod↦  ↲mod↳
 * this one is a bit confusing with "forces": ╡mod╞
 * looks best:    asd ⧼mod⧽ fub    asd ╡mod╞ fub
 * I like ⥆mod⥅ semantically, but the font doesn't look great
 * improve with parens or spaces?  asd ⥆(mod)⥅ fub    asd ⥆ mod ⥅ fub
 * reverse direction?  asd ⥅(mod)⥆ fub    asd ⥅ mod⥆ fub
 * asd ⧽mod⧼ fub -- I like this better.  parens open to arguments.

 * multi-arg? (asd, foo)⧽zip⧼(baz, fub)
 * multi-arg? ⧼asd, foo⧽zip⧼baz, fub⧽  # I don't really like that

 * I think the language should enforce a no-spaces policy on the
   infix enclosure, otherwise it could cause bugs from being less
   obviously infix.

But: a + b invokes a.__radd__(b), should a ⧽zip⧼ b
 * invoke a.__rzip(b)
 * find a local name called zip and apply zip(a, b)
 * ?

Maybe in order it looks for the local name, then falls back to a.__magic?
But then we can create ambiguous code.

Maybe we have one encloser style for each behaviour?  Seems inelegant.
 * foo ⧽zip⧼ baz executes zip(foo, baz)
 * foo ⧼zip⧽ baz executes foo.__rzip(baz)

 * foo ⧽zip⧽ baz executes foo.__rzip(baz)
 * foo ⧼zip⧼ baz executes baz.__lzip(foo)

 * Inelegant, and no predicted use.

If I'm gonna do infix, what about going down this rabbit hole:

    x += 5
    x ⧼mod⧽= 5
    x ⧽mod⧼= 5

    # d = {k:v*10 for (k,v) in d}
    d ⧼valmult⧽= 10  # what's the point though?

"Apply infix function, then attach the old name to the new value"

How will this deal with the infix function having side-effects?  Especially
if it invokes a.__rmod(5)

```
for x in 1 ⧽through⧼ 12
    console.info(x)
```

Use american shorthand:

```
for x in 1 ⧽thru⧼ 12
    console.info(x)
```

This could also be used to disambiguate between the two uses of "in":
`for member in collection` versus `if value in collection`

```

for x in my_list
    console.info(x)

if x ⧽in⧼ some_list
    console.info(x)

if [1,3,5] ⧽contains⧼ x
    console.info(x)

if x ⧽inside⧼ [1,2,3,6]
    console.info(x)

# Of course if shorthand is really desired there's a natural mathematical
# symbol to express this, but it might be too esoteric for a general audience

if x ϵ [1,2,3,6]
    console.info(x)

```



----

"Enclosers".  There is a module-level attribute, "enclosers" that let special
brackets represent function / class calls.

__module__.enclosers = {
    ⦃⦄ : numpy.array,
}

----

What if you interpret __call__ as "the most common thing done with this object"?

 * functions - execute code block with arguments
 * classes - return a new instance with arguments
 * lists - slice (args are indexes)
 * dicts - return value at key (args are keys)

----

Annotate methods so that you don't have to type "self" or "cls" all the time.

But: this breaks static analysis! (Maybe?  If the rule was that @blah names
affect compilation, then we might still be able to do it in limited cases)

```
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

    result = z(1)
```

----

Classes?

```
    Z = class(inherit=A)
        a = 1

    Z = ⟬inherit=A⟭ ⇥ a = 1 ⇤ 

    z = Z()
```

----

Instances?

```
    z = A()
    z = object(class=A)  # I don't like this.  It doesn't match with Python
    z = instance(A)
    z = instance(A, B)   # This might be really confusing
    z = ⦃A⦄
    z = ⦃⦄  # empty instance all it has is an id
            # I don't like that.
            # I think ⦃⦄  should *require* an argument
    z = ⦃object⦄  # empty instance all it has is an id
```

The argument inside ⦃...⦄ should be mandatory.

But *everything* is an instance so this seems a little weird.

----

Modules?

* Mostly, they should just be implied from files / file structure, but
  interesting mocking could be done if you made them available for manipulation
* How are modules different?  Isolated scope.  More stuff?
* How does writing a module in a scope and then doing `import module_name` get
  understood? Is it understood statically or dynamically?

    M = module(__name__="__main__")
        main = function()
            pass
        if __name__ == "__main__":
            main()

    M.__load__()
    assertCalled(M.__namespace__.main)

    M = ⎰ __name__ = "__main__"⎱  # looks too much like an L, I think
        pass # namespace goes here

    M = ⎴ __name__ = "__main__" ⎵
        pass # namespace goes here

    M = ⏞ __name__ = "__main__" ⏟ # feels like a pretty good semantic map
        pass # namespace goes here

Packages?

I feel I'm too far into the woods now.

----

Per-block scopes

    baz = []

    a = function(a, b=3) ⊩ @scope('inherit')
        baz.append(a + b) # baz comes from above scope ("lexical" / "static")

    b = function(a, b=3) ⊩ @scope('isolate')
        baz = [1, 2] # does not affect outer baz (like "let" in JS)

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

This would also allow mixing in code from other languages if the goal was
to actually intersperse and call foreign functions:

    b = "asdf"
    @JS"""
    var c = b.substr(1);
    """
    # Ideally now c is in the local namespace
    🛈  c  #Prints "sdf"

Doesn't seem so hard if we make some assumptions - like it's going to be
compiled to Javascript anyway.  This would be completely broken for compiling
to Python

Breaks our ability to statically analyze for bugs, but it's fine to give that
power to users who know what they're doing

Much like Python raw strings, it gives us a sane point to answer:
What will be the result of the following?

    @PY"""
       a = 'Foo\n'
    """

Does this generate the python code

    a = 'Foo
    '

Or the code

    a = 'Foo\n'

(It should be the latter)

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

    z = foo(a *args) # Actually does multiplication.
    # Easy-to-make hard-to-spot* error

So maybe instead of * , use ^.

    foo = function(a, ^args, ^^kwargs)
        pass

    z = foo(a, ^args, ^^kwargs)

    z = foo(a ^ args) # Syntax error

----

"Forces"

Use forces on dicts to make them attr-dicts:

    d = dict(a=3, b=4) ⊩ @dictattrs
    assert d.a == d.{'a'}

Since forces can change compilation, we can make this convenient:

    d = dict() ⊩ @dictnamespace
        a = 3
        b = 4
    assert d.{'a'} == 3
    assert d.b == 4

Maybe "forces" can be narrowed to be interpreted as "changing
the behaviour of '=' (assignment) such that the value on the
left-hand-sign goes through the Forces Function any time assignment
happens for that name.

----

Promises to async / await

Example JS Code:

```
    api.post('customers', validation.acceptableFields)
    .then(function(response) {
      return exports.serverResponseToValidation(response, 201);
    })
    .then(function(validation) {

      if (!exports.isValid(validation)) {
        dispatch({ type: exports.NEW_SAVE_ERROR, validation: validation });
        return;
      }

      var id = api.getIdFromHeader(response);
      customer['id'] = id;

      dispatch({ type: exports.NEW_SAVE_SUCCESS, validation: validation });
      var destinationUrl = window.config.dashboardRoot + '/customers/' + id;
      browserHistory.push(destinationUrl);

    })
    .catch(function(err) {
      console.error(err); // eslint-disable-line no-console
      dispatch({ type: exports.NEW_SAVE_ERROR, customer: customer });
    });
```

Replace that with:

```
    try:
      response = await api.post('customers', validation.acceptableFields)
      validation = await serverResponseToValidation(response, 201)

      if not validation.isValid
          dispatch(type=NEW_SAVE_ERROR, validation=validation)
          return

      id = api.getIdFromHeader(response)
      customer['id'] = id

      dispatch(type=NEW_SAVE_SUCCESS, validation=validation)
      destinationUrl = window.config.dashboardRoot + '/customers/' + id
      browserHistory.push(destinationUrl)

    catch Exception as err: 🛈
      log(err)
      dispatch(type=NEW_SAVE_ERROR, customer=customer)
```


----

Testing is critical to finishing your code.

Code is not done being written until there are tests.

Code without tests is broken.

How can the language itself make test writing easier / faster / friendlier?

 * reserve `_test_*` as a special prefix on names.  Testing apparati should
   scan for those and treat them as callables that return / throw in
   predictable ways
 * Have some kind of syntactic way to associate functions / methods with 
   their corresponding unit test
 * Doctests are nice for simple, stateless functions
 * A symbol that marks objects that will fail compile without tests
 * One of these? ⦹ ⮿ ⸆ 〶 🜖 🞋 🝨 🛆  ⚖

```

    zany = function(a, b=3, c="foo") 🜖
        baz = a + b
        zap = c + baz
        return zap + baz

    # Make doctests explicit:

    wacky = function(a, b=3, c="foo")
        🜖"""
        wacky(1)
        > "foo4"

        wacky(1,1,'bar')
        > "bar2"
        """
        return c + str(a+b)

```

 * Maybe it could optionally specify the test path? 🜖(all_tests.test_zany)
 * Maybe the test could follow in-line:

```

    wacky = function(a, b=3, c="foo")
        return c + str(a+b)
        ⇤ 🜖
        assert(wacky(1), 'foo4')

```

 * Testing with mocks is a bit of a hassle.  But what are mocks other than
   declaring what values to use for the lexical scope of the function

```

    wacky = function(a, b=3, c="foo")
        return c + str(a+b)
        ⇤ 🜖 (arg values go here), (lexical scope values go here)
        # "sut" is a reserved keyword for System Under Test
        assert(sut(1), 'foo4')

```

 * Tests can be chained

```

    baz = 99
    wacky = function(a, b=3, c="foo")
        contents = file('/tmp/foo.txt').read()
        return str(baz) + c + str(a+b) + contents
        ⇤ 🜖 (
            kwargs = {'a': 1},
            builtin_scope = {'file': fake_file}
        )
        assert(sut(), '99foo4Hello World')
        ⇤ 🜖 (
            kwargs = {'a': 2},
            builtin_scope = {'file': fake_file},
            global_scope = {'baz': 88}
        )
        assert(sut(), '88foo5Hello World')

```

----

Addressing: `a = [1,2]; a[0]` - it's weird to use the same symbol, `[` for
both creation and addressing.

Also, it's weird to get 2 different kinds of exception, KeyError
and IndexError from the same-looking operation, `foo[x]`.
(You could also get TypeError, eg: `[1,2]['foo']`)
(You could also get AttributeError, eg: `None[3]`)

What about do addressing similar to how attributes are addressed?

```
    my_list = [1]
    my_dict = {'a':1}
    my_func = ⦗⦘ ⇥ a = 1 ⇤
    my_clss = ⟬⟭ ⇥ a = 1 ⇤
    my_inst = my_clss()

    my_list.[0]
    my_dict.{'a'}
    my_clss.a
    my_clss.⟬a⟭
    my_inst.a    # access the instance attr, falling back to class attr
                 # (falling back to the dict key?)
    my_inst.⟬a⟭  # access the class attribute
    my_clss.⦃a⦄  # access the instance attribute

    my_func.⦗a⦘  # should throw some kind of error
                 # or maybe some kind of inspection if the function body
                 # stack hasn't been garbage collected - handy for testing

```

Hmm... This would be possible:

```
    my_dict.'a'  # this one might encourage typos, and
                 # doesn't work for other types of key
```

What about:

```
    A = 'a'
    my_clss.⟬A⟭
    my_inst.⦃A⦄
    my_clss.⟬'a'⟭
    my_inst.⦃'a'⦄

```

Actually, I like that better than the above.  Maybe this rule should apply:

<name>.<name> :
    This one is the ultimate convenience, gun aimed at foot, hammer cocked
    access instance attr, falling back to class attr
    (and then falling back to dict key??? - it'd be more like JS that way)
<name>.<encloser> <expression> </encloser> :
    1. evaluate the expression
    2. use the value for a symbol-specific lookup
    3. maybe the expression is called a "Selector"?
<name>.<integer> :
    The above mentioned Decimal-default that is runtime-expensive and
    spits out a warning

Ok, now that we've gone this far, let's look at the quotes again...

```

    foo = 'asdf zab123zoob baz'

    foo."'bar'" # ??? SelectorError?
    foo."5"     # get the character at index 5
    foo."5:10"  # get the string at slice(5,10)
    foo."'zab(.*)zoob'"  # Regex?

    fob = [3, 4, 8, 16]

    fob.[1]     # 4
    fob.[1:3]   # [4,5]

    # If we consider this an overridable pattern, we could create a
    # DOM class whose instances could do stuff like this:
    dom."'#bar'"
    dom."'.bar'"

    # Though really, this might be a great example of the use of
    # the "enclosers" idea mentioned above.
    __module__.enclosers = {
        ❮❯ : getElementBy,
    }
    dom.❮'.foo'❯
    dom.❮'#bar'❯
    # It would be nice to make that more compact like:
    dom.❮.foo❯
    dom.❮#bar❯

```

Could we get js-style filtering?

```

    foo = [1,2,3,4,5]

    evens = foo.[⦗x⦘ ⇥  return x%2 == 0 ⇤]

    evens = foo.[⦗x⦘
        return x%2 == 0
    ]

    evens = foo.[
        ⦗x⦘
            return x%2 == 0
    ]

    # Which is better?
    evens = [x for x in foo if x%2 == 0]
    evens = foo.[⦗x⦘ ⇥  return x%2 == 0 ⇤]
    # Explicitness, compactness, one is an actual function declaration & call

```

If <name>.<name> is a convenient foot-gun, is there a way to *explicitly*
say "give me the instance attribute named bar"?
what about "give me the class attribute named bar"?

    <name>..<name>
    foo..bar
    # This could be a set-up for typo bugs though

    <name>.<encloser> <expression> </encloser>
    foo.|bar|
    foo.`bar`

    foo.|bar|  # instance attr
    foo.||bar||  # class attr
    foo.__class__.|bar|  # class attr

    <name>^<name>
    foo^bar
    foo~bar
    foo|bar

Or, I could switch it around and have
foo.bar be explicitly an attribute (like Python)
and foo~bar be liberally any query and a convenient foot-gun (like JS)

```
    foo = {'bar': 3, 'get': 5}

    foo.bar           # AttributeError
    foo.get           # <function>
    foo.get('bar')    # 3
    foo~bar           # 3
    foo~"bar"         # 3
    foo.__class__~bar # ???
    foo~get           # <function>

```

I don't think I like that.  The period symbol is already a
jack-of-all-trades due to it's use in numbers for floats / Decimals.

Hmm, what about polymorphism?

```
    first_two = ⦗a ⊩ @interface('sequence')⦘
        return a.[:2]
    first_two('asdf')
    first_two([1,2,3,4])

    first_two = ⦗a ⊩ @loose⦘
        return a.[:2]
    first_two('asdf')
    first_two([1,2,3,4])

```

----

How about default values for arguments?

Using equals sign is not great
 * How about one of these: ⊦ ⊧ ⤙ ⩦ ⩴ ⩷ ⫢ ⫨ ⫩
 * I like these: ⊦ ⊧ ⫨ ⫩
 * Best one is "MODELS" (1 char width): ⊧
 * &d shortcut for "defaults to"
 * This is a really common thing to do though, so it's a lot of typing

```

    z = function(a, b⊧3, c⊧"foo") ⊩ @method
        self.baz = a + b
        self.zap = c + self.baz

    z = ⦗a ⊩ @int, b ⊧ 3 ⊩ @int, c ⊧ "foo"⦘ ⊩ (@classmethod, @returns(int))
        cls.baz = a + b
        cls.zap = c + self.baz
        return cls.baz

```

There's a big difference between JS and Python here though, because in
JS the default values are evaluated at "call time", and in Python default
values are evaluated at "compile time".

----

Bugs can happen when you check for falsy / truthy and the kind of falsy/truthy
is different than what you expected.  It's a chance to catch a bug with
explicitness.

Maybe raw if/else should only check for booleans, but `@truthy()` is a
built-in language macro that calls __bool__ on members and returns


```

    if latitude:
        print 'Latitude was None'
        # BUG!  maybe it was actually 0.0??!?!
        # This is an insidious example, because most of the time latitude
        # would not be 0.0 (locations must be EXACTLY on the equator).
        # This bug might live for years before it ever exhibits

```

This is a bug because the writer had knowledge that `latitude` could be one of
two types, either a float or a None.  But they weren't considering that 0.0
would also be falsy.

What about adding shortcuts for the common truthy/falsy checks,
to be more careful and explicit?

```

    if myCollection.is_not_empty
        # do something with items from myCollection

    if myNumber.is_zero
        # do something with 0.0 or 0

```

That gets pretty verbose.

Use the symbol ⸮, maybe?
Or just the question mark "?"

```

    # Using enclosers is one idea, but it breaks down for numbers and None
    if myCollection.[?]
        # do something with items from myCollection

    if myCollection."?"
        # do something with items from myCollection

    # So just a simpler .? that implies a call to __bool__
    if myNumber.?
        # do something with 0.0 or 0

```

Another bug introduced by implicit falsy-ness:

```

x = latitude or longitude not in [180, -180]
...
if x == True
   print 'coordinate is not on a boundary'

```

In Python and Javascript, if the value of `latitude` is 1.0, then
the value of x will be 1.0.  So, `x == True` will be False.

This might be avoided by printing a warning whenever we see `== True`

But maybe changing the logic of what `or` and `and` do would be better.

But there's a lot of code that depends on the way `or` and `and` work...

We could introduce alternate operators:

 * `or` behaves the way it does in JS and Python
 * `⧽OR⧼` always returns a boolean value


----

Enumerated types:

```
™(
    'salt',
    'coriander',
    'cinnamon',
)

...

foo = 'corriandar'™  # throws an exception

```

I don't know how valuable this is though, and it's a bit of a hack

How about this: the ™ is just a hint to the compiler and the version
control system.  For the compiler, there's a leventshien-distance
threshold that, if exceeded, causes an error and for the version
control system, if one ™ string changes but not all of them do, then
there's an error.

