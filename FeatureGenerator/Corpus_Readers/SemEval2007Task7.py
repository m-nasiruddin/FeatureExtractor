#!/usr/bin/python
__author__ = 'Mohammad'


class SemEval2007Task7TokenInfo:
    """this class contains SemEval2007Task7 information"""

    def __init__(self, id, lemma, pos, token):
        """this method works as a constructor in Python and runs as soon as an object of a class is instantiated"""
        self.id = id  # it contains 'ignore', if the word is a function word (e.g. DT/IN/POS) and 'done', if not
        self.lemma = lemma  # it contains the lemma form of a word
        self.pos = pos  # it contains part of speech info (e.g. DT, NNP, etc.)
        self.token = token  # it contains the surface form a word

    def __repr__(self):
        """this is a built-in function which returns a string containing a printable representation of an object"""
        return 'id = {}; lemma = {}; pos = {}; token = {}'.format(self.id, self.lemma, self.pos, self.token)


source_file = open('../dataset/evaluation_corpora/SemEval2007Task7', 'r')  # source corpus path
output_file = open('../dataset/evaluation_corpora/buf_SemEval2007Task7', 'a')  # output corpus path
read_semcor = source_file.read()  # read the entire corpus at once
semcor_sentences = read_semcor.split('</sentence>')  # split the corpus by sentences
# initializing the list
id = ''
lemma = ''
pos = ''
token = ''
for semcor_sentence in semcor_sentences:  # iterating over all the semcor sentences
    stripped_semcor_sentence = semcor_sentence.strip()  # remove leading and trailing white spaces
    if stripped_semcor_sentence.find('<sentence id=') > -1:  # identifies the beginning of a sentence
        lines = stripped_semcor_sentence.split('\n')  # split by ne lines
        sentence_list = []  # sentence array declaration
        for line in lines:  # iterating over all the lines
            if line.startswith('<instance '):  # if the line starts with '<wf'
                split_lines = line.replace('>', ' ').split()  # line split by '>'
                for item in split_lines:  # iterating over all the split_lines
                    if item.startswith('id='):  # if item line starts with 'cmd='
                        id = item[3:].strip('"')
                    elif item.startswith('lemma='):  # if item line starts with 'lemma'
                        lemma = item[6:].strip('"')
                    elif item.startswith('pos='):  # if item line starts with 'pos'
                        pos = item[4:].strip('"')
                    elif not item.startswith('<instance '):  # if the item starts with '<wf '
                        token = item[:item.index('<')].strip('"')
                        token_info = SemEval2007Task7TokenInfo(id, lemma, pos,
                                                               token)  # calls the SemEval2007Task7_Info class
                        sentence_list.append(token_info)  # for each line info is appending to the sentence list
                        # resets the list to empty
                        id = ''
                        lemma = ''
                        pos = ''
                        token = ''
            elif not line.startswith('<'):  # condition for removing header and footer
                # as no info found for this line, items are set to empty
                id = ''
                lemma = ''
                pos = ''
                token = line
                token_info = SemEval2007Task7TokenInfo(id, lemma, pos, token)  # calling the SemEval2007Task7_Info class
                sentence_list.append(token_info)  # for each line info is appending to the sentence list
                # resets the list to empty
                id = ''
                lemma = ''
                pos = ''
                token = ''
        print sentence_list
        for sentence_token_info in sentence_list:  # iterating over a sentence
            output_file.write(sentence_token_info.lemma)
            output_file.write(' ')
print('FINISHED!')