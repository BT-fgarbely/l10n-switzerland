# -*- coding: utf-8 -*-

"""Convert many unicode characters to ascii characters that are like them.

I want to collate names, with the property that a last name starting with
O-umlaut will be in with the last name's starting with O.    Horrors!

So I want that many Latin-1 characters have their umlaute's, etc., stripped.
Some of it can be done automatically but some needs to be done by hand, that
I can tell.
"""
import sys
import unicodedata

__version__ = '1.0.1'
__author__ = 'Jim Hefferon: ftpmaint at tug.ctan.org'
__date__ = '2008-July-15'
__notes__ = """As sources, used effbot's web site, and
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/251871
and man uni2ascii
"""

# These characters that are not done automatically by NFKD, and
# have a name starting with "LATIN".    Some of these I found on the interwebs,
# but some I did by eye.    Corrections or additions appreciated.
EXTRA_LATIN_NAMES = {
    # First are ones I got off the interweb
    u"\N{LATIN CAPITAL LETTER O WITH STROKE}": u"O",
    u"\N{LATIN SMALL LETTER A WITH GRAVE}": u"a",
    u"\N{LATIN SMALL LETTER A WITH ACUTE}": u"a",
    u"\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}": u"a",
    u"\N{LATIN SMALL LETTER A WITH TILDE}": u"a",
    u"\N{LATIN SMALL LETTER A WITH DIAERESIS}": u"ae",
    u"\N{LATIN SMALL LETTER A WITH RING ABOVE}": u"a",
    u"\N{LATIN SMALL LETTER C WITH CEDILLA}": u"c",
    u"\N{LATIN SMALL LETTER E WITH GRAVE}": u"e",
    u"\N{LATIN SMALL LETTER E WITH ACUTE}": u"e",
    u"\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}": u"e",
    u"\N{LATIN SMALL LETTER E WITH DIAERESIS}": u"e",
    u"\N{LATIN SMALL LETTER I WITH GRAVE}": u"i",
    u"\N{LATIN SMALL LETTER I WITH ACUTE}": u"i",
    u"\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}": u"i",
    u"\N{LATIN SMALL LETTER I WITH DIAERESIS}": u"i",
    u"\N{LATIN SMALL LETTER N WITH TILDE}": u"n",
    u"\N{LATIN SMALL LETTER O WITH GRAVE}": u"o",
    u"\N{LATIN SMALL LETTER O WITH ACUTE}": u"o",
    u"\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}": u"o",
    u"\N{LATIN SMALL LETTER O WITH TILDE}": u"o",
    u"\N{LATIN SMALL LETTER O WITH DIAERESIS}": u"oe",
    u"\N{LATIN SMALL LETTER U WITH GRAVE}": u"u",
    u"\N{LATIN SMALL LETTER U WITH ACUTE}": u"u",
    u"\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}": u"u",
    u"\N{LATIN SMALL LETTER U WITH DIAERESIS}": u"ue",
    u"\N{LATIN SMALL LETTER Y WITH ACUTE}": u"y",
    u"\N{LATIN SMALL LETTER Y WITH DIAERESIS}": u"y",
    u"\N{LATIN SMALL LETTER A WITH MACRON}": u"a",
    u"\N{LATIN SMALL LETTER A WITH BREVE}": u"a",
    u"\N{LATIN SMALL LETTER C WITH ACUTE}": u"c",
    u"\N{LATIN SMALL LETTER C WITH CIRCUMFLEX}": u"c",
    u"\N{LATIN SMALL LETTER E WITH MACRON}": u"e",
    u"\N{LATIN SMALL LETTER E WITH BREVE}": u"e",
    u"\N{LATIN SMALL LETTER G WITH CIRCUMFLEX}": u"g",
    u"\N{LATIN SMALL LETTER G WITH BREVE}": u"g",
    u"\N{LATIN SMALL LETTER G WITH CEDILLA}": u"g",
    u"\N{LATIN SMALL LETTER H WITH CIRCUMFLEX}": u"h",
    u"\N{LATIN SMALL LETTER I WITH TILDE}": u"i",
    u"\N{LATIN SMALL LETTER I WITH MACRON}": u"i",
    u"\N{LATIN SMALL LETTER I WITH BREVE}": u"i",
    u"\N{LATIN SMALL LETTER J WITH CIRCUMFLEX}": u"j",
    u"\N{LATIN SMALL LETTER K WITH CEDILLA}": u"k",
    u"\N{LATIN SMALL LETTER L WITH ACUTE}": u"l",
    u"\N{LATIN SMALL LETTER L WITH CEDILLA}": u"l",
    u"\N{LATIN CAPITAL LETTER L WITH STROKE}": u"L",
    u"\N{LATIN SMALL LETTER L WITH STROKE}": u"l",
    u"\N{LATIN SMALL LETTER N WITH ACUTE}": u"n",
    u"\N{LATIN SMALL LETTER N WITH CEDILLA}": u"n",
    u"\N{LATIN SMALL LETTER O WITH MACRON}": u"o",
    u"\N{LATIN SMALL LETTER O WITH BREVE}": u"o",
    u"\N{LATIN SMALL LETTER R WITH ACUTE}": u"r",
    u"\N{LATIN SMALL LETTER R WITH CEDILLA}": u"r",
    u"\N{LATIN SMALL LETTER S WITH ACUTE}": u"s",
    u"\N{LATIN SMALL LETTER S WITH CIRCUMFLEX}": u"s",
    u"\N{LATIN SMALL LETTER S WITH CEDILLA}": u"s",
    u"\N{LATIN SMALL LETTER T WITH CEDILLA}": u"t",
    u"\N{LATIN SMALL LETTER U WITH TILDE}": u"u",
    u"\N{LATIN SMALL LETTER U WITH MACRON}": u"u",
    u"\N{LATIN SMALL LETTER U WITH BREVE}": u"u",
    u"\N{LATIN SMALL LETTER U WITH RING ABOVE}": u"u",
    u"\N{LATIN SMALL LETTER W WITH CIRCUMFLEX}": u"w",
    u"\N{LATIN SMALL LETTER Y WITH CIRCUMFLEX}": u"y",
    u"\N{LATIN SMALL LETTER Z WITH ACUTE}": u"z",
    u"\N{LATIN SMALL LETTER W WITH GRAVE}": u"w",
    u"\N{LATIN SMALL LETTER W WITH ACUTE}": u"w",
    u"\N{LATIN SMALL LETTER W WITH DIAERESIS}": u"w",
    u"\N{LATIN SMALL LETTER Y WITH GRAVE}": u"y",
    # Below are the ones that failed automated conversion
    u'\N{LATIN CAPITAL LETTER AE}': u'AE',
    u'\N{LATIN CAPITAL LETTER ETH}': u'D',
    u"\N{LATIN CAPITAL LETTER A WITH DIAERESIS}": u"Ae",
    u"\N{LATIN CAPITAL LETTER O WITH DIAERESIS}": u"Oe",
    u"\N{LATIN CAPITAL LETTER U WITH DIAERESIS}": u"Ue",
    u'\N{LATIN CAPITAL LETTER THORN}': u'TH',
    u'\N{LATIN SMALL LETTER SHARP S}': u'ss',
    u'\N{LATIN SMALL LETTER AE}': u'ae',
    u'\N{LATIN SMALL LETTER ETH}': u'd',
    u'\N{LATIN SMALL LETTER THORN}': 'th',
    u'\N{LATIN CAPITAL LETTER D WITH STROKE}': u'D',
    u'\N{LATIN SMALL LETTER D WITH STROKE}': u'd',
    u'\N{LATIN CAPITAL LETTER H WITH STROKE}': u'H',
    u'\N{LATIN SMALL LETTER H WITH STROKE}': u'h',
    u'\N{LATIN SMALL LETTER DOTLESS I}': u'i',
    u'\N{LATIN SMALL LETTER KRA}': u'q',
    u'\N{LATIN CAPITAL LETTER ENG}': u'N',
    u'\N{LATIN SMALL LETTER ENG}': u'n',
    u'\N{LATIN CAPITAL LIGATURE OE}': u'OE',
    u'\N{LATIN SMALL LIGATURE OE}': u'oe',
    u'\N{LATIN CAPITAL LETTER T WITH STROKE}': u'T',
    u'\N{LATIN SMALL LETTER T WITH STROKE}': u't',
    u'\N{LATIN SMALL LETTER B WITH STROKE}': u'b',
    u'\N{LATIN CAPITAL LETTER B WITH HOOK}': u'B',
    u'\N{LATIN CAPITAL LETTER B WITH TOPBAR}': u'B',
    u'\N{LATIN SMALL LETTER B WITH TOPBAR}': u'b',
    u'\N{LATIN CAPITAL LETTER OPEN O}': u'O',
    u'\N{LATIN CAPITAL LETTER C WITH HOOK}': u'C',
    u'\N{LATIN SMALL LETTER C WITH HOOK}': u'c',
    u'\N{LATIN CAPITAL LETTER AFRICAN D}': u'D',
    u'\N{LATIN CAPITAL LETTER D WITH HOOK}': u'D',
    u'\N{LATIN CAPITAL LETTER D WITH TOPBAR}': u'D',
    u'\N{LATIN SMALL LETTER D WITH TOPBAR}': u'd',
    u'\N{LATIN CAPITAL LETTER REVERSED E}': u'E',
    u'\N{LATIN CAPITAL LETTER OPEN E}': u'E',
    u'\N{LATIN CAPITAL LETTER F WITH HOOK}': u'F',
    u'\N{LATIN SMALL LETTER F WITH HOOK}': u'f',
    u'\N{LATIN CAPITAL LETTER G WITH HOOK}': u'G',
    u'\N{LATIN SMALL LETTER HV}': u'hv',
    u'\N{LATIN CAPITAL LETTER IOTA}': u'i',
    u'\N{LATIN CAPITAL LETTER I WITH STROKE}': u'I',
    u'\N{LATIN CAPITAL LETTER K WITH HOOK}': u'K',
    u'\N{LATIN SMALL LETTER K WITH HOOK}': u'k',
    u'\N{LATIN SMALL LETTER L WITH BAR}': u'l',
    u'\N{LATIN CAPITAL LETTER N WITH LEFT HOOK}': u'N',
    u'\N{LATIN SMALL LETTER N WITH LONG RIGHT LEG}': u'N',
    u'\N{LATIN CAPITAL LETTER O WITH MIDDLE TILDE}': u'O',
    u'\N{LATIN CAPITAL LETTER OI}': u'OI',
    u'\N{LATIN SMALL LETTER OI}': u'oi',
    u'\N{LATIN CAPITAL LETTER P WITH HOOK}': u'P',
    u'\N{LATIN SMALL LETTER P WITH HOOK}': u'p',
    u'\N{LATIN CAPITAL LETTER ESH}': u'SH',
    u'\N{LATIN SMALL LETTER T WITH PALATAL HOOK}': u't',
    u'\N{LATIN CAPITAL LETTER T WITH HOOK}': u'T',
    u'\N{LATIN SMALL LETTER T WITH HOOK}': u't',
    u'\N{LATIN CAPITAL LETTER T WITH RETROFLEX HOOK}': u'T',
    u'\N{LATIN CAPITAL LETTER V WITH HOOK}': u'V',
    u'\N{LATIN CAPITAL LETTER Y WITH HOOK}': u'Y',
    u'\N{LATIN SMALL LETTER Y WITH HOOK}': u'y',
    u'\N{LATIN CAPITAL LETTER Z WITH STROKE}': u'Z',
    u'\N{LATIN SMALL LETTER Z WITH STROKE}': u'z',
    u'\N{LATIN CAPITAL LETTER EZH}': u'S',
    u'\N{LATIN SMALL LETTER EZH WITH TAIL}': u's',
    u'\N{LATIN LETTER WYNN}': u'w',
    u'\N{LATIN CAPITAL LETTER AE WITH MACRON}': u'AE',
    u'\N{LATIN SMALL LETTER AE WITH MACRON}': u'ae',
    u'\N{LATIN CAPITAL LETTER G WITH STROKE}': u'G',
    u'\N{LATIN SMALL LETTER G WITH STROKE}': u'g',
    u'\N{LATIN CAPITAL LETTER EZH WITH CARON}': u'S',
    u'\N{LATIN SMALL LETTER EZH WITH CARON}': u's',
    u'\N{LATIN CAPITAL LETTER HWAIR}': u'HW',
    u'\N{LATIN CAPITAL LETTER WYNN}': u'W',
    u'\N{LATIN CAPITAL LETTER AE WITH ACUTE}': u'AE',
    u'\N{LATIN SMALL LETTER AE WITH ACUTE}': u'AE',
    u'\N{LATIN SMALL LETTER O WITH STROKE AND ACUTE}': u'o',
    u'\N{LATIN CAPITAL LETTER YOGH}': u'J',
    u'\N{LATIN SMALL LETTER YOGH}': u'j',
    u'\N{LATIN CAPITAL LETTER N WITH LONG RIGHT LEG}': u'N',
    u'\N{LATIN SMALL LETTER D WITH CURL}': u'd',
    u'\N{LATIN CAPITAL LETTER OU}': u'OU',
    u'\N{LATIN SMALL LETTER OU}': u'ou',
    u'\N{LATIN CAPITAL LETTER Z WITH HOOK}': u'Z',
    u'\N{LATIN SMALL LETTER Z WITH HOOK}': u'z',
    u'\N{LATIN SMALL LETTER L WITH CURL}': u'l',
    u'\N{LATIN SMALL LETTER N WITH CURL}': u'n',
    u'\N{LATIN SMALL LETTER T WITH CURL}': u't',
    u'\N{LATIN SMALL LETTER DOTLESS J}': u'j',
    u'\N{LATIN SMALL LETTER DB DIGRAPH}': u'db',
    u'\N{LATIN SMALL LETTER QP DIGRAPH}': u'qp',
    u'\N{LATIN CAPITAL LETTER A WITH STROKE}': u'A',
    u'\N{LATIN CAPITAL LETTER C WITH STROKE}': u'C',
    u'\N{LATIN SMALL LETTER C WITH STROKE}': u'C',
    u'\N{LATIN CAPITAL LETTER L WITH BAR}': u'L',
    u'\N{LATIN CAPITAL LETTER T WITH DIAGONAL STROKE}': u'T',
    u'\N{LATIN SMALL LETTER S WITH SWASH TAIL}': u'S',
    u'\N{LATIN SMALL LETTER Z WITH SWASH TAIL}': u'Z',
    u'\N{LATIN SMALL LETTER B WITH HOOK}': u'b',
    u'\N{LATIN SMALL LETTER OPEN O}': u'o',
    u'\N{LATIN SMALL LETTER C WITH CURL}': u'c',
    u'\N{LATIN SMALL LETTER D WITH TAIL}': u'd',
    u'\N{LATIN SMALL LETTER D WITH HOOK}': u'd',
    u'\N{LATIN SMALL LETTER OPEN E}': u'e',
    u'\N{LATIN SMALL LETTER DOTLESS J WITH STROKE}': u'j',
    u'\N{LATIN SMALL LETTER G WITH HOOK}': u'g',
    u'\N{LATIN SMALL LETTER SCRIPT G}': u'g',
    u'\N{LATIN LETTER SMALL CAPITAL G}': u'G',
    u'\N{LATIN SMALL LETTER H WITH HOOK}': u'h',
    u'\N{LATIN SMALL LETTER HENG WITH HOOK}': u'h',
    u'\N{LATIN SMALL LETTER I WITH STROKE}': u'i',
    u'\N{LATIN LETTER SMALL CAPITAL I}': u'I',
    u'\N{LATIN SMALL LETTER L WITH MIDDLE TILDE}': u'L',
    u'\N{LATIN SMALL LETTER L WITH BELT}': u'L',
    u'\N{LATIN SMALL LETTER L WITH RETROFLEX HOOK}': u'L',
    u'\N{LATIN SMALL LETTER M WITH HOOK}': u'm',
    u'\N{LATIN SMALL LETTER N WITH LEFT HOOK}': u'n',
    u'\N{LATIN SMALL LETTER N WITH RETROFLEX HOOK}': u'n',
    u'\N{LATIN LETTER SMALL CAPITAL N}': u'N',
    u'\N{LATIN SMALL LETTER BARRED O}': u'o',
    u'\N{LATIN LETTER SMALL CAPITAL OE}': u'OE',
    u'\N{LATIN SMALL LETTER R WITH LONG LEG}': u'r',
    u'\N{LATIN SMALL LETTER R WITH TAIL}': u'r',
    u'\N{LATIN SMALL LETTER R WITH FISHHOOK}': u'r',
    u'\N{LATIN LETTER SMALL CAPITAL R}': u'R',
    u'\N{LATIN SMALL LETTER S WITH HOOK}': u's',
    u'\N{LATIN SMALL LETTER ESH}': u'sh',
    u'\N{LATIN SMALL LETTER DOTLESS J WITH STROKE AND HOOK}': u'j',
    u'\N{LATIN SMALL LETTER ESH WITH CURL}': u'sh',
    u'\N{LATIN SMALL LETTER T WITH RETROFLEX HOOK}': u't',
    u'\N{LATIN SMALL LETTER U BAR}': u'u',
    u'\N{LATIN SMALL LETTER V WITH HOOK}': u'v',
    u'\N{LATIN LETTER SMALL CAPITAL Y}': u'Y',
    u'\N{LATIN SMALL LETTER Z WITH RETROFLEX HOOK}': u'z',
    u'\N{LATIN SMALL LETTER Z WITH CURL}': u'z',
    u'\N{LATIN SMALL LETTER EZH}': u's',
    u'\N{LATIN SMALL LETTER EZH WITH CURL}': u's',
    u'\N{LATIN LETTER STRETCHED C}': u'c',
    u'\N{LATIN LETTER SMALL CAPITAL B}': u'B',
    u'\N{LATIN SMALL LETTER CLOSED OPEN E}': u'e',
    u'\N{LATIN LETTER SMALL CAPITAL G WITH HOOK}': u'G',
    u'\N{LATIN LETTER SMALL CAPITAL H}': u'H',
    u'\N{LATIN SMALL LETTER J WITH CROSSED-TAIL}': u'j',
    u'\N{LATIN LETTER SMALL CAPITAL L}': u'L',
    u'\N{LATIN SMALL LETTER Q WITH HOOK}': u'q',
    u'\N{LATIN LETTER SMALL CAPITAL A}': u'A',
    u'\N{LATIN LETTER SMALL CAPITAL AE}': u'AE',
    u'\N{LATIN LETTER SMALL CAPITAL BARRED B}': u'B',
    u'\N{LATIN LETTER SMALL CAPITAL C}': u'C',
    u'\N{LATIN LETTER SMALL CAPITAL D}': u'D',
    u'\N{LATIN LETTER SMALL CAPITAL ETH}': u'D',
    u'\N{LATIN LETTER SMALL CAPITAL E}': u'E',
    u'\N{LATIN LETTER SMALL CAPITAL J}': u'J',
    u'\N{LATIN LETTER SMALL CAPITAL K}': u'K',
    u'\N{LATIN LETTER SMALL CAPITAL L WITH STROKE}': u'L',
    u'\N{LATIN LETTER SMALL CAPITAL M}': u'M',
    # u'\N{LATIN LETTER SMALL CAPITAL REVERSED N}': u'',
    u'\N{LATIN LETTER SMALL CAPITAL O}': u'O',
    u'\N{LATIN LETTER SMALL CAPITAL OPEN O}': u'O',
    u'\N{LATIN LETTER SMALL CAPITAL OU}': u'OU',
    # u'\N{LATIN SMALL LETTER TOP HALF O}': u'',
    # u'\N{LATIN SMALL LETTER BOTTOM HALF O}': u'',
    u'\N{LATIN LETTER SMALL CAPITAL P}': u'P',
    # u'\N{LATIN LETTER SMALL CAPITAL REVERSED R}': u'',
    # u'\N{LATIN LETTER SMALL CAPITAL TURNED R}': u'',
    u'\N{LATIN LETTER SMALL CAPITAL T}': u'T',
    u'\N{LATIN LETTER SMALL CAPITAL U}': u'U',
    # u'\N{LATIN SMALL LETTER SIDEWAYS U}': u'',
    # u'\N{LATIN SMALL LETTER SIDEWAYS DIAERESIZED U}': u'',
    # u'\N{LATIN SMALL LETTER SIDEWAYS TURNED M}': u'',
    u'\N{LATIN LETTER SMALL CAPITAL V}': u'V',
    u'\N{LATIN LETTER SMALL CAPITAL W}': u'W',
    u'\N{LATIN LETTER SMALL CAPITAL Z}': u'',
    u'\N{LATIN LETTER SMALL CAPITAL EZH}': u'S',
    # u'\N{LATIN LETTER VOICED LARYNGEAL SPIRANT}': u'',
    # u'\N{LATIN LETTER AIN}': u'',
    u'\N{LATIN SMALL LETTER UE}': u'ue',
    u'\N{LATIN SMALL LETTER B WITH MIDDLE TILDE}': u'b',
    u'\N{LATIN SMALL LETTER D WITH MIDDLE TILDE}': u'd',
    u'\N{LATIN SMALL LETTER F WITH MIDDLE TILDE}': u'f',
    u'\N{LATIN SMALL LETTER M WITH MIDDLE TILDE}': u'm',
    u'\N{LATIN SMALL LETTER N WITH MIDDLE TILDE}': u'n',
    u'\N{LATIN SMALL LETTER P WITH MIDDLE TILDE}': u'p',
    u'\N{LATIN SMALL LETTER R WITH MIDDLE TILDE}': u'r',
    u'\N{LATIN SMALL LETTER R WITH FISHHOOK AND MIDDLE TILDE}': u'r',
    u'\N{LATIN SMALL LETTER S WITH MIDDLE TILDE}': u's',
    u'\N{LATIN SMALL LETTER T WITH MIDDLE TILDE}': u't',
    u'\N{LATIN SMALL LETTER Z WITH MIDDLE TILDE}': u'z',
    # u'\N{LATIN SMALL LETTER TURNED G}': u'',
    # u'\N{LATIN SMALL LETTER INSULAR G}': u'',
    u'\N{LATIN SMALL LETTER TH WITH STRIKETHROUGH}': u'th',
    u'\N{LATIN SMALL CAPITAL LETTER I WITH STROKE}': u'I',
    # u'\N{LATIN SMALL LETTER IOTA WITH STROKE}': u'',
    u'\N{LATIN SMALL LETTER P WITH STROKE}': u'p',
    u'\N{LATIN SMALL CAPITAL LETTER U WITH STROKE}': u'U',
    # u'\N{LATIN SMALL LETTER UPSILON WITH STROKE}': u'',
    u'\N{LATIN SMALL LETTER B WITH PALATAL HOOK}': u'b',
    u'\N{LATIN SMALL LETTER D WITH PALATAL HOOK}': u'd',
    u'\N{LATIN SMALL LETTER F WITH PALATAL HOOK}': u'f',
    u'\N{LATIN SMALL LETTER G WITH PALATAL HOOK}': u'g',
    u'\N{LATIN SMALL LETTER K WITH PALATAL HOOK}': u'k',
    u'\N{LATIN SMALL LETTER L WITH PALATAL HOOK}': u'l',
    u'\N{LATIN SMALL LETTER M WITH PALATAL HOOK}': u'm',
    u'\N{LATIN SMALL LETTER N WITH PALATAL HOOK}': u'n',
    u'\N{LATIN SMALL LETTER P WITH PALATAL HOOK}': u'p',
    u'\N{LATIN SMALL LETTER R WITH PALATAL HOOK}': u'r',
    u'\N{LATIN SMALL LETTER S WITH PALATAL HOOK}': u's',
    u'\N{LATIN SMALL LETTER ESH WITH PALATAL HOOK}': u'sh',
    u'\N{LATIN SMALL LETTER V WITH PALATAL HOOK}': u'v',
    u'\N{LATIN SMALL LETTER X WITH PALATAL HOOK}': u'x',
    u'\N{LATIN SMALL LETTER Z WITH PALATAL HOOK}': u'z',
    u'\N{LATIN SMALL LETTER A WITH RETROFLEX HOOK}': u'a',
    # u'\N{LATIN SMALL LETTER ALPHA WITH RETROFLEX HOOK}': u'',
    u'\N{LATIN SMALL LETTER D WITH HOOK AND TAIL}': u'd',
    u'\N{LATIN SMALL LETTER E WITH RETROFLEX HOOK}': u'e',
    u'\N{LATIN SMALL LETTER OPEN E WITH RETROFLEX HOOK}': u'e',
    u'\N{LATIN SMALL LETTER REVERSED OPEN E WITH RETROFLEX HOOK}': u'e',
    # u'\N{LATIN SMALL LETTER SCHWA WITH RETROFLEX HOOK}': u'',
    u'\N{LATIN SMALL LETTER I WITH RETROFLEX HOOK}': u'i',
    u'\N{LATIN SMALL LETTER OPEN O WITH RETROFLEX HOOK}': u'o',
    u'\N{LATIN SMALL LETTER ESH WITH RETROFLEX HOOK}': u'sh',
    u'\N{LATIN SMALL LETTER U WITH RETROFLEX HOOK}': u'u',
    u'\N{LATIN SMALL LETTER EZH WITH RETROFLEX HOOK}': u's',
    # u'\N{LATIN SUBSCRIPT SMALL LETTER SCHWA}': u'',
    # u'\N{LATIN CROSS}': u''
}

