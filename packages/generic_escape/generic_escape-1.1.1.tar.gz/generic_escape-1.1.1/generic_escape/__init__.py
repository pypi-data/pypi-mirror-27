
import re
from itertools import chain as ichain
from ._version import version as __version__

__all__ = ['GenericEscape','GenericQuote']

def re_one_of(xs):
    """return a regex string that matches one of the xs"""
    # the "a^" thing matches nothing on purpose (not even with re.M).
    # it is necessary in the case where `xs` is empty because then the
    # regex is "" which then matches the empty string -- oops.
    escape = re.escape
    xs = sorted(xs, key=len, reverse=True)
    return '|'.join(escape(x) for x in xs) if xs else 'a^'

class GenericEscape(object):
    r"""You should most definitely subclass this.

>>> ge = GenericEscape()
>>> ge.escape('a\nb')
'a\\nb'

The `unescape` method returns a tuple (end_position, unescaped_string).
>>> ge.unescape('a\\nb')
(4, 'a\nb')

Note that unescaping stops when an unescaped sequence is encountered, UNLESS it
is in `unescape_whitelist`.
>>> ge.unescape("ab\\nxy\nc")
(6, 'ab\nxy')

The `unescape_split` method can be used as a generalized str.split.
>>> ge.escaped[" " ] = r"\s"
>>> ge.escaped["\t"] = r"\t"
>>> ge.update()
>>> import re
>>> ge.unescape_split("a b c", " ")
(5, ['a', 'b', 'c'])
>>> ge.unescape_split("a\sb   c\t\t d", re.compile("[ \t]+"))[1]
['a b', 'c', 'd']
"""
    escaped = {"\\": r"\\",
               "\'": r"\'",
               "\"": r"\"",
               "\n": r"\n"}
    unescape_whitelist = set()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update()
    
    def update(self):
        e = self.escaped
        
        self._escape_re = re.compile(re_one_of(e.keys()), re.DOTALL)
        
        self._unescape_re = re.compile(
            '({})|({})'.format(*[
                re_one_of(X)
                for X in [e.values(), frozenset(e.keys()).difference(
                        self.unescape_whitelist)]]), re.DOTALL)
        
        self._escape_dict = e
        self._unescape_dict = {v:k for k,v in e.items()}
    
    def unescape(self, string, *, start_position=0):
        """returns (end_position, unescaped_string)"""
        unescape_re   = self._unescape_re
        unescape_dict = self._unescape_dict
        r = []
        i = start_position
        len_string = len(string)
        while True:
            m = unescape_re.search(string, i)
            if m:
                r.append(string[i:m.start()])
                good, bad = m.groups()
                if good is not None:
                    i = m.end()
                    r.append(unescape_dict[good])
                else: # bad is not None
                    i = m.start()
                    break
            else: # rest of string is kosher, use it as-is
                r.append(string[i:])
                i = len(string)
                break
        
        return (i, ''.join(r))
    
    def unescape_split(self, string, delimiter, *, start_position=0, maxsplit=None):
        """`delimiter` must be string or regex
returns (end_position, list_of_strings)"""
        if isinstance(delimiter, str):
            delimiter = re.compile(re.escape(delimiter))
        result = []
        splitcount = 0
        i = start_position
        while True:
            i, field = self.unescape(string, start_position=i)
            result.append(field)
            if maxsplit is not None and splitcount >= maxsplit:
                break
            m = delimiter.match(string, i)
            if not m:
                break
            i = m.end()
            splitcount += 1
        return (i, result)
    
    def escape(self, string):
        """returns escaped string"""
        escape_dict = self._escape_dict
        return self._escape_re.sub(lambda m:escape_dict[m.group()], string)

class UnquoteError(ValueError):
    pass

class NoStartingQuoteError(UnquoteError):
    pass

class NoEndingQuoteError(UnquoteError):
    pass

class GenericQuote(object):
    r"""You should most definitely subclass this.

`quoting_delimiters` must contain a dictionary where the key is the starting
delimiter, and the value is `(ending_delimiter, quoted_ending_delimiter)`.
If `escape_class` escapes `ending_delimiter` anyway, you may leave
`quoted_ending_delimiter` equal to `None`.

>>> gq = GenericQuote()
>>> gq.quote('"', 'a\nb')
'"a\\nb"'

The `unescape` method returns a tuple (start_quote, end_position, unquoted_string).
>>> gq.unquote('"a\\nb"')
('"', 6, 'a\nb')

Unmatched delimiters raise errors.
>>> gq.unquote('"abc')
Traceback (most recent call last):
(...)
generic_escape.NoEndingQuoteError

A less boring example:
>>> class LessBoringEscape(GenericEscape):
...   escaped = {"&":"&amp;", "<":"&lt;", ">":"&gt;"}
>>> gq.quoting_delimiters = {"<":(">",None)}
>>> gq.escape_class = LessBoringEscape
>>> gq.update()
>>> gq.quote("<", "a>b")
'<a&gt;b>'
>>> gq.unquote("<x&amp;>")
('<', 8, 'x&')
"""
    
    escape_class = GenericEscape
    quoting_delimiters = {"'":("'",r"\'"),
                          '"':('"',r"\"")}
    
    def __init__(self, *args, **kwargs):
        self.update()
        super().__init__(*args, **kwargs)
    
    def update(self):
        qds = self.quoting_delimiters
        escape_class = self.escape_class
        es = self._escaper_dict = {}
        ue_re = self._unquote_ending_re = {}
        for startq,(endq,endq_escaped) in qds.items():
            e = es[startq] = escape_class()
            e.escaped = e.escaped.copy()
            if endq_escaped is not None:
                e.escaped[endq] = endq_escaped
            e.update()
            ue_re[startq] = re.compile(re.escape(endq))
        self._unquote_re = re.compile(
            re_one_of(qds.keys()), re.DOTALL)
        
    def quote(self, start_quote, string):
        return ''.join((start_quote,
                        self._escaper_dict[start_quote].escape(string),
                        self.quoting_delimiters[start_quote][0]))
    
    def unquote(self, string, *, start_position=0):
        """returns (start_quote, end_position, unquoted_string)"""
        m = self._unquote_re.match(string, start_position)
        if not m:
            raise NoStartingQuoteError
        startq = m.group()
        i, r = self._escaper_dict[startq].unescape(string, start_position=m.end())
        m = self._unquote_ending_re[startq].match(string, i)
        if not m:
            raise NoEndingQuoteError
        return (startq, m.end(), r)

