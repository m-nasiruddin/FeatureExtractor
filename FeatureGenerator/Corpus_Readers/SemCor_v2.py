#!/usr/bin/python
__author__ = 'Mohammad'


class SemCorTokenInfo:
    """this class contains SemCor3.0 information for each line (more specifically for each word)"""

    def __init__(self, wf_cmd, wf_rdf, wf_pos, wf_lemma, wf_wnsn, wf_lexsn, wf_pn, wf_ot, wf_token):
        self.cmd = wf_cmd  # it contains 'ignore', if the word is a function word (e.g. DT/IN/POS) and 'done', if not
        self.rdf = wf_rdf  # it contains 'group' if the word is a group word (multiword expression/polylexical item),
        # 'location' if the word refers to a location
        self.pos = wf_pos  # it contains part of speech info (e.g. DT, NNP, etc.)
        self.lemma = wf_lemma  # it contains the lemma form of a word
        self.wnsn = wf_wnsn  # it contains the no of sense info of this word (e.g. 1,2, etc.)
        self.lexsn = wf_lexsn  # it contains the synset id (e.g. 1:03:00::, 2:32:00::, etc.)
        self.pn = wf_pn  # same as 'rdf'
        self.ot = wf_ot  # it contains 'notag', if not tag info is available
        self.token = wf_token  # it contains the surface form a word

    def __repr__(self):
        """this is a built-in function which returns a string containing a printable representation of an object"""
        return 'cmd = {}; rdf = {}; pos = {}; lemma = {}; wnsn = {}; lexn = {}; pn = {}; ot = {}; token = {}' \
            .format(self.cmd, self.rdf, self.pos, self.lemma, self.wnsn, self.lexsn, self.pn, self.ot, self.token)

    def __eq__(self, other):
        """normally object/instance values aren't comparable, this method compares whether values of two instances are
        equal or not"""
        return self.cmd == other.cmd and self.rdf == other.rdf and self.pos == other.pos and self.lemma == other.lemma \
               and self.wnsn == other.wnsn and self.lexsn == other.lexsn and self.pn == other.pn and self.ot == other.ot \
               and self.token == other.token

    def __hash__(self):
        """this method redefines the hashable object"""
        return hash((self.cmd, self.rdf, self.pos, self.lemma, self.wnsn, self.lexsn, self.pn, self.ot, self.token))

# class LemmaSentenceInfo(SemCorTokenInfo):
# """this class contains SemCor3.0 information for lemma and corresponding sentences for each line (more
#     specifically for each word)"""
#     def __init__(self, lemma_info, sentence_info):
#         self.lemma_info = lemma_info  # it contains 'ignore', if the word is a function word (e.g. DT/IN/POS) and
#         # 'done', if not
#         self.sentence_info = sentence_info  # it contains the surface form of a word
#
#     def __repr__(self):
#         """this is a built-in function which returns a string containing a printable representation of an object"""
#         return 'lemma_info = {}; sentence_info = {}'.format(self.lemma_info, self.sentence_info)

token_sentence_info_dict = {}  # dictionary for unique lemma_info
source_file = open('../dataset/sense_tagged_corpora/semcor3.0', 'r')  # source corpus path
# output_file = open('../dataset/sense_tagged_corpora/buf_SemCor3.0', 'a')  # output corpus path
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
sentence_info_list = []  # sentence array declaration
for semcor_sentence in semcor_sentences:  # iterating over all the semcor sentences
    stripped_semcor_sentence = semcor_sentence.strip()  # remove leading and trailing white spaces
    sentence_info = []  # token array declaration
    if stripped_semcor_sentence.find('<s snum=') > -1:  # identifies the beginning of a sentence
        lines = stripped_semcor_sentence.split('\n')  # split by semcor lines (each semcor line contains word info)
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
                        token_info = SemCorTokenInfo(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token)
                        sentence_info.append(token_info)  # for each line info is appending to the sentence list
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
            elif line.startswith('<punc'):  # condition for punctuation
                # as no info found for this line, items are set to empty
                cmd = ''
                rdf = ''
                lemma = ''
                pos = ''
                wnsn = ''
                lexsn = ''
                pn = ''
                ot = ''
                token = line[6:line.index('</punc>')]  # takes the punctuation as a token
                token_info = SemCorTokenInfo(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token)  # calling SemCor_Info
                sentence_info.append(token_info)  # for each line info is appending to the sentence list
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
    sentence_info_list.append(sentence_info)  # all the sentence_info are appending into the sentence_info_list
for sentence_info_val in sentence_info_list:  # iterating over a sentence
    for token_info_key in sentence_info_val:  # iterating over a sentence
        if token_info_key not in token_sentence_info_dict:  # checks if the token_sentence_info_dict doesn't contain
            # token_info
            token_sentence_info_dict[token_info_key] = []  # creates an empty list for each token_info
        token_sentence_info_dict[token_info_key].append(sentence_info_val)  # with the corresponding token_info puts
        # the sentence_info in the dictionary

# for printing the dictionary keys and values
target_index_list = []  # target_index list declaration
for key in sorted(token_sentence_info_dict):  # reads the keys from the dictionary
    if key.lemma == 'jury':  # HARDCODED: search for a lemma in the keys
        print("\n\n\n=== KEY ===: " + key.token, len(token_sentence_info_dict[key]))  # prints the tokens in the key
        # and the length of values for corresponding keys
        # len(token_sentence_info_dict[key]) gives the number of items (sentences) for a particular key (lemma/token)
        for value in token_sentence_info_dict[key]:  # iterates ove the values (sentence_info) of a key (token_info)
            for token_info_val in value:  # iterates ove the values (sentence_info) list for each token_info

                # pos-tag feature
                if key.lemma == token_info_val.lemma:  # checks the key (lemma/token) in the values (sentences)
                    sentence_length = len(value)  # get the length of a sentence
                    print(sentence_length)  # prints the length of a sentence
                    target_index = value.index(key)  # gets the target index/index of the key (lemma/token) in the
                    # values (sentences)
                    target_index_list.append(value.index(key))  # stores target index in a list
                    maximum_index = max(target_index_list)  # get the maximum value of target index
                    print(target_index)  # gets the index of the key (lemma/token) in the values (sentences)
                    print(token_info_val.lemma)
print(maximum_index)
print('FINISHED!')