# Additional ones; see "man uni2ascii"
UNI2ASCII_CONVERSIONS = {
    u'\N{NO-BREAK SPACE}': u' ',
    u'\N{LEFT-POINTING DOUBLE ANGLE QUOTATION MARK}': u'"',
    u'\N{SOFT HYPHEN}': u'',
    u'\N{RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK}': u'"',
    u'\N{ETHIOPIC WORDSPACE}': u' ',
    u'\N{OGHAM SPACE MARK}': u' ',
    u'\N{EN QUAD}': u' ',
    u'\N{EM QUAD}': u' ',
    u'\N{EN SPACE}': u' ',
    u'\N{EM SPACE}': u' ',
    u'\N{THREE-PER-EM SPACE}': u' ',
    u'\N{FOUR-PER-EM SPACE}': u' ',
    u'\N{SIX-PER-EM SPACE}': u' ',
    u'\N{FIGURE SPACE}': u' ',
    u'\N{PUNCTUATION SPACE}': u' ',
    u'\N{THIN SPACE}': u' ',
    u'\N{HAIR SPACE}': u' ',
    u'\N{ZERO WIDTH SPACE}': u' ',
    u'\N{ZERO WIDTH NO-BREAK SPACE}': u' ',
    u'\N{HYPHEN}': u'-',
    u'\N{NON-BREAKING HYPHEN}': u'-',
    u'\N{FIGURE DASH}': u'-',
    u'\N{EN DASH}': u'-',
    u'\N{EM DASH}': u'-',
    u'\N{LEFT SINGLE QUOTATION MARK}': u'`',
    u'\N{RIGHT SINGLE QUOTATION MARK}': u"'",
    u'\N{SINGLE LOW-9 QUOTATION MARK}': u'`',
    u'\N{SINGLE HIGH-REVERSED-9 QUOTATION MARK}': u'`',
    u'\N{LEFT DOUBLE QUOTATION MARK}': u'"',
    u'\N{RIGHT DOUBLE QUOTATION MARK}': u'"',
    u'\N{DOUBLE LOW-9 QUOTATION MARK}': u'"',
    u'\N{DOUBLE HIGH-REVERSED-9 QUOTATION MARK}': u'"',
    u'\N{SINGLE LEFT-POINTING ANGLE QUOTATION MARK}': u'`',
    u'\N{SINGLE RIGHT-POINTING ANGLE QUOTATION MARK}': u"'",
    u'\N{LOW ASTERISK}': u'*',
    u'\N{MINUS SIGN}': u'-',
    u'\N{ASTERISK OPERATOR}': u'*',
    u'\N{BOX DRAWINGS LIGHT HORIZONTAL}': u'-',
    u'\N{BOX DRAWINGS HEAVY HORIZONTAL}': u'-',
    u'\N{BOX DRAWINGS LIGHT VERTICAL}': u'|',
    u'\N{BOX DRAWINGS HEAVY VERTICAL}': u'|',
    u'\N{HEAVY ASTERISK}': u'*',
    u'\N{HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT}': u'"',
    u'\N{HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT}': u'"',
    u'\N{IDEOGRAPHIC SPACE}': u' ',
    u'\N{SMALL AMPERSAND}': u'&',
    u'\N{SMALL ASTERISK}': u'*',
    u'\N{SMALL PLUS SIGN}': u'+',
    u'\N{CENT SIGN}': u'cent',
    u'\N{POUND SIGN}': u'pound',
    u'\N{YEN SIGN}': u'yen',
    u'\N{COPYRIGHT SIGN}': u'(c)',
    u'\N{REGISTERED SIGN}': u'(R)',
    u'\N{VULGAR FRACTION ONE QUARTER}': u'1/4',
    u'\N{VULGAR FRACTION ONE HALF}': u'1/2',
    u'\N{VULGAR FRACTION THREE QUARTERS}': u'3/4',
    u'\N{LATIN SMALL LETTER SHARP S}': u'ss',
    u'\N{LATIN CAPITAL LIGATURE IJ}': u'IJ',
    u'\N{LATIN SMALL LIGATURE IJ}': u'ij',
    u'\N{LATIN CAPITAL LIGATURE OE}': u'OE',
    u'\N{LATIN SMALL LIGATURE oe}': u'oe',
    u'\N{LATIN CAPITAL LETTER DZ}': u'DZ',
    u'\N{LATIN CAPITAL LETTER DZ WITH CARON}': u'DZ',
    u'\N{LATIN CAPITAL LETTER D WITH SMALL LETTER Z}': u'Dz',
    u'\N{LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON}': u'Dz',
    u'\N{LATIN SMALL LETTER DZ}': u'dz',
    u'\N{LATIN SMALL LETTER TS DIGRAPH}': u'ts',
    u'\N{HORIZONTAL ELLIPSIS}': u'...',
    u'\N{MIDLINE HORIZONTAL ELLIPSIS}': u'...',
    u'\N{LEFTWARDS ARROW}': u'<-',
    u'\N{RIGHTWARDS ARROW}': u'->',
    u'\N{LEFTWARDS DOUBLE ARROW}': u'<=',
    u'\N{RIGHTWARDS DOUBLE ARROW}': u'=>',
}

