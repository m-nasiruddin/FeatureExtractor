#!/usr/bin/python
__author__ = 'Mohammad'

import os
import shutil


def surrounding_words(full_sentence_info_list, target_key_info):
    """pos-tag features (takes a range (left and right) and prints pos-tag info, without the target word)"""
    # Open a file
    shutil.rmtree('../dataset/output')  # removes a directory with sub directories and files
    os.mkdir('../dataset/output')  # creates a new directory
    output_file = open('../dataset/output/jurry.sur.txt', 'a')  # open a file in append mode

    token_info_vocabulary = []
    all_token_info_vocabulary = []
    for full_sentence_info in full_sentence_info_list:  # iterates ove the values (sentence_info(s)) list
        for token_info_val in full_sentence_info:  # iterates ove the values (sentence_info(s)) list
            if token_info_val != target_key_info:  # detects the target info [we don't want to consider the target info]
                all_token_info_vocabulary.append(token_info_val)  # adds values in token_info_vocabulary
    unique_all_token_info_vocabulary = set(all_token_info_vocabulary)  # set() function removes duplicate entries

    output_file.write('SENSE\t')  # sense id header
    for token_index, token_info_val in enumerate(unique_all_token_info_vocabulary, start=1):  # iterates over the values
        # (sentence_info(s)) list
        output_file.write('A' + str(token_index) + '\t')  # writes the header with numbers
    output_file.write('\n')  # writes a newline

    for full_sentence_info in full_sentence_info_list:  # iterates ove the values (sentence_info(s)) list
        for token_info_val in full_sentence_info:  # iterates ove the values (sentence_info(s)) list
            token_info_vocabulary.append(token_info_val)  # adds values in token_info_vocabulary
            unique_token_info_vocabulary = set(token_info_vocabulary)  # set() function removes duplicate entries
        for vocabulary in unique_all_token_info_vocabulary:
            if vocabulary in unique_token_info_vocabulary:  # detects the target info [we want not to consider the target info]
                output_file.write(vocabulary.token + '\t')  # prints the right pos-tag info
            else:
                output_file.write('0' + '\t')
        output_file.write('\n')
    output_file.close()  # closes the file