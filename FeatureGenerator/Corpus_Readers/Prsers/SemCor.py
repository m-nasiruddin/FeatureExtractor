__author__ = 'Mohammad'


def semcor_parser(read_file):
    semcor_sentences = read_file.split('</s>')  # split the corpus by sentences
    # # initializing the list
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
                            cmd = item[4:]  # takes the value from the index 4 to the end
                        elif item.startswith('rdf='):  # if item line starts with 'rdf='
                            rdf = item[4:]  # takes the value from the index 4 to the end
                        elif item.startswith('pos='):  # if item line starts with 'pos='
                            pos = item[4:]  # takes the value from the index 4 to the end
                        elif item.startswith('lemma='):  # if item line starts with 'lemma='
                            lemma = item[6:]  # takes the value from the index 6 to the end
                        elif item.startswith('wnsn='):  # if item line starts with 'wnsn='
                            wnsn = item[5:]  # takes the value from the index 5 to the end
                        elif item.startswith('lexsn='):  # if item line starts with 'lexsn='
                            lexsn = item[6:]  # takes the value from the index 6 to the end
                        elif item.startswith('pn='):  # if the item starts with 'pn='
                            pn = item[3:]  # takes the value from the index 3 to the end
                        elif item.startswith('ot='):  # if the item starts with 'ot='
                            ot = item[3:]  # takes the value from the index 3 to the end
                        else:  # it works for tokens
                            token = item[:item.index('<')]  # takes the value from the beginning to the '<' symbol
                    token_info = SemCorTokenInfo(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token)  # instantiate the
                    # SemCor_Info class
                    sentence_info.append(token_info)  # for each line info is appending to the sentence list
                    # # resets the list to empty
                    cmd = ''
                    rdf = ''
                    lemma = ''
                    pos = ''
                    wnsn = ''
                    lexsn = ''
                    pn = ''
                    ot = ''
                    token = ''
                elif line.startswith('<punc>'):  # condition for punctuation
                    # # as no info found for this line, items are set to empty
                    cmd = ''
                    rdf = ''
                    lemma = ''
                    pos = ''
                    wnsn = ''
                    lexsn = ''
                    pn = ''
                    ot = ''
                    token = line[6:line.index('</punc>')]  # takes the punctuation as a token
                    token_info = SemCorTokenInfo(cmd, rdf, pos, lemma, wnsn, lexsn, pn, ot, token)  # instantiate the
                    # SemCor_Info class
                    sentence_info.append(token_info)  # for each line info is appending to the sentence list
                    # # resets the list to empty
                    cmd = ''
                    rdf = ''
                    lemma = ''
                    pos = ''
                    wnsn = ''
                    lexsn = ''
                    pn = ''
                    ot = ''
                    token = ''
        sentence_info_list.append(sentence_info)  # all the sentence_info are appending into the
    token_sentence_info_dict_generator(sentence_info_list)  # calls token_sentence_info_dict_generator
    # function passing the parameter sentence_info_list