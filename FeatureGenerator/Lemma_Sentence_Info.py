#!/usr/bin/python
__author__ = 'Mohammad'

import FeatureExtractor.FeatureGenerator.Corpus_Readers.SemCor


class Lemma_Sentence_Info:
    def __init__(self, sentence, lemma):
        self.sentence = sentence
        self.word = lemma


for token in FeatureExtractor.FeatureGenerator.Corpus_Readers.SemCor.sentence_list:  # iterating over a sentence
    print(token)