# More from "man uni2ascii", in a different category.
EXTRA_CHARACTERS = {
    u'\N{ACUTE ACCENT}': u"'",
    u'\N{BROKEN BAR}': u'|',
    u'\N{CENT SIGN}': u' cents ',
    u'\N{COPYRIGHT SIGN}': u'(C)',
    u'\N{CURRENCY SIGN}': u' currency ',
    u'\N{DEGREE SIGN}': u' degrees ',
    u'\N{DIVISION SIGN}': u'/',
    u'\N{INVERTED EXCLAMATION MARK}': u'!',
    u'\N{INVERTED QUESTION MARK}': u'?',
    u'\N{MACRON}': u'_',
    u'\N{MICRO SIGN}': u'micro',
    u'\N{MIDDLE DOT}': u'*',
    u'\N{MULTIPLICATION SIGN}': u'*',
    u'\N{NOT SIGN}': u'not',
    u'\N{PILCROW SIGN}': u'paragraph',
    u'\N{PLUS-MINUS SIGN}': u'+/-',
    u'\N{POUND SIGN}': u'pound',
    u'\N{REGISTERED SIGN}': u'(R)',
    u'\N{SECTION SIGN}': u'section',
    u'\N{SOFT HYPHEN}': u'',
    u'\N{SUPERSCRIPT ONE}': u'^1',
    u'\N{SUPERSCRIPT THREE}': u'^3',
    u'\N{SUPERSCRIPT TWO}': u'^2',
    u'\N{VULGAR FRACTION ONE HALF}': u'1/2',
    u'\N{VULGAR FRACTION ONE QUARTER}': u'1/4',
    u'\N{VULGAR FRACTION THREE QUARTERS}': u'3/4',
    u'\N{YEN SIGN}': u'yen'
}
FG_HACKS = {
    u'\u0082': u'',  # "break permitted here" symbol
    u'\u2022': u'*',  # Bullet
}


