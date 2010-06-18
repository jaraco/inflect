
This is the Perl version of the documentation with some TODO comments added
TODO: edit to match the Python version
TODO: change the format
TODO: fix things below marked with TODO


=head1 NAME

Lingua::EN::Inflect - Convert singular to plural. Select "a" or "an".

=head1 VERSION

This document describes version 1.891 of Lingua::EN::Inflect

=head1 SYNOPSIS

 use Lingua::EN::Inflect qw ( PL PL_N PL_V PL_ADJ NO NUM
		  PL_eq PL_N_eq PL_V_eq PL_ADJ_eq
		  A AN
		  PART_PRES
		  ORD NUMWORDS
		  WORDLIST
		  inflect classical
		  def_noun def_verb def_adj def_a def_an ); 


 # UNCONDITIONALLY FORM THE PLURAL

      print "The plural of ", $word, " is ", PL($word), "\n";


 # CONDITIONALLY FORM THE PLURAL

      print "I saw $cat_count ", PL("cat",$cat_count), "\n";


 # FORM PLURALS FOR SPECIFIC PARTS OF SPEECH

      print PL_N("I",$N1), PL_V("saw",$N1),
	PL_ADJ("my",$N2), PL_N("saw",$N2), "\n";


 # DEAL WITH "0/1/N" -> "no/1/N" TRANSLATION:

      print "There ", PL_V("was",$errors), NO(" error",$errors), "\n";


 # USE DEFAULT COUNTS:

      print NUM($N1,""), PL("I"), PL_V(" saw"), NUM($N2), PL_N(" saw");
      print "There ", NUM($errors,''), PL_V("was"), NO(" error"), "\n";


 # COMPARE TWO WORDS "NUMBER-INSENSITIVELY":

      print "same\n"      if PL_eq($word1, $word2);
      print "same noun\n" if PL_eq_N($word1, $word2);
      print "same verb\n" if PL_eq_V($word1, $word2);
      print "same adj.\n" if PL_eq_ADJ($word1, $word2);


 # ADD CORRECT "a" OR "an" FOR A GIVEN WORD:

      print "Did you want ", A($thing), " or ", AN($idea), "\n";


 # CONVERT NUMERALS INTO ORDINALS (i.e. 1->1st, 2->2nd, 3->3rd, etc.)

      print "It was", ORD($position), " from the left\n";

 # CONVERT NUMERALS TO WORDS (i.e. 1->"one", 101->"one hundred and one", etc.)
 # IN A SCALAR CONTEXT: GET BACK A SINGLE STRING...

    $words = NUMWORDS(1234);      # "one thousand, two hundred and thirty-four"
    $words = NUMWORDS(ORD(1234)); # "one thousand, two hundred and thirty-fourth"


 # IN A LIST CONTEXT: GET BACK A LIST OF STRINGSi, ONE FOR EACH "CHUNK"...

    @words = NUMWORDS(1234);    # ("one thousand","two hundred and thirty-four")


 # OPTIONAL PARAMETERS CHANGE TRANSLATION:

    $words = NUMWORDS(12345, group=>1);
		# "one, two, three, four, five"

    $words = NUMWORDS(12345, group=>2);
		# "twelve, thirty-four, five"

    $words = NUMWORDS(12345, group=>3);
		# "one twenty-three, forty-five"

    $words = NUMWORDS(1234, 'and'=>'');
		# "one thousand, two hundred thirty-four"

    $words = NUMWORDS(1234, 'and'=>', plus');
		# "one thousand, two hundred, plus thirty-four" #TODO: I get no comma before plus: check perl

    $words = NUMWORDS(555_1202, group=>1, zero=>'oh');
		# "five, five, five, one, two, oh, two"

    $words = NUMWORDS(555_1202, group=>1, one=>'unity');
		# "five, five, five, unity, two, oh, two" #TODO: 'oh' is remembered. a bug?

    $words = NUMWORDS(123.456, group=>1, decimal=>'mark');
		# "one two three mark four five six"  #TODO: DOCBUG: perl gives commas here as do I
                                                      #TODO: 'unity' is remembered. a bug?

# LITERAL STYLE ONLY NAMES NUMBERS LESS THAN A CERTAIN THRESHOLD...

    $words = NUMWORDS(   9, threshold=>10);    # "nine"
    $words = NUMWORDS(  10, threshold=>10);    # "ten"
    $words = NUMWORDS(  11, threshold=>10);    # "11"
    $words = NUMWORDS(1000, threshold=>10);    # "1,000"

 # JOIN WORDS INTO A LIST:

    $list = WORDLIST("apple", "banana", "carrot");
		# "apple, banana, and carrot"

    $list = WORDLIST("apple", "banana");
		# "apple and banana"

    $list = WORDLIST("apple", "banana", "carrot", {final_sep=>""});
		# "apple, banana and carrot"


 # REQUIRE "CLASSICAL" PLURALS (EG: "focus"->"foci", "cherub"->"cherubim")

      classical;          # USE ALL CLASSICAL PLURALS

      classical 1;           #  USE ALL CLASSICAL PLURALS
      classical 0;           #  USE ALL MODERN PLURALS (DEFAULT)

      classical 'zero';      #  "no error" INSTEAD OF "no errors"
      classical zero=>1;     #  "no error" INSTEAD OF "no errors"
      classical zero=>0;     #  "no errors" INSTEAD OF "no error" 

      classical 'herd';      #  "2 buffalo" INSTEAD OF "2 buffalos"
      classical herd=>1;     #  "2 buffalo" INSTEAD OF "2 buffalos"
      classical herd=>0;     #  "2 buffalos" INSTEAD OF "2 buffalo"

      classical 'persons';   # "2 chairpersons" INSTEAD OF "2 chairpeople"
      classical persons=>1;  # "2 chairpersons" INSTEAD OF "2 chairpeople"
      classical persons=>0;  # "2 chairpeople" INSTEAD OF "2 chairpersons"

      classical 'ancient';   # "2 formulae" INSTEAD OF "2 formulas"
      classical ancient=>1;  # "2 formulae" INSTEAD OF "2 formulas"
      classical ancient=>0;  # "2 formulas" INSTEAD OF "2 formulae"



 # INTERPOLATE "PL()", "PL_N()", "PL_V()", "PL_ADJ()", A()", "AN()"
 # "NUM()" AND "ORD()" WITHIN STRINGS:

      print inflect("The plural of $word is PL($word)\n");
      print inflect("I saw $cat_count PL("cat",$cat_count)\n");
      print inflect("PL(I,$N1) PL_V(saw,$N1) PL(a,$N2) PL_N(saw,$N2)");
      print inflect("NUM($N1,)PL(I) PL_V(saw) NUM($N2,)PL(a) PL_N(saw)");
