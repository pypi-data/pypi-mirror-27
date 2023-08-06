
from . import GenericEscape, GenericQuote
import unittest
import re

def get_indices_and_remove(haystack, needle, count):
    if count == 0: return []
    r = []
    l = haystack.split(needle, count)
    i = 0
    for s in l:
        i += len(s)
        r.append(i)
    r.pop()
    return (''.join(l), r)

class GenericEscapeTest(unittest.TestCase):
    def test_escape(self):
        def back_and_forth_check(instance, s):
            v = instance.unescape(instance.escape(s))[1]
            self.assertEqual(s,v)
        for escaped in [GenericEscape.escaped,
                        {'a':'aa'},
                        {'~' :'~tilde',     'b':'~bee',
                         '\\':'~backslash', 'Z':'~Z'}]:
            inst = GenericEscape()
            inst.escaped = escaped
            inst.unescape_whitelist = {'Z'}
            inst.update()
            for s in ["asdf","a'~bZ","a'\'Z~~b",'~b\\\'ZZ a','a~Z~\\n\nb']:
                back_and_forth_check(inst,s)
    def test_unescape(self):
        inst = GenericEscape()
        for original,expected_ue in [
                (         '@',''      ),
                (        'a@','a'     ),
                (   'abc@\nd','abc'   ),
                ('a\\n\\\\x@','a\n\\x'),
                (   'a@\\Xyz','a'     ),
                (   'abc@"yz','abc'   )]:
            original,(expected_endp,) = get_indices_and_remove(original,'@',1)
            endp, ue = inst.unescape(original)
            self.assertEqual(expected_endp, endp)
            self.assertEqual(expected_ue  , ue  )
    def test_unescape_split(self):
        class MyEscapeClass(GenericEscape):
            escaped = {'~':'~~','a':'~a','b':'~b'}
        inst = MyEscapeClass()
        R = re.compile
        for original,delim,maxsplit,expected_ues in [
                (          '@','a'        ,None,['']          ),
                (         'x@','a'        ,0   ,['x']         ),
                (         'x@','a'        ,99  ,['x']         ),
                (   'xxxayyy@','a'        ,None,['xxx','yyy'] ),
                (      'xaay@','a'        ,None,['x','','y']  ),
                (     'xanax@',R('[an]+') ,None,['x']*2       ),
                (     'xax@ba','a'        ,None,['x']*2       ),
                (     'x@axax','a'        ,0   ,['x']*1       ),
                (     'xax@ax','a'        ,1   ,['x']*2       ),
                (     'xaxax@','a'        ,None,['x']*3       ),
                (  'x~aax~aa@','a'        ,None,['xa','xa','']),
                ('xaxbnba~ax@',R('[abn]+'),None,['x','x','ax'])]:
            original,(expected_endp,) = get_indices_and_remove(original,'@',1)
            endp, ues = inst.unescape_split(original, delim, maxsplit=maxsplit)
            self.assertEqual(expected_endp, endp)
            self.assertEqual(expected_ues , ues )

class GenericQuoteTest(unittest.TestCase):
    def test_quote(self):
        class MyEscapeClass(GenericEscape):
            escaped = {'~':'~tilde',
                       'b':'~bee'}
        inst = GenericQuote()
        inst.quoting_delimiters = {'[[':(']]','~doubleleftbracket'),
                                   '[!':( '>','~leftanglebracket' ),
                                   'X' :( 'Y','~capitaly'         ),
                                   'Z' :( 'Z','~capitalz'         )}
        inst.escape_class = MyEscapeClass
        inst.update()
        for startq in inst.quoting_delimiters.keys():
            for s in ['[[!Xa~>]]~ [[~[',
                      '[<[[[!> aa XZ~',
                      '[[X>]]>aY~capitaly~~[[']:
                quoted = inst.quote(startq, s)
                self.assertEqual(s, inst.unquote(quoted)[2])
    def test_unescape(self):
        class MyEscapeClass(GenericEscape):
            escaped = {'~':'~tilde',
                       'b':'~bee',
                       '[':'~[', ']':'~]',
                       'Z':'~Z'}
            unescape_whitelist = {'Z'}
        inst = GenericQuote()
        inst.quoting_delimiters = {'['  :(']'  ,None ),
                                   'aaa':('aaa','~3a'),
                                   'a'  :('a'  ,'~a' )}
        inst.escape_class = MyEscapeClass
        inst.update()
        for original,expected_uq in [
                (                   '[@]@',''        ),
                (                  '[@x]@','x'       ),
                (          'aaa@x~beeaaa@','xb'      ),
                (         'a@~a~a~beea@aa','aab'     ),
                ('[@a~]Z~Z~tilde~beexZ]@]','a]ZZ~bxZ')]:
            original,(expected_sq_i,expected_endp,) = get_indices_and_remove(
                original,'@',2)
            expected_sq = original[:expected_sq_i]
            sq, endp, uq = inst.unquote(original)
            self.assertEqual(expected_sq  , sq  )
            self.assertEqual(expected_endp, endp)
            self.assertEqual(expected_uq  , uq  )

