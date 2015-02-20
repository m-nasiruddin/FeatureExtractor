__author__ = 'Mohammad'


class InfoSemcor:
    def __init__(self, cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, word):
        self.cmd = cmd
        self.rdf = rdf
        self.pos = pos
        self.lemma = lemma
        self.wnsn = wnsn
        self.lexsn = lexsn
        self.pn = pn
        self.ot = ot
        self.word = word

    def __repr__(self):
        return "cmd = {}; rdf = {}; pos = {}; lemma = {}; wnsn = {}; lexn = {}; pn = {}; ot = {};" \
               "word = {}".format(self.cmd, self.rdf, self.pos, self.lemma, self.wnsn, self.lexsn,
                                  self.pn, self.ot, self.word)


class Loc:
    def __init__(self, sentence, word):
        self.sentence = sentence
        self.word = word


def __featureextractor__(semcor, dstdirectory, features):
    ftrvalues = features.split("_")
    ftrnumber = 0
    lminval = 0
    lmaxval = 0
    tminval = 0
    tmaxval = 0
    twt = False
    tw = False

    for ftrvalue in ftrvalues:
        if "-" in ftrvalue:
            ftrvalminus = ftrvalue.split("-")
            if ftrvalminus[0] is "l":
                lminval = int(ftrvalminus[1])
            else:
                tminval = int(ftrvalminus[1])
        elif "+" in ftrvalue:
            ftrvalplus = ftrvalue.split("+")
            if ftrvalplus[0] is "l":
                lmaxval = int(ftrvalplus[1])
            else:
                tmaxval = int(ftrvalplus[1])
        elif "twt" in ftrvalue:
            twt = True
            ftrnumber += 1
        elif "tw" in ftrvalue:
            tw = True
            ftrnumber += 1
    ftrnumber += (lmaxval + lminval)
    ftrnumber += (tmaxval + tminval)

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
    sentcnt = 0

    for s in values:
        s = s.strip()
        if s.find("<s snum") > 0:
            lines = s.split('\n')
            sentence = []
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
                            info = InfoSemcor(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, word)
                            sentence.append(info)
                            wval = windex.get(lemma)
                            if wval is None:
                                wval = list()
                                windex[lemma] = wval
                            wval.append(Loc(sentcnt, wcnt))
                            wcnt += 1
                            cmd = ""
                            rdf = ""
                            pos = ""
                            lemma = ""
                            wnsn = ""
                            lexsn = ""
                            pn = ""
                            ot = ""
        sentcnt += 1
        text.append(sentence)

    for wi in windex.keys():
        outfile = open(dstdirectory + "/" + wi + ".csv", "w")
        outfile.write('"SENSE"')
        curnum = 1
        for i in range(1, ftrnumber + 1):
            outfile.write('\t"A' + str(curnum) + '"')
            curnum += 1
        outfile.write('\n')

        for loc in windex.get(wi):
            slist = text[loc.sentence]
            lexsn = text[loc.sentence][loc.word].lexsn
            outstr = ''
            if lexsn is not None and len(lexsn) > 0:
                outstr += '"' + lexsn + '"\t'
                for i in range(loc.word - lminval, loc.word + lmaxval + 1):
                    if i != loc.word:
                        if i >= 0 and i < len(slist):
                            if slist[i].lemma is not "":
                                outstr += '"' + slist[i].lemma.lower() + '"\t'
                            else:
                                outstr += '"' + slist[i].word.lower() + '"\t'
                        else:
                            outstr += '"X"\t'
                for i in range(loc.word - tminval, loc.word + tmaxval + 1):
                    if i is not loc.word:
                        if i >= 0 and i < len(slist):
                            outstr += '"' + slist[i].pos + '"\t'
                        else:
                            outstr += '"X"\t'
                if tw:
                    outstr += '"' + text[loc.sentence][loc.word].word.lower() + '"\t'
                if twt:
                    outstr += '"' + text[loc.sentence][loc.word].pos + '"'
                if len(slist) > 1:
                    outstr += "\n"
            outfile.write(outstr)

        outfile.flush()
        outfile.close()

    print ("Successfully finished!")