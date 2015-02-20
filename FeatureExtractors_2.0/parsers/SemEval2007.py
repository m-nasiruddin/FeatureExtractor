__author__ = 'nasirudd'


class InfoSemEval2007:
    def __init__(self, id, lemma, pos, word):
        self.id = id
        self.lemma = lemma
        self.pos = pos
        self.word = word


    def __repr__(self):
        return 'id = {}; lemma = {}; pos = {}; word = {}'.format(self.id, self.lemma, self.pos, self.word)


source_file = open('../data/SemEval2007task7/test/eng-coarse-all-words.xml', 'r')
output_file = open('semeval_raw', 'a')

read_source_file = source_file.read()
sentences = read_source_file.split('</sentence>')
id = ''
lemma = ''
pos = ''
word = ''

for sentence in sentences:
    sentence = sentence.strip()
    if sentence.find('<sentence id') > 0:
        lines = sentence.split('\n')
        semeval_info = []
        for line in lines:
            if line.startswith('<instance'):
                line_split = line.replace('>', ' ').split()
                # print(line_split)
                for item in line_split:
                    if item.startswith('id'):
                        id = item[3:].strip('"')
                    elif item.startswith('lemma'):
                        lemma = item[6:].strip('"')
                    elif item.startswith('pos'):
                        pos = item[4:].strip('"')
                    elif not item.startswith('<instance'):
                        word = item[:item.index('<')]
                        info = InfoSemEval2007(id, lemma, pos, word)
                        semeval_info.append(info)
                        id = ''
                        lemma = ''
                        pos = ''
                        word = ''
            else:
                output_file.write(line + ' ')

        print semeval_info
        for infos in semeval_info:
            output_file.write(infos.lemma)
            output_file.write(' ')
print('FINISH')