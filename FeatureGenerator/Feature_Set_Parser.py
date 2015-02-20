#!/usr/bin/python
__author__ = 'Mohammad'


class Feature_Set_Parser:
    def __init__(self, pos, collocation, surrounding_word, n_gram, skip_gram):
        self.pos = pos
        self.collocation = collocation
        self.surrounding_word = surrounding_word
        self.n_gram = n_gram
        self.skip_gram = skip_gram