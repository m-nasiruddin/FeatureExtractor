# -*- coding: utf-8 -*-
__author__ = 'Mohammad'


def __local_collocation__(loc, text, mincolval, maxcolval):
    """Depending one the input argument, this generates the local collocation feature set with the surrounding
    words in a given context. Please see the NUSPTSemEval2007 system for more info."""
    slist = text[loc.sentence]
    lexsn = text[loc.sentence][loc.word].lexsn
    outstr = ''
    if lexsn is not None and len(lexsn) > 0:
        for i in range(0, len(mincolval)):
            outstr += '"'
            for cw in range(loc.word + mincolval[i], loc.word + maxcolval[i] + 1):
                if cw != loc.word:
                    if cw >= 0 and cw < len(slist):
                        if slist[cw].is_punc():
                            outstr += slist[cw].word
                        else:
                            if slist[cw].lemma is not "":
                                outstr += slist[cw].lemma.lower()
                            else:
                                outstr += slist[cw].word.lower()
                    else:
                        outstr += '∅'
                    if (cw < loc.word + maxcolval[i]):
                        outstr += "_"
            outstr += '"\t'
    return outstr