def build_dictionary():
    'Return the translation dictionary.'
    d = dict()
    # First do what can be done automatically
    for i in range(0xffff):
        u = unichr(i)
        try:
            n = unicodedata.name(u)
            if n.startswith('LATIN '):
                k = unicodedata.normalize('NFKD', u).encode('ASCII', 'ignore')
                if k:
                    d[i] = unicode(k)  # i=ord(u)
        except ValueError:
            pass
    # Next, add some by-hand ones (overlap possible, so order matters)
    for m in [EXTRA_LATIN_NAMES, EXTRA_CHARACTERS,
              UNI2ASCII_CONVERSIONS, FG_HACKS]:
        for i in m:
            try:
                d[ord(i)] = unicode(m[i])
            except Exception:
                pass
    return d

udict = build_dictionary()


def convert(string):
    return string.translate(udict)


def coroutine(func):
    def start(*argz, **kwz):
        cr = func(*argz, **kwz)
        cr.next()
        return cr
    return start


@coroutine
def co_filter(drain, in_enc='utf-8', out_enc='ascii'):
    bs = None
    while True:
        chunk = (yield bs)
        bs = drain(convert(unicode(chunk)).encode('utf-8'))


def uc_filter(sin, sout, bs=8192, in_enc='utf-8', out_enc='ascii'):
    sout = co_filter(sout.write, in_enc, out_enc)
    while True:
        dta = sin.read(bs)
        if not dta:
            break
        else:
            sout.send(dta)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(
        usage='%prog [options]',
        description='utf8 stdin -> ascii stdout'
    )
    parser.add_option(
        '-s',
        '--src-enc',
        action='store',
        type='str',
        dest='src_enc',
        metavar='ENC',
        default='utf-8',
        help='source encoding (utf-8)'
    )
    parser.add_option(
        '-d',
        '--dst-enc',
        action='store',
        type='str',
        dest='dst_enc',
        metavar='ENC',
        default='ascii',
        help='destination encoding (ascii)'
    )
    parser.add_option(
        '-c',
        '--chunk',
        action='store',
        type='int',
        dest='bs',
        metavar='BYTES',
        default=8192,
        help='read/write in chunks of a given size (8192)'
    )
    optz, arguments = parser.parse_args()
    if arguments:
        parser.error('Only stdin -> stdout conversion suported')

    uc_filter(sys.stdin, sys.stdout, bs=optz.bs,
              in_enc=optz.src_enc, out_enc=optz.dst_enc)
