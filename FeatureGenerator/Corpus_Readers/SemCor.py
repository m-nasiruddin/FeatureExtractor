#!/usr/bin/python
__author__ = 'Mohammad'


class SemCorTokenInfo:
    """this class contains SemCor3.0 information for each line (more specifically for each word)"""

    def __init__(self, cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token):
        """this method works as a constructor in Python and runs as soon as an object of a class is instantiated"""
        self.cmd = cmd  # it contains 'ignore', if the word is a function word (e.g. DT/IN/POS) and 'done', if not
        self.rdf = rdf  # it contains 'group' if the word is a group word (multiword expression/polylexical item),
        # 'location' if the word refers to a location
        self.pos = pos  # it contains part of speech info (e.g. DT, NNP, etc.)
        self.lemma = lemma  # it contains the lemma form of a word
        self.wnsn = wnsn  # it contains the no of sense info of this word (e.g. 1,2, etc.)
        self.lexsn = lexsn  # it contains the synset id (e.g. 1:03:00::, 2:32:00::, etc.)
        self.pn = pn  # same as 'rdf'
        self.ot = ot  # it contains 'notag', if not tag info is available
        self.token = token  # it contains the surface form a word

    def __repr__(self):
        """this is a built-in function which returns a string containing a printable representation of an object"""
        return 'cmd = {}; rdf = {}; pos = {}; lemma = {}; wnsn = {}; lexn = {}; pn = {}; ot = {}; token = {}' \
            .format(self.cmd, self.rdf, self.pos, self.lemma, self.wnsn, self.lexsn, self.pn, self.ot, self.token)


source_file = open('../dataset/sense_tagged_corpora/semcor3.0', 'r')  # source corpus path
output_file = open('../dataset/sense_tagged_corpora/buf_SemCor3.0', 'a')  # output corpus path
read_semcor = source_file.read()  # read the entire corpus at once
semcor_sentences = read_semcor.split('</s>')  # split the corpus by sentences
# initializing the list
cmd = ''
rdf = ''
pos = ''
lemma = ''
wnsn = ''
lexsn = ''
pn = ''
ot = ''
token = ''
for semcor_sentence in semcor_sentences:  # iterating over all the semcor sentences
    stripped_semcor_sentence = semcor_sentence.strip()  # remove leading and trailing white spaces
    if stripped_semcor_sentence.find('<s snum=') > -1:  # identifies the beginning of a sentence
        lines = stripped_semcor_sentence.split('\n')  # split by semcor lines (each semcor line contains word info)
        sentence_list = []  # sentence array declaration
        for line in lines:  # iterating over all the lines
            if line.startswith('<wf '):  # if the line starts with '<wf'
                split_lines = line.replace('>', ' ').split()  # line split by '>'
                for item in split_lines:  # iterating over all the split_lines
                    if item.startswith('cmd='):  # if item line starts with 'cmd='
                        cmd = item[4:]
                    elif item.startswith('rdf='):  # if item line starts with 'rdf'
                        rdf = item[4:]
                    elif item.startswith('pos='):  # if item line starts with 'pos'
                        pos = item[4:]
                    elif item.startswith('lemma='):  # if item line starts with 'lemma'
                        lemma = item[6:]
                    elif item.startswith('wnsn='):  # if item line starts with 'wnsn'
                        wnsn = item[5:]
                    elif item.startswith('lexsn='):  # if item line starts with 'lexsn'
                        lexsn = item[6:]
                    elif item.startswith('pn='):  # if the item starts with 'pn'
                        pn = item[3:]
                    elif item.startswith('ot='):  # if the item starts with 'ot'
                        ot = item[3:]
                    elif not item.startswith('<wf '):  # if the item starts with '<wf '
                        token = item[:item.index('<')]
                        # calls the SemEval2007Task7_Info class
                        token_info = SemCorTokenInfo(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token)  # calling the
                        # SemCorInfo class
                        sentence_list.append(token_info)  # for each line info is appending to the sentence list
                        # resets the list to empty
                        cmd = ''
                        rdf = ''
                        lemma = ''
                        pos = ''
                        wnsn = ''
                        lexsn = ''
                        pn = ''
                        ot = ''
                        token = ''
            elif line.startswith('<punc'):  # condition for punctuationa
                # as no info found for this line, items are set to empty
                cmd = ''
                rdf = ''
                lemma = ''
                pos = ''
                wnsn = ''
                lexsn = ''
                pn = ''
                ot = ''
                token = line[6:line.index('</punc>')]
                token_info = SemCorTokenInfo(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token)  # calling the SemCorInfo
                sentence_list.append(token_info)  # for each line info is appending to the sentence list
                # resets the list to empty
                cmd = ''
                rdf = ''
                lemma = ''
                pos = ''
                wnsn = ''
                lexsn = ''
                pn = ''
                ot = ''
                token = ''
        # print sentence_list
        for sentence_token_info in sentence_list:  # iterating over a sentence
            output_file.write(sentence_token_info.token)
            output_file.write(' ')
    output_file.write('\n')
print('FINISHED!')