print inflect("I saw NUM($cat_count) PL("cat")\nNUM()");
print inflect("There PL_V(was,$errors) NO(error,$errors)\n");
print inflect("There NUM($errors,) PL_V(was) NO(error)\n";
print inflect("Did you want A($thing) or AN($idea)\n");
print inflect("It was ORD($position) from the left\n");


 # ADD USER-DEFINED INFLECTIONS (OVERRIDING INBUILT RULES):

      def_noun( "VAX", "VAXen" )  # SINGULAR => PLURAL

      def_verb( "will" , "shall",  # 1ST PERSON SINGULAR => PLURAL
                "will" , "will",   # 2ND PERSON SINGULAR => PLURAL
                "will" , "will")   # 3RD PERSON SINGULAR => PLURAL

      def_adj(  "hir"  , "their")  # SINGULAR => PLURAL

      def_a("h")        # "AY HALWAYS SEZ 'HAITCH'!"

      def_an(   "horrendous.*" )    # "AN HORRENDOUS AFFECTATION"


=head1 DESCRIPTION

The exportable subroutines of Lingua::EN::Inflect provide plural
inflections, "a"/"an" selection for English words, and manipulation
of numbers as words

Plural forms of all nouns, most verbs, and some adjectives are
provided. Where appropriate, "classical" variants (for example: "brother" ->
"brethren", "dogma" -> "dogmata", etc.) are also provided.

Pronunciation-based "a"/"an" selection is provided for all English
words, and most initialisms.

It is also possible to inflect numerals (1,2,3) to ordinals (1st, 2nd, 3rd)
and to english words ("one", "two", "three).

In generating these inflections, Lingua::EN::Inflect follows the Oxford
English Dictionary and the guidelines in Fowler's Modern English
Usage, preferring the former where the two disagree.

The module is built around standard British spelling, but is designed
to cope with common American variants as well. Slang, jargon, and
other English dialects are I<not> explicitly catered for.

Where two or more inflected forms exist for a single word (typically a
"classical" form and a "modern" form), Lingua::EN::Inflect prefers the
more common form (typically the "modern" one), unless "classical"
processing has been specified
(see L<"MODERN VS CLASSICAL INFLECTIONS">).

=head1 FORMING PLURALS

=head2 Inflecting Plurals

All of the C<PL_...> plural inflection subroutines take the word to be
inflected as their first argument and return the corresponding inflection.
Note that all such subroutines expect the I<singular> form of the word. The
results of passing a plural form are undefined (and unlikely to be correct).

The C<PL_...> subroutines also take an optional second argument,
which indicates the grammatical "number" of the word (or of another word
with which the word being inflected must agree). If the "number" argument is
supplied and is not C<1> (or C<"one"> or C<"a">, or some other adjective that
implies the singular), the plural form of the word is returned. If the
"number" argument I<does> indicate singularity, the (uninflected) word
itself is returned. If the number argument is omitted, the plural form
is returned unconditionally.

The various subroutines are:

=over 8

=item C<PL_N($;$)>

The exportable subroutine C<PL_N()> takes a I<singular> English noun or
pronoun and returns its plural. Pronouns in the nominative ("I" ->
"we") and accusative ("me" -> "us") cases are handled, as are
possessive pronouns ("mine" -> "ours").


=item C<PL_V($;$)>

The exportable subroutine C<PL_V()> takes the I<singular> form of a
conjugated verb (that is, one which is already in the correct "person"
and "mood") and returns the corresponding plural conjugation.


=item C<PL_ADJ($;$)>

The exportable subroutine C<PL_ADJ()> takes the I<singular> form of
certain types of adjectives and returns the corresponding plural form.
Adjectives that are correctly handled include: "numerical" adjectives
("a" -> "some"), demonstrative adjectives ("this" -> "these", "that" ->
"those"), and possessives ("my" -> "our", "cat's" -> "cats'", "child's"
-> "childrens'", etc.)


=item C<PL($;$)>

The exportable subroutine C<PL()> takes a I<singular> English noun,
pronoun, verb, or adjective and returns its plural form. Where a word
has more than one inflection depending on its part of speech (for
example, the noun "thought" inflects to "thoughts", the verb "thought"
to "thought"), the (singular) noun sense is preferred to the (singular)
verb sense.

Hence C<PL("knife")> will return "knives" ("knife" having been treated
as a singular noun), whereas C<PL("knifes")> will return "knife"
("knifes" having been treated as a 3rd person singular verb).

The inherent ambiguity of such cases suggests that,
where the part of speech is known, C<PL_N>, C<PL_V>, and
C<PL_ADJ> should be used in preference to C<PL>.

=back

Note that all these subroutines ignore any whitespace surrounding the
word being inflected, but preserve that whitespace when the result is
returned. For example, C<S<PL(" cat  ")>> returns S<" cats  ">.


=head2 Numbered plurals

The C<PL_...> subroutines return only the inflected word, not the count that
was used to inflect it. Thus, in order to produce "I saw 3 ducks", it
is necessary to use:

    print "I saw $N ", PL_N($animal,$N), "\n";

Since the usual purpose of producing a plural is to make it agree with
a preceding count, Lingua::EN::Inflect provides an exportable subroutine
(C<NO($;$)>) which, given a word and a(n optional) count, returns the
count followed by the correctly inflected word. Hence the previous
example can be rewritten:

    print "I saw ", NO($animal,$N), "\n";

In addition, if the count is zero (or some other term which implies
zero, such as C<"zero">, C<"nil">, etc.) the count is replaced by the
word "no". Hence, if C<$N> had the value zero, the previous example
would print the somewhat more elegant:

    I saw no animals

rather than:

    I saw 0 animals

Note that the name of the subroutine is a pun: the subroutine
returns either a number (a I<No.>) or a C<"no">, in front of the
inflected word.


=head2 Reducing the number of counts required

In some contexts, the need to supply an explicit count to the various
C<PL_...> subroutines makes for tiresome repetition. For example:

    print PL_ADJ("This",$errors), PL_N(" error",$errors),
          PL_V(" was",$errors), " fatal.\n";

Lingua::EN::Inflect therefore provides an exportable subroutine
(C<NUM($;$)>) which may be used to set a persistent "default number"
value. If such a value is set, it is subsequently used whenever an
optional second "number" argument is omitted. The default value thus set 
can subsequently be removed by calling C<NUM()> with no arguments.
Hence we could rewrite the previous example:

    NUM($errors);
    print PL_ADJ("This"), PL_N(" error"), PL_V(" was"), "fatal.\n";
    NUM();

Normally, C<NUM()> returns its first argument, so that it may also
be "inlined" in contexts like:

    print NUM($errors), PL_N(" error"), PL_V(" was"), " detected.\n"
    print PL_ADJ("This"), PL_N(" error"), PL_V(" was"), "fatal.\n"
        if $severity > 1;

However, in certain contexts (see L<"INTERPOLATING INFLECTIONS IN STRINGS">)
it is preferable that C<NUM()> return an empty string. Hence C<NUM()>
provides an optional second argument. If that argument is supplied (that is, if
it is defined) and evaluates to false, C<NUM> returns an empty string
instead of its first argument. For example:

    print NUM($errors,0), NO("error"), PL_V(" was"), " detected.\n";
    print PL_ADJ("This"), PL_N(" error"), PL_V(" was"), "fatal.\n"
        if $severity > 1;
    


=head2 Number-insensitive equality

Lingua::EN::Inflect also provides a solution to the problem
of comparing words of differing plurality through the exportable subroutines
C<PL_eq($$)>, C<PL_N_eq($$)>, C<PL_V_eq($$)>, and C<PL_ADJ_eq($$)>.
Each  of these subroutines takes two strings, and  compares them
using the corresponding plural-inflection subroutine (C<PL()>, C<PL_N()>,
C<PL_V()>, and C<PL_ADJ()> respectively).

The comparison returns true if:

=over 8

=item *

the strings are C<eq>-equal, or

=item *

one string is C<eq>-equal to a plural form of the other, or

=item *

the strings are two different plural forms of the one word.

=back

Hence all of the following return true:

    PL_eq("index","index")      # RETURNS "eq"
    PL_eq("index","indexes")    # RETURNS "s:p"
    PL_eq("index","indices")    # RETURNS "s:p"
    PL_eq("indexes","index")    # RETURNS "p:s"
    PL_eq("indices","index")    # RETURNS "p:s"
    PL_eq("indices","indexes")  # RETURNS "p:p"
    PL_eq("indexes","indices")  # RETURNS "p:p"
    PL_eq("indices","indices")  # RETURNS "eq"

As indicated by the comments in the previous example, the actual value
returned by the various C<PL_eq_...> subroutines encodes which of the
three equality rules succeeded: "eq" is returned if the strings were
identical, "s:p" if the strings were singular and plural respectively,
"p:s" for plural and singular, and "p:p" for two distinct plurals.
Inequality is indicated by returning an empty string.

It should be noted that two distinct singular words which happen to take
the same plural form are I<not> considered equal, nor are cases where
one (singular) word's plural is the other (plural) word's singular.
Hence all of the following return false:

    PL_eq("base","basis")       # ALTHOUGH BOTH -> "bases"
    PL_eq("syrinx","syringe")   # ALTHOUGH BOTH -> "syringes"
    PL_eq("she","he")       # ALTHOUGH BOTH -> "they"

    PL_eq("opus","operas")      # ALTHOUGH "opus" -> "opera" -> "operas"
    PL_eq("taxi","taxes")       # ALTHOUGH "taxi" -> "taxis" -> "taxes"

Note too that, although the comparison is "number-insensitive" it is I<not>
case-insensitive (that is, C<PL("time","Times")> returns false. To obtain
both number and case insensitivity, prefix both arguments with C<lc>
(that is, C<PL(lc "time", lc "Times")> returns true).


=head1 OTHER VERB FORMS

=head2 Present participles

C<Lingua::EN::Inflect> also provides the C<PART_PRES> subroutine,
which can take a 3rd person singular verb and
correctly inflect it to its present participle:

    PART_PRES("runs")   # "running"
    PART_PRES("loves")  # "loving"
    PART_PRES("eats")   # "eating"
    PART_PRES("bats")   # "batting"
    PART_PRES("spies")  # "spying"


=head1 PROVIDING INDEFINITE ARTICLES

=head2 Selecting indefinite articles

Lingua::EN::Inflect provides two exportable subroutines (C<A($;$)> and
C<AN($;$)>) which will correctly prepend the appropriate indefinite
article to a word, depending on its pronunciation. For example:

    A("cat")        # -> "a cat"
    AN("cat")       # -> "a cat"
    A("euphemism")      # -> "a euphemism"
    A("Euler number")   # -> "an Euler number"
    A("hour")       # -> "an hour"
    A("houri")      # -> "a houri"

The two subroutines are I<identical> in function and may be used
interchangeably. The only reason that two versions are provided is to
enhance the readability of code such as:

    print "That is ", AN($errortype), " error\n;
    print "That is ", A($fataltype), " fatal error\n;

Note that in both cases the actual article provided depends I<only> on
the pronunciation of the first argument, I<not> on the name of the
subroutine.

C<A()> and C<AN()> will ignore any indefinite article that already
exists at the start of the string. Thus:

    @half_arked = (
        "a elephant",
        "a giraffe",
        "an ewe",
        "a orangutan",
    );

    print A($_), "\n" for @half_arked;

    # prints:
    #     an elephant
    #     a giraffe
    #     a ewe
    #     an orangutan


C<A()> and C<AN()> both take an optional second argument. As with the
C<PL_...> subroutines, this second argument is a "number" specifier. If
its value is C<1> (or some other value implying singularity), C<A()> and
C<AN()> insert "a" or "an" as appropriate. If the number specifier 
implies plurality, (C<A()> and C<AN()> insert the actual second argument instead.
For example:

    A("cat",1)      # -> "a cat"
    A("cat",2)      # -> "2 cat"
    A("cat","one")      # -> "one cat"
    A("cat","no")       # -> "no cat"

Note that, as implied by the previous examples, C<A()> and
C<AN()> both assume that their job is merely to provide the correct
qualifier for a word (that is: "a", "an", or the specified count).
In other words, they assume that the word they are given has
already been correctly inflected for plurality. Hence, if C<$N> 
has the value 2, then:

      print A("cat",$N);

prints "2 cat", instead of "2 cats". The correct approach is to use:

      print A(PL("cat",$N),$N);

or, better still:

      print NO("cat",$N);

Note too that, like the various C<PL_...> subroutines, whenever C<A()>
and C<AN()> are called with only one argument they are subject to the
effects of any preceding call to C<NUM()>. Hence, another possible
solution is:

      NUM($N);
      print A(PL("cat"));
    

=head2 Indefinite articles and initialisms

"Initialisms" (sometimes inaccurately called "acronyms") are terms which
have been formed from the initial letters of words in a phrase (for
example, "NATO", "NBL", "S.O.S.", "SCUBA", etc.)

Such terms present a particular challenge when selecting between "a"
and "an", since they are sometimes pronounced as if they were a single
word ("nay-tow", "sku-ba") and sometimes as a series of letter names
("en-eff-ell", "ess-oh-ess").

C<A()> and C<AN()> cope with this dichotomy using a series of inbuilt
rules, which may be summarized as:

=over 8

=item 1.

If the word starts with a single letter, followed by a period or dash
(for example, "R.I.P.", "C.O.D.", "e-mail", "X-ray", "T-square"), then
choose the appropriate article for the I<sound> of the first letter
("an R.I.P.", "a C.O.D.", "an e-mail", "an X-ray", "a T-square").

=item 2.

If the first two letters of the word are capitals,
consonants, and do not appear at the start of any known English word,
(for example, "LCD", "XML", "YWCA"), then once again choose "a" or
"an" depending on the I<sound> of the first letter ("an LCD", "an
XML", "a YWCA").

=item 3.

Otherwise, assume the string is a capitalized word or a
pronounceable initialism (for example, "LED", "OPEC", "FAQ", "UNESCO"), and
therefore takes "a" or "an" according to the (apparent) pronunciation of
the entire word ("a LED", "an OPEC", "a FAQ", "a UNESCO").

=back

Note that rules 1 and 3 together imply that the presence or absence of
punctuation may change the selection of indefinite article for a
particular initialism (for example, "a FAQ" but "an F.A.Q.").


=head2 Indefinite articles and "soft H's"

Words beginning in the letter 'H' present another type of difficulty
when selecting a suitable indefinite article. In a few such words
(for example, "hour", "honour", "heir") the 'H' is not voiced at
all, and so such words inflect with "an". The remaining cases
("voiced H's") may be divided into two categories:
"hard H's" (such as "hangman", "holograph", "hat", etc.) and
"soft H's" (such as "hysterical", "horrendous", "holy", etc.)

Hard H's always take "a" as their indefinite article, and soft
H's normally do so as well. But I<some> English speakers prefer
"an" for soft H's (although the practice is now generally considered an
affectation, rather than a legitimate grammatical alternative).

At present, the C<A()> and C<AN()> subroutines ignore soft H's and use
"a" for any voiced 'H'. The author would, however, welcome feedback on
this decision (envisaging a possible future "soft H" mode).


=head1 INFLECTING ORDINALS

Occasionally it is useful to present an integer value as an ordinal
rather than as a numeral. For example:

    Enter password (1st attempt): ********
    Enter password (2nd attempt): *********
    Enter password (3rd attempt): *********
    No 4th attempt. Access denied.

To this end, Lingua::EN::Inflect provides the C<ORD()> subroutine.
<ORD()> takes a single argument and forms its ordinal equivalent.
If the argument isn't a numerical integer, it just adds "-th".


=head1 CONVERTING NUMBERS TO WORDS

The exportable subroutine C<NUMWORDS> takes a number (cardinal or ordinal)
and returns an English representation of that number. In a scalar context 
a string is returned. Hence:

    use Lingua::EN::Inflect qw( NUMWORDS );

    $words = NUMWORDS(1234567);

puts the string:

    "one million, two hundred and thirty-four thousand, five hundred and sixty-seven"
    
into $words.

In a list context each comma-separated chunk is returned as a separate element.
Hence:

    @words = NUMWORDS(1234567);

puts the list:

    ("one million",
     "two hundred and thirty-four thousand",
     "five hundred and sixty-seven")

into @words.

Non-digits (apart from an optional leading plus or minus sign,
any decimal points, and ordinal suffixes -- see below) are silently
ignored, so the following all produce identical results:

        NUMWORDS(5551202);
        NUMWORDS(5_551_202);
        NUMWORDS("5,551,202");
        NUMWORDS("555-1202");

That last case is a little awkward since it's almost certainly a phone number,
and "five million, five hundred and fifty-one thousand, two hundred and two"
probably isn't what's wanted.

To overcome this, C<NUMWORDS()> takes an optional named argument, 'group',
which changes how numbers are translated. The argument must be a
positive integer less than four, which indicated how the digits of the
number are to be grouped. If the argument is C<1>, then each digit is
translated separately. If the argument is C<2>, pairs of digits
(starting from the I<left>) are grouped together. If the argument is
C<3>, triples of numbers (again, from the I<left>) are grouped. Hence:

        NUMWORDS("555-1202", group=>1)

returns C<"five, five, five, one, two, zero, two">, whilst:

        NUMWORDS("555-1202", group=>2)

returns C<"fifty-five, fifty-one, twenty, two">, and:

        NUMWORDS("555-1202", group=>3)

returns C<"five fifty-five, one twenty, two">.

Phone numbers are often written in words as
C<"five..five..five..one..two..zero..two">, which is also easy to
achieve:

        join '..', NUMWORDS("555-1202", group=>1)

C<NUMWORDS> also handles decimal fractions. Hence:

        NUMWORDS("1.2345")

returns C<"one point two three four five"> in a scalar context
and C<("one","point","two","three","four","five")>) in an array context.
Exponent form (C<"1.234e56">) is not yet handled.

Multiple decimal points are only translated in one of the "grouping" modes.
Hence:

        NUMWORDS(101.202.303)

returns C<"one hundred and one point two zero two three zero three">,
whereas:

        NUMWORDS(101.202.303, group=>1)

returns C<"one zero one point two zero two point three zero three">.

The digit C<'0'> is unusual in that in may be translated to English as "zero",
"oh", or "nought". To cater for this diversity, C<NUMWORDS> may be passed
a named argument, 'zero', which may be set to
the desired translation of C<'0'>. For example:

        print join "..", NUMWORDS("555-1202", group=>3, zero=>'oh')

prints C<"five..five..five..one..two..oh..two">.
By default, zero is rendered as "zero".

Likewise, the digit C<'1'> may be rendered as "one" or "a/an" (or very
occasionally other variants), depending on the context. So there is a
C<'one'> argument as well:

        print NUMWORDS($_, one=>'a solitary', zero=>'no more'),
              PL(" bottle of beer on the wall\n", $_)
                   for (3,2,1,0);

        # prints:
        #     three bottles of beer on the wall
        #     two bottles of beer on the wall
        #     a solitary bottle of beer on the wall
        #     no more bottles of beer on the wall
              
Care is needed if the word "a/an" is to be used as a C<'one'> value.
Unless the next word is known in advance, it's almost always necessary
to use the C<A> function as well:

        print A( NUMWORDS(1, one=>'a') . " $_\n")
         for qw(cat aardvark ewe hour);   

    # prints:
    #     a cat
    #     an aardvark
    #     a ewe
    #     an hour

Another major regional variation in number translation is the use of
"and" in certain contexts. The named argument 'and'
allows the programmer to specify how "and" should be handled. Hence:

        print scalar NUMWORDS("765", 'and'=>'')

prints "seven hundred sixty-five", instead of "seven hundred and sixty-five".
By default, the "and" is included.

The translation of the decimal point is also subject to variation
(with "point", "dot", and "decimal" being the favorites).
The named argument 'decimal' allows the
programmer to how the decimal point should be rendered. Hence:

        print scalar NUMWORDS("666.124.64.101", group=>3, decimal=>'dot')

prints "six sixty-six, dot, one twenty-four, dot, sixty-four, dot, one zero one"
By default, the decimal point is rendered as "point".

C<NUMWORDS> also handles the ordinal forms of numbers. So:

        print scalar NUMWORDS('1st');
        print scalar NUMWORDS('3rd');
        print scalar NUMWORDS('202nd');
        print scalar NUMWORDS('1000000th');

print:

        first
        third
        two hundred and twenty-second
        one millionth

Two common idioms in this regard are:

        print scalar NUMWORDS(ORD($number));

and:

        print scalar ORD(NUMWORDS($number));

These are identical in effect, except when $number contains a decimal:

        $number = 99.09;
        print scalar NUMWORDS(ORD($number));    # ninety-ninth point zero nine
        print scalar ORD(NUMWORDS($number));    # ninety-nine point zero ninth

Use whichever you feel is most appropriate.


=head1 CONVERTING LISTS OF WORDS TO PHRASES

When creating a list of words, commas are used between adjacent items,
except if the items contain commas, in which case semicolons are used.
But if there are less than two items, the commas/semicolons are omitted
entirely. The final item also has a conjunction (usually "and" or "or")
before it. And although it's technically incorrect (and sometimes
misleading), some people prefer to omit the comma before that final
conjunction, even when there are more than two items.

That's complicated enough to warrant its own subroutine: C<WORDLIST()>.
This subroutine expects a list of words, possibly with one or more hash
references containing options. It returns a string that joins the list
together in the normal English usage. For example:

    print "You chose ", WORDLIST(@selected_items), "\n";
    # You chose barley soup, roast beef, and Yorkshire pudding

    print "You chose ", WORDLIST(@selected_items, {final_sep=>""}), "\n";
    # You chose barley soup, roast beef and Yorkshire pudding

    print "Please chose ", WORDLIST(@side_orders, {conj=>"or"}), "\n";
    # Please chose salad, vegetables, or ice-cream

The available options are:

    Option named    Specifies                Default value

    conj            Final conjunction        "and"
    sep             Inter-item separator     ","
    last_sep        Final separator          value of 'sep' option


=head1 INTERPOLATING INFLECTIONS IN STRINGS

By far the commonest use of the inflection subroutines is to
produce message strings for various purposes. For example:

        print NUM($errors), PL_N(" error"), PL_V(" was"), " detected.\n";
        print PL_ADJ("This"), PL_N(" error"), PL_V(" was"), "fatal.\n"
                if $severity > 1;

Unfortunately the need to separate each subroutine call detracts
significantly from the readability of the resulting code. To ameliorate
this problem, Lingua::EN::Inflect provides an exportable string-interpolating
subroutine (C<inflect($)>), which recognizes calls to the various inflection
subroutines within a string and interpolates them appropriately.

Using C<inflect> the previous example could be rewritten:

        print inflect "NUM($errors) PL_N(error) PL_V(was) detected.\n";
        print inflect "PL_ADJ(This) PL_N(error) PL_V(was) fatal.\n"
                if $severity > 1;

Note that C<inflect> also correctly handles calls to the C<NUM()> subroutine
(whether interpolated or antecedent). The C<inflect()> subroutine has
a related extra feature, in that it I<automatically> cancels any "default
number" value before it returns its interpolated string. This means that
calls to C<NUM()> which are embedded in an C<inflect()>-interpolated
string do not "escape" and interfere with subsequent inflections.


=head1 MODERN VS CLASSICAL INFLECTIONS

Certain words, mainly of Latin or Ancient Greek origin, can form
plurals either using the standard English "-s" suffix, or with 
their original Latin or Greek inflections. For example:

        PL("stigma")            # -> "stigmas" or "stigmata"
        PL("torus")             # -> "toruses" or "tori"
        PL("index")             # -> "indexes" or "indices"
        PL("millennium")        # -> "millenniums" or "millennia"
        PL("ganglion")          # -> "ganglions" or "ganglia"
        PL("octopus")           # -> "octopuses" or "octopodes"


Lingua::EN::Inflect caters to such words by providing an
"alternate state" of inflection known as "classical mode".
By default, words are inflected using their contemporary English
plurals, but if classical mode is invoked, the more traditional 
plural forms are returned instead.

The exportable subroutine C<classical()> controls this feature.
If C<classical()> is called with no arguments, it unconditionally
invokes classical mode. If it is called with a single argument, it
turns all classical inflects on or off (depending on whether the argument is
true or false). If called with two or more arguments, those arguments 
specify which aspects of classical behaviour are to be used.

Thus:

        classical;                  # SWITCH ON CLASSICAL MODE
        print PL("formula");        # -> "formulae"

        classical 0;                # SWITCH OFF CLASSICAL MODE
        print PL("formula");        # -> "formulas"

        classical $cmode;           # CLASSICAL MODE IFF $cmode
        print PL("formula");        # -> "formulae" (IF $cmode)
                                    # -> "formulas" (OTHERWISE)

        classical herd=>1;          # SWITCH ON CLASSICAL MODE FOR "HERD" NOUNS
        print PL("wilderbeest");    # -> "wilderbeest"

        classical names=>1;         # SWITCH ON CLASSICAL MODE FOR NAMES
        print PL("sally");          # -> "sallies"
        print PL("Sally");          # -> "Sallys"

Note however that C<classical()> has no effect on the inflection of words which
are now fully assimilated. Hence:

        PL("forum")             # ALWAYS -> "forums"
        PL("criterion")         # ALWAYS -> "criteria"

LEI assumes that a capitalized word is a person's name. So it forms the
plural according to the rules for names (which is that you don't
inflect, you just add -s or -es). You can choose to turn that behaviour
off (it's on by the default, even when the module isn't in classical
mode) by calling C< classical(names=>0) >;

=head1 USER-DEFINED INFLECTIONS

=head2 Adding plurals at run-time

Lingua::EN::Inflect provides five exportable subroutines which allow
the programmer to override the module's behaviour for specific cases:

=over 8

=item C<def_noun($$)>

The C<def_noun> subroutine takes a pair of string arguments: the singular and the
plural forms of the noun being specified. The singular form 
specifies a pattern to be interpolated (as C<m/^(?:$first_arg)$/i>).
Any noun matching this pattern is then replaced by the string in the
second argument. The second argument specifies a string which is
interpolated after the match succeeds, and is then used as the plural
form. For example:

      def_noun  'cow'        => 'kine';
      def_noun  '(.+i)o'     => '$1i';
      def_noun  'spam(mer)?' => '\\$\\%\\@#\\$\\@#!!';

Note that both arguments should usually be specified in single quotes,
so that they are not interpolated when they are specified, but later (when
words are compared to them). As indicated by the last example, care
also needs to be taken with certain characters in the second argument,
to ensure that they are not unintentionally interpolated during comparison.

The second argument string may also specify a second variant of the plural
form, to be used when "classical" plurals have been requested. The beginning
of the second variant is marked by a '|' character:

      def_noun  'cow'        => 'cows|kine';
      def_noun  '(.+i)o'     => '$1os|$1i';
      def_noun  'spam(mer)?' => '\\$\\%\\@#\\$\\@#!!|varmints';

If no classical variant is given, the specified plural form is used in
both normal and "classical" modes.

If the second argument is C<undef> instead of a string, then the
current user definition for the first argument is removed, and the
standard plural inflection(s) restored.

Note that in all cases, later plural definitions for a particular
singular form replace earlier definitions of the same form. For example:

      # FIRST, HIDE THE MODERN FORM....
      def_noun  'aviatrix' => 'aviatrices';

      # LATER, HIDE THE CLASSICAL FORM...
      def_noun  'aviatrix' => 'aviatrixes';

      # FINALLY, RESTORE THE DEFAULT BEHAVIOUR...
      def_noun  'aviatrix' => undef;


Special care is also required when defining general patterns and
associated specific exceptions: put the more specific cases I<after>
the general pattern. For example:

      def_noun  '(.+)us' => '$1i';      # EVERY "-us" TO "-i"
      def_noun  'bus'    => 'buses';    # EXCEPT FOR "bus"

This "try-most-recently-defined-first" approach to matching
user-defined words is also used by C<def_verb>, C<def_a> and C<def_an>.


=item C<def_verb($$$$$$)>

The C<def_verb> subroutine takes three pairs of string arguments (that is, six
arguments in total), specifying the singular and plural forms of the three
"persons" of verb. As with C<def_noun>, the singular forms are specifications of
run-time-interpolated patterns, whilst the plural forms are specifications of
(up to two) run-time-interpolated strings:

       def_verb 'am'       => 'are',
                'are'      => 'are|art",
                'is'       => 'are';

       def_verb 'have'     => 'have',
                'have'     => 'have",
                'ha(s|th)' => 'have';

Note that as with C<def_noun>, modern/classical variants of plurals
may be separately specified, subsequent definitions replace previous
ones, and C<undef>'ed plural forms revert to the standard behaviour.


=item C<def_adj($$)>

The C<def_adj> subroutine takes a pair of string arguments, which specify
the singular and plural forms of the adjective being defined.
As with C<def_noun> and C<def_adj>, the singular forms are specifications of
run-time-interpolated patterns, whilst the plural forms are specifications of
(up to two) run-time-interpolated strings:

       def_adj  'this'     => 'these',
       def_adj  'red'      => 'red|gules',

As previously, modern/classical variants of plurals
may be separately specified, subsequent definitions replace previous
ones, and C<undef>'ed plural forms revert to the standard behaviour.


=item C<def_a($)> and C<def_an($)>

The C<def_a> and C<def_an> subroutines each take a single argument, which
specifies a pattern. If a word passed to C<A()> or C<AN()> matches this
pattern, it will be prefixed (unconditionally) with the corresponding indefinite
article. For example:

      def_a  'error';
      def_a  'in.+';

      def_an 'mistake';
      def_an 'error';

As with the other C<def_...> subroutines, such redefinitions are sequential
in effect so that, after the above example, "error" will be inflected with "an".

=back

=head2 The F<$HOME/.inflectrc> file

When it is imported, Lingua::EN::Inflect executes (as Perl code)
the contents of any file named F<.inflectrc> which it finds in the
in the directory where F<Lingua/EN/Inflect.pm> is installed,
or in the current home directory (C<$ENV{HOME}>), or in both.
Note that the code is executed within the Lingua::EN::Inflect
namespace.

Hence the user or the local Perl guru can make appropriate calls to
C<def_noun>, C<def_verb>, etc. in one of these F<.inflectrc> files, to
permanently and universally modify the behaviour of the module. For example

      > cat /usr/local/lib/perl5/Text/Inflect/.inflectrc

      def_noun  "UNIX"  => "UN*X|UNICES";

      def_verb  "teco"  => "teco",      # LITERALLY: "to edit with TECO"
                "teco"  => "teco",
                "tecos" => "teco";

      def_a     "Euler.*";              # "Yewler" TURNS IN HIS GRAVE


Note that calls to the C<def_...> subroutines from within a program
will take precedence over the contents of the home directory
F<.inflectrc> file, which in turn takes precedence over the system-wide
F<.inflectrc> file.


=head1 DIAGNOSTICS

On loading, if the Perl code in a F<.inflectrc> file is invalid
(syntactically or otherwise), an appropriate fatal error is issued.
A common problem is not ending the file with something that
evaluates to true (as the five C<def_...> subroutines do).

Using the five C<def_...> subroutines directly in a program may also
result in fatal diagnostics, if a (singular) pattern or an interpolated
(plural) string is somehow invalid.

Specific diagnostics related to user-defined inflections are:

=over 8

=item C<"Bad user-defined singular pattern:\n\t %s">

The singular form of a user-defined noun or verb
(as defined by a call to C<def_noun>, C<def_verb>, C<def_adj>,
C<def_a> or C<def_an>) is not a valid Perl regular expression. The
actual Perl error message is also given.

=item C<"Bad user-defined plural string: '%s'">

The plural form(s) of a user-defined noun or verb
(as defined by a call to C<def_noun>, C<def_verb> or C<def_adj>)
is not a valid Perl interpolated string (usually because it 
interpolates some undefined variable).

=item C<"Bad .inflectrc file (%s):\n %s">

Some other problem occurred in loading the named local 
or global F<.inflectrc> file. The Perl error message (including
the line number) is also given.

=back

There are I<no> diagnosable run-time error conditions for the actual
inflection subroutines, except C<NUMWORDS> and hence no run-time
diagnostics. If the inflection subroutines are unable to form a plural
via a user-definition or an inbuilt rule, they just "guess" the
commonest English inflection: adding "-s" for nouns, removing "-s" for
verbs, and no inflection for adjectives.

C<Lingua::EN::Inflect::NUMWORDS()> can C<die> with the following messages:

=over 8

=item C<"Bad grouping option: %s">

The optional argument to C<NUMWORDS()> wasn't 1, 2 or 3.

=item C<"Number out of range">

C<NUMWORDS()> was passed a number larger than
999,999,999,999,999,999,999,999,999,999,999,999 (that is: nine hundred
and ninety-nine decillion, nine hundred and ninety-nine nonillion, nine
hundred and ninety-nine octillion, nine hundred and ninety-nine
septillion, nine hundred and ninety-nine sextillion, nine hundred and
ninety-nine quintillion, nine hundred and ninety-nine quadrillion, nine
hundred and ninety-nine trillion, nine hundred and ninety-nine billion,
nine hundred and ninety-nine million, nine hundred and ninety-nine
thousand, nine hundred and ninety-nine :-) 

The problem is that C<NUMWORDS> doesn't know any
words for number components bigger than "decillion".


=head1 OTHER ISSUES

=head2 2nd Person precedence

If a verb has identical 1st and 2nd person singular forms, but
different 1st and 2nd person plural forms, then when its plural is
constructed, the 2nd person plural form is always preferred.

The author is not currently aware of any such verbs in English, but is
not quite arrogant enough to assume I<ipso facto> that none exist.


=head2 Nominative precedence

The singular pronoun "it" presents a special problem because its plural form
can vary, depending on its "case". For example:

        It ate my homework       ->  They ate my homework
        It ate it                ->  They ate them
        I fed my homework to it  ->  I fed my homework to them

As a consequence of this ambiguity, C<PL()> or C<PL_N> have been implemented
so that they always return the I<nominative> plural (that is, "they").

However, when asked for the plural of an unambiguously I<accusative>
"it" (namely, C<PL("to it")>, C<PL_N("from it")>, C<PL("with it")>,
etc.), both subroutines will correctly return the accusative plural
("to them", "from them", "with them", etc.)


=head2 The plurality of zero

The rules governing the choice between:

      There were no errors.

and

      There was no error.

are complex and often depend more on I<intent> rather than I<content>.
Hence it is infeasible to specify such rules algorithmically.

Therefore, Lingua::EN::Text contents itself with the following compromise: If
the governing number is zero, inflections always return the plural form
unless the appropriate "classical" inflection is in effect, in which case the
singular form is always returned.

Thus, the sequence:

      NUM(0);
      print inflect "There PL(was) NO(choice)";

produces "There were no choices", whereas:

      classical 'zero';     # or: classical(zero=>1);
      NUM(0);
      print inflect "There PL(was) NO(choice)";

it will print "There was no choice".


=head2 Homographs with heterogeneous plurals

Another context in which intent (and not content) sometimes determines
plurality is where two distinct meanings of a word require different
plurals. For example:

      Three basses were stolen from the band's equipment trailer.
      Three bass were stolen from the band's aquarium.

      I put the mice next to the cheese.
      I put the mouses next to the computers.

      Several thoughts about leaving crossed my mind.
      Several thought about leaving across my lawn.

Lingua::EN::Inflect handles such words in two ways:

=over 8

=item *

If both meanings of the word are the I<same> part of speech (for
example, "bass" is a noun in both sentences above), then one meaning
is chosen as the "usual" meaning, and only that meaning's plural is
ever returned by any of the inflection subroutines.

=item *

If each meaning of the word is a different part of speech (for
example, "thought" is both a noun and a verb), then the noun's
plural is returned by C<PL()> and C<PL_N()> and the verb's plural is
returned only by C<PL_V()>.

=back

Such contexts are, fortunately, uncommon (particularly
"same-part-of-speech" examples). An informal study of nearly 600
"difficult plurals" indicates that C<PL()> can be relied upon to "get
it right" about 98% of the time (although, of course, ichthyophilic
guitarists or cyber-behaviouralists may experience higher rates of
confusion).

If the choice of a particular "usual inflection" is considered
inappropriate, it can always be reversed with a preliminary call
to the corresponding C<def_...> subroutine.

=head1 NOTE

I'm not taking any further correspondence on:

=over

=item "octopi".

Despite the populist pandering of certain New World dictionaries, the
plural is "octopuses" or (for the pendantic classicist) "octopodes". The
suffix "-pus" is Greek, not Latin, so the plural is "-podes", not "pi".


=item "virus".

Had no plural in Latin (possibly because it was a mass noun).
The only plural is the Anglicized "viruses".

=back

=head1 AUTHORS

Damian Conway (damian@conway.org)
Matthew Persico (ORD inflection)


=head1 BUGS AND IRRITATIONS

The endless inconsistencies of English.

(I<Please> report words for which the correct plural or
indefinite article is not formed, so that the reliability
of Lingua::EN::Inflect can be improved.)



=head1 COPYRIGHT

 Copyright (c) 1997-2000, Damian Conway. All Rights Reserved.
 This module is free software. It may be used, redistributed
     and/or modified under the same terms as Perl itself.

"""
