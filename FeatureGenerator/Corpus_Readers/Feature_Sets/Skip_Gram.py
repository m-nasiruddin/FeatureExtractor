#!/usr/bin/python
__author__ = 'Mohammad'

import os
import shutil


def skip_gram_features(full_sentence_info_list, k_skip, n_gram):
    """pos-tag features (takes a range (left and right) and prints pos-tag info, without the target word)"""
    # Open a file
    shutil.rmtree('../dataset/output')  # removes a directory with sub directories and files
    os.mkdir('../dataset/output')  # creates a new directory
    output_file = open('../dataset/output/jurry.skip.txt', 'a')  # open a file in append mode

    grams = []
    for full_sentence_info in full_sentence_info_list:  # iterates ove the values (sentence_info(s)) list
        if n_gram == 0 or len(full_sentence_info) == 0:
            return None
        for i in range(len(full_sentence_info) - n_gram + 1):
            grams.extend(initial_skip_grams(full_sentence_info[i:], k_skip, n_gram))
    for gram in grams:  # for printing the skip_gram
        for gra in gram:
            output_file.write(gra.token + '_')
        output_file.write('\n')
    output_file.close()  # closes the file


def initial_skip_grams(full_sentence_info, k_skip, n_gram):
    """this function responsible for the initial skip grams"""
    if n_gram == 1:
        return [[full_sentence_info[0]]]
    grams = []
    for j in range(min(k_skip + 1, len(full_sentence_info) - 1)):
        kmj_skip_nm1_grams = initial_skip_grams(full_sentence_info[j + 1:], k_skip - j, n_gram - 1)
        if kmj_skip_nm1_grams is not None:
            for gram in kmj_skip_nm1_grams:
                grams.append([full_sentence_info[0]] + gram)
    return grams