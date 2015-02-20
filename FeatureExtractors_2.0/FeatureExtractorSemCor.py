# -*- coding: utf-8 -*-
__author__ = 'Mohammad'

import parsers.SemCor
import stopwords.StopwordsLoader
import NovelFeatures.ArgumentParser
import NovelFeatures.POSTags
import NovelFeatures.LocalCollocation
import NovelFeatures.SurroundingWords
import NovelFeatures.SurroundingWordsWithoutStopwords


class __Loc__:
    def __init__(self, sentence, word):
        self.sentence = sentence
        self.word = word


def __sense_generator__(loc, txt):
    "This function generates senses in a context."
    lexsn = txt[loc.sentence][loc.word].lexsn
    outstr = ''
    if lexsn is not None and len(lexsn) > 0:
        outstr += '"' + lexsn + '"\t'
    return outstr


def __feature_extractor__(semcor, dstdirectory, featurenames):
    """This function extracts features from SemCor."""
    argmnts = NovelFeatures.ArgumentParser.__argument_parser__(featurenames)
    mincolval = argmnts[1]
    maxcolval = argmnts[2]
    minposval = argmnts[3]
    maxposval = argmnts[4]

    values = semcor.split("</s>")
    cmd = ""
    rdf = ""
    lemma = ""
    pos = ""
    wnsn = ""
    lexsn = ""
    pn = ""
    ot = ""
    text = []
    windex = dict()
    winindex = dict()
    sentcnt = 0
    stoplist = stopwords.StopwordsLoader.__stopwords_loader__("stopwords/stopwords.txt");

    for s in values:
        s = s.strip()
        sentence = []
        if s.find("<s snum") > 0:
            lines = s.split('\n')
            wcnt = 0
            for line in lines:
                if line.startswith('<wf'):
                    line_split = line.replace('>', ' ').split()
                    for item in line_split:
                        if item.startswith("cmd"):
                            cmd = item[4:]
                        elif item.startswith("rdf"):
                            rdf = item[4:]
                        elif item.startswith("lemma"):
                            lemma = item[6:]
                        elif item.startswith("pos"):
                            pos = item[4:]
                        elif item.startswith("wnsn"):
                            wnsn = item[5:]
                        elif item.startswith("lexsn"):
                            lexsn = item[6:]
                        elif item.startswith("pn"):
                            pn = item[3:]
                        elif item.startswith("ot"):
                            ot = item[3:]
                        elif item.startswith("dc"):
                            None
                        elif item.startswith("sep"):
                            None
                        elif not item.startswith("<wf"):

                            word = item[:item.index("<")]
                            info = parsers.SemCor.InfoSemCor(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, word)
                            sentence.append(info)
                            wval = windex.get(lemma)
                            if wval is None:
                                wval = list()
                                windex[lemma] = wval
                            wval.append(__Loc__(sentcnt, wcnt))
                            cmd = ""
                            rdf = ""
                            pos = ""
                            lemma = ""
                            wnsn = ""
                            lexsn = ""
                            pn = ""
                            ot = ""
                            wcnt += 1
                elif line.startswith('<punc'):
                    line_split = line.replace('>', ' ').split()
                    for item in line_split:
                        if not item.startswith("<punc"):
                            word = item[:item.index("<")]
                            info = parsers.SemCor.InfoSemCor("", "", "", "", "", "", "", "", word)
                            sentence.append(info)
                            wcnt += 1
        sentcnt += 1
        text.append(sentence)

        for w in windex.keys():
            slist = windex.get(w)
            wmin = 0
            wmax = 0
            for loc in slist:
                slen = len(text[loc.sentence])
                lwmin = -(loc.word - 1)
                lwmax = slen - loc.word
                if (lwmin < wmin):
                    wmin = lwmin
                if (lwmax > wmax):
                    wmax = lwmax
            winindex[w] = [wmin, wmax]

    window_file = open("data/indexes/windows.csv", "w")
    for wi in windex.keys():
        if len(wi) > 0:
            outfile = open(dstdirectory + "/" + wi + ".csv", "w")
            outfile.write('"SENSE"')
            curnum = 1

            senselist = list()
            loccollist = list()
            postaglist = list()
            swordlist = list()
            locs = list()
            for loc in windex.get(wi):
                senselist.append(__sense_generator__(loc, text))
                loccollist.append(NovelFeatures.LocalCollocation.__local_collocation__(loc, text, mincolval, maxcolval))
                postaglist.append(NovelFeatures.POSTags.__pos_tags__(loc, text, minposval, maxposval))
                swordlist.append(NovelFeatures.SurroundingWords.__surrounding_words__(loc, winindex, wi, text))
                locs.append(loc.word)
            window_file.write(wi)
            newswordlist = NovelFeatures.SurroundingWordsWithoutStopwords.__surrounding_words_without_stopwords__(locs,
                                                                                                                  stoplist,
                                                                                                                  swordlist,
                                                                                                                  window_file)
            window_file.flush()

            ncols = -1
            for i in range(0, len(senselist)):
                outstr = senselist[i]
                outstr += loccollist[i]
                outstr += postaglist[i]
                outstr += newswordlist[i]
                if ncols == -1:
                    ncols = len(outstr.split("\t")) - 1
                    for i in range(1, ncols):
                        outfile.write('\t"A' + str(curnum) + '"')
                        curnum += 1
                    outfile.write('\n')
                outfile.write(outstr)
                outfile.flush()
            outfile.close()
    window_file.close()
    print("Successfully finished!")