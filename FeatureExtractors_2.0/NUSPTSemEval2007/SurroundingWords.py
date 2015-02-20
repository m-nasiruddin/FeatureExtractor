# -*- coding: utf-8 -*-
__author__ = 'Mohammad'


def __surrounding_words__(loc, winindex, wi, text):
    """This generates the surrounding words feature set with the (maximum number of words) surrounding words in a given
    context."""
    slist = text[loc.sentence]
    lexsn = text[loc.sentence][loc.word].lexsn
    outstr = ''
    if lexsn is not None and len(lexsn) > 0:
        curwindex = winindex.get(wi)
        for i in range(loc.word + curwindex[0] - 1, loc.word + curwindex[1] + 1):
            if i >= 0 and i < len(slist):
                if slist[i].lemma is not "":
                    outstr += '"' + slist[i].lemma.lower() + '"\t'
                else:
                    outstr += '"' + slist[i].word.lower() + '"\t'
            else:
                outstr += '"0"\t'
        if len(slist) > 1:
            outstr += "\n"
    return outstr