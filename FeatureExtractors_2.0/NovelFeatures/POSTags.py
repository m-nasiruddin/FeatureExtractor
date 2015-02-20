# -*- coding: utf-8 -*-
__author__ = 'Mohammad'


def __pos_tags__(loc, text, minposval, maxposval):
    """Depending one the input argument (surrounding word range), this generates the POS-tags feature set with the
    surrounding words in a given context. Please see the NUSPTSemEval2007 system for more info."""
    slist = text[loc.sentence]
    lexsn = text[loc.sentence][loc.word].lexsn
    outstr = ''
    if lexsn is not None and len(lexsn) > 0:
        for i in range(loc.word + minposval, loc.word + maxposval + 1):
            if i >= 0 and i < len(slist):
                if slist[i].is_punc():
                    outstr += '"' + "ε" + '"\t'
                else:
                    outstr += '"' + slist[i].pos + '"\t'
            else:
                outstr += '"ε"\t'
    return outstr