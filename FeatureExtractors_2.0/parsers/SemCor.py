class InfoSemCor:
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

    def is_punc(self):
        return len(self.cmd) == 0 and \
               len(self.rdf) == 0 and \
               len(self.pos) == 0 and \
               len(self.lemma) == 0 and \
               len(self.wnsn) == 0 and \
               len(self.lexsn) == 0 and \
               len(self.pn) == 0 and \
               len(self.ot) == 0 and \
               len(self.word) > 0

    def __repr__(self):
        return "cmd = {}; rdf = {}; pos = {}; lemma = {}; wnsn = {}; lexn = {}; pn = {}; ot = {};" \
               "word = {}".format(self.cmd, self.rdf, self.pos, self.lemma, self.wnsn, self.lexsn,
                                  self.pn, self.ot, self.word)
